use curve25519_dalek::constants;
use curve25519_dalek::edwards::{EdwardsPoint, CompressedEdwardsY};
use curve25519_dalek::scalar::Scalar;

pub struct PublicKey {
    pub pk: EdwardsPoint
}

pub struct SecretKey {
    pub sk: Scalar
}

pub struct KeyPair {
    pub pk: PublicKey,
    pub sk: SecretKey,
}

pub struct KeyGenerator {
    g: EdwardsPoint,
}

impl KeyGenerator {
    pub fn new() -> KeyGenerator {
        KeyGenerator {
            g: constants::ED25519_BASEPOINT_POINT,
        }
    }

    pub fn generate(&self) -> KeyPair {
        let mut csprng = rand::thread_rng();
        let sk = Scalar::random(&mut csprng);
        let pk = self.g * sk;
        KeyPair {
            sk: SecretKey { sk },
            pk: PublicKey { pk }
        }
    }
}

pub struct ElGamal {}

impl ElGamal {
    pub fn new() -> ElGamal {
        ElGamal {}
    }

    pub fn generate_plaintexts(&self) -> (EdwardsPoint, EdwardsPoint) {
        let g = constants::ED25519_BASEPOINT_POINT;
        (
            g,
            g + g,
        )
    }

    pub fn encrypt(&self, pk: &PublicKey, message: EdwardsPoint) -> (EdwardsPoint, EdwardsPoint) {
        let g = constants::ED25519_BASEPOINT_POINT;
        let mut csprng = rand::thread_rng();

        let y = Scalar::random(&mut csprng);
        let s = pk.pk * y;
        let c1 = g * y;
        let c2 = message + s;
        (c1, c2)
    }

    pub fn decrypt(&self, sk: &SecretKey, (c1, c2): (EdwardsPoint, EdwardsPoint)) -> EdwardsPoint {
        let s = c1 * sk.sk;
        let message = c2 - s;
        message
    }
}

pub trait Base64 {
    fn b64_serialize(&self) -> String;
    fn b64_deserialize(data: &str) -> Self;
}

impl Base64 for EdwardsPoint {
    fn b64_serialize(&self) -> String {
        base64::encode(self.compress().as_bytes())
    }

    fn b64_deserialize(data: &str) -> Self {
        CompressedEdwardsY::from_slice(base64::decode(data).unwrap().as_slice()).decompress().unwrap()
    }
}

impl Base64 for Scalar {
    fn b64_serialize(&self) -> String {
        base64::encode(self.as_bytes())
    }

    fn b64_deserialize(data: &str) -> Self {
        let mut bytes = [0_u8; 32];
        bytes.copy_from_slice(base64::decode(data.as_bytes()).unwrap().as_slice());
        Self::from_bytes_mod_order(bytes)
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encrypt_decrypt() {
        let mut csprng = rand::thread_rng();
        let g = constants::ED25519_BASEPOINT_POINT;
        let key_gen = KeyGenerator::new();
        let key_pair = key_gen.generate();
        let elgamal = ElGamal::new();

        let message = g * Scalar::random(&mut csprng);
        let cipher = elgamal.encrypt(&key_pair.pk, message);

        let decrypted = elgamal.decrypt(&key_pair.sk, cipher);
        assert_eq!(message, decrypted);
    }
}
