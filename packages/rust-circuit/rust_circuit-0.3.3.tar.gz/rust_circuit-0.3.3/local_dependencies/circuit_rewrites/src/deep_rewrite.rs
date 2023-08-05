use circuit_base::{
    deep_map_op_context, deep_map_preorder_unwrap, deep_map_unwrap, prelude::*,
    visit_circuit_unwrap, Add, Concat, GeneralFunction, Index,
};
use itertools::Itertools;
use num_bigint::BigUint;
use pyo3::prelude::*;
use rr_util::{
    timed, timed_value,
    util::{apply_fn_until_none, apply_fn_until_same, mapping_until_end, AsOp},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use crate::{
    algebraic_rewrite::*,
    batching::batch_einsum,
    canonicalize::deep_canonicalize,
    circuit_optimizer::OptimizationContext,
    concat_rewrite::{
        add_pull_concat, concat_drop_size_zero, concat_fuse, einsum_pull_concat,
        generalfunction_pull_concat, index_concat_drop_unreached,
    },
    diag_rewrite::{add_pull_diags, einsum_push_down_trace},
    generalfunction_rewrite::{
        generalfunction_evaluate_simple, generalfunction_merge_inverses,
        generalfunction_special_case_simplification,
    },
    module_rewrite::elim_empty_module,
    nb_rewrites::{add_elim_removable_axes_weak, einsum_elim_removable_axes_weak},
    scatter_rewrite::{
        add_pull_scatter, concat_to_scatter, einsum_pull_scatter, index_einsum_to_scatter,
        scatter_elim_identity, scatter_fuse, scatter_pull_removable_axes,
    },
};

/// seperate _py function because pyfunctions cant take reference arguments
#[pyfunction]
#[pyo3(name = "compiler_simp_step")]
pub fn compiler_simp_step_py(circ: CircuitRc) -> Option<CircuitRc> {
    compiler_simp_step(&circ, &mut Default::default())
}

fn simp<'a, T: CircuitNode + Into<Circuit> + Clone>(
    x: &'a T,
    fns: &[(&'static str, &dyn Fn(&'a T) -> Option<CircuitRc>)],
    context: &mut OptimizationContext,
) -> Option<CircuitRc> {
    for (name, f) in fns {
        if let Some(result) = f(x) {
            if **result == x.clone().c() {
                println!("{}", stringify!(f));
                x.crc().compiler_print();
                result.compiler_print();
                panic!()
            }
            if context.settings.log_simplifications {
                if context.settings.verbose >= 3 {
                    println!("{}", name);
                }
                context.cache.simplification_log.push(name);
            }
            return Some(result);
        }
    }

    None
}

macro_rules! f_wrap {
    ($f:expr) => {
        (stringify!($f), &|x| $f(x).map(|v| v.rc()))
    };
}

macro_rules! l_wrap {
    ($f:expr) => {
        (stringify!($f), &|x| $f(x))
    };
}

