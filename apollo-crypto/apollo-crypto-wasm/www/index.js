import { ElGamal, KeyGenerator } from "apollo-crypto";

const elgamal = ElGamal.new();
const keyGenerator = KeyGenerator.new();
const keys = keyGenerator.generate();
const [p0, p1] = elgamal.generate_plaintexts().split(',');
const [c1, c2] = elgamal.encrypt(keys.public_key(), p0).split(',');
console.log(c1);
console.log(c2);
const decrypted = elgamal.decrypt(keys.secret_key(), c1, c2);
console.log(decrypted === p0);
