use anyhow::Result;
use circuit_base::{
    circuit_utils::{count_nodes, prefix_all_names},
    CircuitNode, CircuitRc, ModuleNode, ModuleNodeArgSpec, ModuleNodeSpec,
};
use pyo3::prelude::*;
#[pyfunction]
pub fn elim_empty_module(circuit: &ModuleNode) -> Option<CircuitRc> {
    if count_nodes(circuit.spec.spec_circuit.clone()) == 1 {
        return Some(circuit.nodes[0].clone());
    }
    return None;
}

#[pyfunction(require_all_inputs = "false")]
pub fn extract_rewrite_raw(
    circuit: CircuitRc,
    input_specs: Vec<(CircuitRc, ModuleNodeArgSpec)>,
    prefix_to_strip: Option<String>,
    module_name: Option<String>,
    spec_name: Option<String>,
    require_all_inputs: bool,
) -> Result<ModuleNode> {
    let mut spec =
        ModuleNodeSpec::new_extract(circuit, input_specs.clone(), spec_name, require_all_inputs)?;
    if let Some(pref) = &prefix_to_strip {
        spec = spec.map_circuit_unwrap(
            |x| {
                if let Some(name) = x.name() {
                    x.clone()
                        .rename(Some(name.strip_prefix(pref).unwrap_or(name).to_owned()))
                } else {
                    x
                }
            },
            None,
        )
    }
    ModuleNode::try_new(
        spec.input_specs
            .iter()
            .map(|x| input_specs.iter().find(|z| &z.1 == x).unwrap().0.clone())
            .collect(),
        spec,
        module_name,
    )
}