pub fn compiler_simp_step(
    circuit: &Circuit,
    context: &mut OptimizationContext,
) -> Option<CircuitRc> {
    match &*circuit {
        Circuit::Add(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(&remove_add_few_input),
                f_wrap!(add_flatten_once),
                f_wrap!(add_elim_zeros),
                f_wrap!(add_collapse_scalar_inputs),
                f_wrap!(add_deduplicate),
                l_wrap!(|x| add_pull_removable_axes(x, true)),
                f_wrap!(add_pull_scatter),
                f_wrap!(add_pull_diags),
                f_wrap!(add_fuse_scalar_multiples),
            ];
            simp(node, fns, context)
        }
        Circuit::Einsum(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                f_wrap!(&einsum_elim_zero),
                l_wrap!(einsum_elim_identity),
                f_wrap!(&einsum_flatten_once),
                f_wrap!(&einsum_of_permute_merge),
                f_wrap!(&einsum_merge_scalars),
                l_wrap!(einsum_pull_removable_axes),
                f_wrap!(&|x| einsum_permute_to_rearrange(x)
                    .map(|z| z.conform_to_input_shape(true).unwrap())),
                l_wrap!(einsum_pull_scatter),
                f_wrap!(&einsum_push_down_trace),
                f_wrap!(&einsum_concat_to_add),
            ];
            simp(node, fns, context)
        }
        Circuit::Index(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(index_elim_identity),
                f_wrap!(&index_fuse),
                l_wrap!(index_merge_scalar),
                l_wrap!(index_einsum_to_scatter),
                l_wrap!(index_concat_drop_unreached),
            ];
            simp(node, fns, context)
        }
        Circuit::Rearrange(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(rearrange_elim_identity),
                f_wrap!(&rearrange_fuse),
                l_wrap!(rearrange_merge_scalar),
                f_wrap!(&permute_of_einsum_merge),
            ];
            simp(node, fns, context)
        }
        Circuit::Concat(node) => {
            let fns: &[(&'static str, &dyn Fn(&Concat) -> _)] = &[
                l_wrap!(concat_elim_identity),
                l_wrap!(concat_pull_removable_axes),
                l_wrap!(concat_merge_uniform),
                f_wrap!(&concat_drop_size_zero),
                f_wrap!(&concat_fuse),
                f_wrap!(&concat_repeat_to_rearrange),
                f_wrap!(&concat_to_scatter),
            ];
            simp(node, fns, context)
        }
        Circuit::GeneralFunction(node) => {
            let fns: &[(&'static str, &dyn Fn(&GeneralFunction) -> _)] = &[
                l_wrap!(generalfunction_pull_removable_axes),
                l_wrap!(generalfunction_merge_inverses),
                l_wrap!(generalfunction_special_case_simplification),
                l_wrap!(generalfunction_evaluate_simple),
            ];
            simp(node, fns, context)
        }
        Circuit::Scatter(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(scatter_elim_identity),
                f_wrap!(&scatter_fuse),
                f_wrap!(&scatter_pull_removable_axes),
            ];
            simp(node, fns, context)
        }
        Circuit::ModuleNode(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[l_wrap!(&elim_empty_module)];
            simp(node, fns, context)
        }
        _ => None,
    }
}

#[pyfunction]
#[pyo3(name = "compiler_simp")]
pub fn compiler_simp_py(circ: CircuitRc) -> CircuitRc {
    let mut context = Default::default();
    compiler_simp(circ, &mut context)
}

pub fn compiler_simp(circ: CircuitRc, opt_context: &mut OptimizationContext) -> CircuitRc {
    deep_simp(circ, opt_context, compiler_simp_step)
}

// original python simp
// def basic_simp_elem(
//     c: Circuit,
//     cum_trivial_expand: bool = False,
//     cumulant_namer: GetPrefixShortNames = lambda _: None,
//     cum_expand_through_factored_add_concat: bool = False,
//     cum_expand_through_diags: bool = True,
//     use_remove_noop_rearrange: bool = False,  # off by default because this makes cumulant stuff non-deterministic!
//     use_factoring: bool = False,
//     use_flatten_adds: bool = True,
//     use_push_down_permute_via_einsum: bool = False,
//     excludes: Set[Rewrite] = set(),
//     extras: List[Rewrite] = [],
//     until: Callable[[Circuit], bool] = lambda _: False,
//     print_updates: bool = False,
// ) -> Circuit:
//     base_transforms: List[Rewrite] = [
//         try_eliminate_zeros,
//         try_remove_add_times_one,
//         try_remove_single_concat,
//         try_remove_trivial_index,
//         try_remove_empty_einsum,
//         try_drop_zero_add,
//         try_zero_empty_add,
//         try_drop_mul_ones,
//         try_fuse_einsum_rearrange,
//         try_fuse_permute_einsum,
//         try_fuse_rearrange,
//         try_fuse_single_einsum,
//         try_fuse_einsum_single,
//         try_rearrange_of_const_to_const,
//         try_nested_einsum_permute_dups_to_eq,
//     ]

