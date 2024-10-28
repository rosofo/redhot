use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn foo() -> PyResult<String> {
    Ok("hi".to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn redhot(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(foo, m)?)?;
    Ok(())
}
