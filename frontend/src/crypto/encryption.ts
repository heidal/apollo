import { box, randomBytes } from "tweetnacl";
import { decodeBase64, encodeBase64, decodeUTF8 } from "tweetnacl-util";
import blake from "blakejs/blake2b";


function sealedBoxNonce(publicKeySender: Uint8Array, publicKeyReceiver: Uint8Array): Uint8Array {
    const state = blake.blake2bInit(box.nonceLength, null);
    blake.blake2bUpdate(state, publicKeySender);
    blake.blake2bUpdate(state, publicKeyReceiver);
    return blake.blake2bFinal(state);
}

export function encrypt(electionKey: string, message: string): string {
    /**
     * NaCl sealed box encryption
     * see https://libsodium.gitbook.io/doc/public-key_cryptography/sealed_boxes
     */
    const electionKeyDecoded = decodeBase64(electionKey);
    const ephemeralKeyPair = box.keyPair();
    const nonce = sealedBoxNonce(ephemeralKeyPair.publicKey, electionKeyDecoded);

    const encryptedMessage = box(
        decodeUTF8(message),
        nonce,
        electionKeyDecoded,
        ephemeralKeyPair.secretKey
    );

    const ciphertext = new Uint8Array(ephemeralKeyPair.publicKey.length + encryptedMessage.length);
    ciphertext.set(ephemeralKeyPair.publicKey);
    ciphertext.set(encryptedMessage, ephemeralKeyPair.publicKey.length);


    return encodeBase64(ciphertext);
}
