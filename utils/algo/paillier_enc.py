import phe as paillier
import numpy as np
from numpy.typing import ArrayLike


class Paillier:

    public_key: paillier.PaillierPublicKey
    private_key: paillier.PaillierPrivateKey

    def __init__(self, keysize=1024) -> None:
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=keysize)

    def encrypt(self, value: int, r: int | None = None):
        """Encrypt using the public key"""
        encrypted = self.public_key.encrypt(value=value, precision=1, r_value=r)
        return encrypted

    def decrypt(self, encrypted):
        """Decrypt using the private key"""
        decrypted = self.private_key.decrypt(encrypted)
        return decrypted

    def encrypt_block(self, block: ArrayLike, r: int | None = None) -> ArrayLike:
        """Encrypt a block of data"""
        return np.array([self.encrypt(val, r) for val in block])

    def decrypt_block(self, block: ArrayLike) -> ArrayLike:
        """Decrypt a block of data"""
        return np.array([self.decrypt(val) for val in block])


if __name__ == "__main__":
    p = Paillier()
    val = np.random.randint(1, 100000000)
    enc = p.encrypt(val)
    dec = p.decrypt(enc)

    print(f"Original: {val}")
    print(f"Encrypted: {enc.ciphertext()}")
    print(f"Decrypted: {dec}")