/// this doesn't have enough options + isn't similar enough to python one. we'll use a HOF for options
pub fn basic_simp_step(circuit: &Circuit, context: &mut OptimizationContext) -> Option<CircuitRc> {
    match &*circuit {
        Circuit::Add(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(&remove_add_few_input),
                f_wrap!(add_elim_zeros),
                f_wrap!(add_deduplicate),
                f_wrap!(add_elim_removable_axes_weak),
            ];
            simp(node, fns, context)
        }
        Circuit::Einsum(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                f_wrap!(&einsum_elim_zero),
                l_wrap!(einsum_elim_identity),
                f_wrap!(&einsum_of_permute_merge),
                f_wrap!(&einsum_elim_removable_axes_weak),
                f_wrap!(&|x| einsum_permute_to_rearrange(x)
                    .map(|z| z.conform_to_input_shape(true).unwrap())),
            ];
            simp(node, fns, context)
        }
        Circuit::Index(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(index_elim_identity),
                f_wrap!(&index_fuse),
                l_wrap!(index_merge_scalar),
            ];
            simp(node, fns, context)
        }
        Circuit::Rearrange(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(rearrange_elim_identity),
                f_wrap!(&rearrange_fuse),
                l_wrap!(rearrange_merge_scalar),
                f_wrap!(&permute_of_einsum_merge),
            ];
            simp(node, fns, context)
        }
        Circuit::Concat(node) => {
            let fns: &[(&'static str, &dyn Fn(&Concat) -> _)] = &[
                l_wrap!(concat_elim_identity),
                l_wrap!(concat_merge_uniform),
                f_wrap!(&concat_drop_size_zero),
                f_wrap!(&concat_fuse),
                f_wrap!(&concat_repeat_to_rearrange),
            ];
            simp(node, fns, context)
        }
        _ => None,
    }
}

/// Deep simplification strategy
///
/// The strategy to apply `compiler_simp_step` to each node in the circuit from the bottom up (post-order).
/// Every time a node is simplified, we iterate over the children to make sure that any children we haven't
/// seen before get recursively fully simplified before continuing.
/// The final result is a fixed point where no further `compiler_simp_step` simplifications are possible.
pub fn deep_simp<F>(circ: CircuitRc, opt_context: &mut OptimizationContext, f: F) -> CircuitRc
where
    F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
{
    /// check if any new children have not been simplified yet, and simplify them if so
    fn simplify_changed_descendants<F>(
        circ: CircuitRc,
        context: &mut OptimizationContext,
        f: &F,
    ) -> Option<CircuitRc>
    where
        F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
    {
        // if let Some(changed) = compiler_simp_step(circ){
        //     return simplify_changed_descendants(circ, simplified)
        // }
        circ.map_children_op(&mut |x: CircuitRc| {
            if context.cache.simplified.contains_key(&x.info().hash) {
                None
            } else {
                Some(fully_simplify(x, context, f))
            }
        })
        .map(|c| c.rc())
    }
    /// fully simplify a circuit and all its descendants recursively until we hit a fixed point
    fn fully_simplify<F>(circ: CircuitRc, context: &mut OptimizationContext, f: &F) -> CircuitRc
    where
        F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
    {
        if let Some(result) = context.cache.simplified.get(&circ.info().hash) {
            return result.clone();
        }
        let mut result: CircuitRc = circ
            .map_children_unwrap(&mut |x: CircuitRc| fully_simplify(x, context, f))
            .rc();
        for iter_count in 0.. {
            match f(&result, context) {
                Some(r) => {
                    result = simplify_changed_descendants(r.clone(), context, f).unwrap_or(r)
                }
                None => break,
            }
            if iter_count > 50 {
                result.compiler_print();
                f(&result, context).unwrap().compiler_print();
                panic!();
            }
        }
        context
            .cache
            .simplified
            .insert(circ.info().hash, result.clone());
        result
    }
    fully_simplify(circ, opt_context, &f)
}

#[pyfunction]
pub fn basic_simp(circuit: CircuitRc) -> CircuitRc {
    deep_simp(circuit, &mut Default::default(), basic_simp_step)
}

#[pyfunction]
pub fn compiler_simp_until_same(circ: CircuitRc) -> CircuitRc {
    let mut context = Default::default();

    apply_fn_until_same(&circ, |x: &CircuitRc| {
        compiler_simp(x.clone(), &mut context)
    })
}

