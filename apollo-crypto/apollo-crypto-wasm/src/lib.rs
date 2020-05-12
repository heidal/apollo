extern crate console_error_panic_hook;

mod utils;

use apollo_crypto_core as apollo;
use apollo_crypto_core::Base64;

use wasm_bindgen::prelude::*;
use crate::utils::set_panic_hook;
use curve25519_dalek::edwards::EdwardsPoint;
use curve25519_dalek::scalar::Scalar;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
pub struct KeyPair {
    key_pair: apollo::KeyPair
}

#[wasm_bindgen]
impl KeyPair {
    pub fn public_key(&self) -> String {
        self.key_pair.pk.pk.b64_serialize()
    }

    pub fn secret_key(&self) -> String {
        self.key_pair.sk.sk.b64_serialize()
    }
}

impl Into<apollo::KeyPair> for KeyPair {
    fn into(self) -> apollo::KeyPair {
        self.key_pair
    }
}

impl Into<KeyPair> for apollo::KeyPair {
    fn into(self) -> KeyPair {
        KeyPair { key_pair: self }
    }
}

#[wasm_bindgen]
struct KeyGenerator {
    key_generator: apollo::KeyGenerator
}

#[wasm_bindgen]
impl KeyGenerator {
    pub fn new() -> KeyGenerator {
        KeyGenerator {
            key_generator: apollo::KeyGenerator::new()
        }
    }

    pub fn generate(&self) -> KeyPair {
        self.key_generator.generate().into()
    }
}

#[wasm_bindgen]
pub struct ElGamal {
    el_gamal: apollo::ElGamal
}

#[wasm_bindgen]
impl ElGamal {
    pub fn new() -> ElGamal {
        ElGamal { el_gamal: apollo::ElGamal::new() }
    }

    pub fn generate_plaintexts(&self) -> String {
        let (p0, p1) = self.el_gamal.generate_plaintexts();
        format!("{},{}", p0.b64_serialize(), p1.b64_serialize())
    }

    pub fn encrypt(&self, pk: &str, message: &str) -> String {
        let public_key = apollo::PublicKey { pk: EdwardsPoint::b64_deserialize(pk) };
        let (c1, c2) = self.el_gamal.encrypt(&public_key, EdwardsPoint::b64_deserialize(&message));
        format!("{},{}", c1.b64_serialize(), c2.b64_serialize())
    }

    pub fn decrypt(&self, sk: &str, c1: &str, c2: &str) -> String {
        let secret_key = apollo::SecretKey { sk: Scalar::b64_deserialize(sk) };
        let message = self.el_gamal.decrypt(&secret_key, (EdwardsPoint::b64_deserialize(c1), EdwardsPoint::b64_deserialize(c2)));
        message.b64_serialize()
    }
}
