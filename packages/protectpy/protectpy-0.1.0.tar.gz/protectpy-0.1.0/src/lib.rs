use envelopers::{ViturKeyProvider, EnvelopeCipher, EncryptedRecord};
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn decrypt(py: Python, ciphertext: String, context: String) -> PyResult<&PyAny> {
    let host = "https://vitur.au.ngrok.io";
    let key_id = "70442f1d-630f-4546-8109-b1e6521860d3";
    let access_token = "token-goes-here".to_string();

    pyo3_asyncio::tokio::future_into_py(py, async {    

        let provider = ViturKeyProvider::new(host.into(), key_id.into(), access_token);
        let cipher: EnvelopeCipher<ViturKeyProvider> = EnvelopeCipher::init(provider);
        let encrypted_record = EncryptedRecord::from_vec(base64::decode(ciphertext).unwrap()).unwrap();

        let decrypted = cipher
            .decrypt_with_context(&encrypted_record, Some(context))
            .await
            .unwrap();

        let result = String::from_utf8(decrypted).unwrap();
        println!("RESULT {:?}", result);

        Ok(result)
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn protectpy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(decrypt, m)?)?;

    Ok(())
}