#[pyfunction]
pub fn deep_push_down_index(circ: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_preorder_unwrap(circ, |circ| {
        if min_size.is_none()
            || circ
                .children()
                .chain(std::iter::once(circ.clone()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            (**circ).map_or_clone(&|index: &Index| {
                let fused = apply_fn_until_none(index, index_fuse);
                index_elim_identity(&fused)
                    .unwrap_or_else(|| push_down_index(&fused).unwrap_or_else(|| fused.crc()))
            })
        } else {
            circ
        }
    })
}

/// we want adds to be nested rather than flat so arguments can be dropped if they're only needed
/// in future adds
/// this is suboptimal in many ways. one is broadcasts allow outer products which should be avoided but aren't
/// for each add, greedily nest into preexisting adds
#[pyfunction]
pub fn deep_heuristic_nest_adds(circ: CircuitRc) -> CircuitRc {
    let circ = deep_canonicalize(circ, &mut Default::default());
    let mut seen_adds: HashSet<Add> = HashSet::default();
    visit_circuit_unwrap(circ.clone(), |c: CircuitRc| {
        if let Some(add) = c.as_add() {
            seen_adds.insert(add.clone());
        }
    });
    // TODO: profile and optimize these

    let mut intersections: HashSet<Add> = HashSet::default();
    for circ in &seen_adds {
        for circ2 in &seen_adds {
            let intersection = Add::new(
                circ.nodes
                    .iter()
                    .filter(|x| circ2.nodes.contains(x))
                    .cloned()
                    .collect(),
                None,
            );
            if intersection.nodes.len() >= 2 && &intersection != circ && &intersection != circ2 {
                intersections.insert(intersection);
            }
        }
    }
    seen_adds.extend(intersections);
    let mut mapping: HashMap<Add, Add> = HashMap::default();
    while let Some((sup, new_sup)) = (|| {
        for cand_sub in &seen_adds {
            if cand_sub.nodes.len() >= 2 {
                for cand_sup in &seen_adds {
                    if cand_sub != cand_sup
                        && cand_sup
                            .nodes
                            .iter()
                            .position(|x| x.info().hash == cand_sub.info().hash)
                            .is_some()
                    {
                        if let Some(new) = extract_add(cand_sup, cand_sub) {
                            return Some((cand_sup.clone(), new));
                        }
                    }
                }
            }
        }
        None
    })() {
        seen_adds.remove(&sup);
        seen_adds.insert(new_sup.clone());
        mapping.insert(sup, new_sup.clone());
    }

    deep_map_preorder_unwrap(circ, |c| {
        (**c).map_or_clone(|add: &Add| {
            let add = mapping_until_end(add, &mapping);

            if add.info().numel() > BigUint::from(100_000_000usize) {
                add_nest_ltr(&add)
            } else {
                add
            }
        })
    })
}

pub fn add_nest_ltr(add: &Add) -> Add {
    let (l, r) = add.nodes.split_at(2.min(add.nodes.len()));
    let base = Add::new(l.to_vec(), None);
    r.iter()
        .fold(base, |acc, x| Add::new(vec![acc.rc(), x.clone()], None))
}

#[pyfunction]
#[pyo3(name = "add_nest_ltr")]
pub fn add_nest_ltr_py(add: Add) -> Add {
    add_nest_ltr(&add)
}

#[pyfunction]
pub fn deep_pull_concat_messy(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_unwrap(circuit, &|x: CircuitRc| {
        if min_size.is_none()
            || x.children()
                .chain(std::iter::once(x.clone()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            match &**x {
                Circuit::Add(add) => add.and_then_or_clone(add_pull_concat),
                Circuit::GeneralFunction(func) => {
                    func.and_then_or_clone(generalfunction_pull_concat)
                }
                Circuit::Einsum(einsum) => einsum.and_then_or_clone(einsum_pull_concat),
                Circuit::Concat(concat) => concat.and_then_or_clone(concat_fuse),
                _ => x.clone(),
            }
        } else {
            x
        }
    })
}

#[pyfunction]
pub fn deep_pull_concat(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    let mut cache = Default::default();
    let pulled = deep_pull_concat_messy(circuit, min_size);
    apply_fn_until_same(&pulled, |x: &CircuitRc| {
        deep_push_down_index(compiler_simp(x.clone(), &mut cache), min_size)
    })
}

#[pyfunction]
#[pyo3(name = "deep_optimize_einsums")]
pub fn deep_optimize_einsums_py(circ: CircuitRc) -> CircuitRc {
    deep_optimize_einsums(circ, &mut Default::default())
}

pub fn deep_optimize_einsums(circ: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        circ.clone(),
        &|x: CircuitRc, context: &mut OptimizationContext| match &**x {
            Circuit::Einsum(ein) => {
                let (result, took) = timed_value!(einsum_nest_optimize(ein, context));
                if result.is_none() {
                    Some(timed!(batch_einsum(ein, context).unwrap()))
                } else {
                    let result = result?;
                    if context.settings.log_slow_einsums && took.as_millis() > 10 {
                        context.cache.slow_einsum_log.push(ein.get_spec());
                    }
                    Some(result.rc())
                }
            }
            _ => None,
        },
        context,
        &mut HashMap::default(),
    )
    .unwrap_or(circ)
}
