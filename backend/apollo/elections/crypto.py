import nacl.encoding, nacl.public, nacl.exceptions


SEED_BIT_SIZE = 256
SEED_BYTE_SIZE = SEED_BIT_SIZE // 8


class CryptoError(Exception):
    pass


def decrypt(election_secret_key: str, ciphertext: str) -> str:
    encoder = nacl.encoding.Base64Encoder()
    try:
        election_sk = nacl.public.PrivateKey(
            election_secret_key.encode("ascii"), encoder
        )
        sealed_box = nacl.public.SealedBox(election_sk)
        message = sealed_box.decrypt(ciphertext, encoder).decode()
    except (TypeError, nacl.exceptions.CryptoError) as e:
        raise CryptoError from e

    return message


def encrypt(election_public_key: str, message: str) -> str:
    encoder = nacl.encoding.Base64Encoder()
    try:
        election_pk = nacl.public.PublicKey(
            election_public_key.encode("ascii"), encoder
        )
        sealed_box = nacl.public.SealedBox(election_pk)
        ciphertext = sealed_box.encrypt(message, encoder).decode()
    except (TypeError, nacl.exceptions.CryptoError) as e:
        raise CryptoError from e

    return ciphertext
