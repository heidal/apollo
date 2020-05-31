import base64
import pytest
from apollo.elections import crypto

pytestmark = pytest.mark.django_db


def test_encrypt_decrypt(opened_election):
    message = base64.b64encode(b"Hello, world!")
    ciphertext = crypto.encrypt(opened_election.public_key, message)
    plaintext = crypto.decrypt(opened_election.secret_key, ciphertext)
    assert plaintext == message.decode('utf-8')


def test_public_key_cannot_be_used_for_decryption(opened_election):
    message = base64.b64encode(b"Hello, world!")
    ciphertext = crypto.encrypt(opened_election.public_key, message)
    with pytest.raises(crypto.CryptoError):
        crypto.decrypt(opened_election.public_key, ciphertext)
