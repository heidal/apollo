import nacl


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
