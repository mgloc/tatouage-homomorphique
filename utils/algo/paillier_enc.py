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

    def encrypt_nparray(self, block: ArrayLike, r: int | None = None) -> ArrayLike:
        """Encrypt data in np_array using the public key, it can be nested"""
        if isinstance(block[0], np.ndarray):
            return np.array([self.encrypt_nparray(b, r) for b in block])
        return np.array([self.encrypt(b, r) for b in block])

    def decrypt_nparray(self, block: ArrayLike) -> ArrayLike:
        """Decrypt data in np_array using the private key, it can be nested"""
        if isinstance(block[0], np.ndarray):
            return np.array([self.decrypt_nparray(b) for b in block])
        return np.array([self.decrypt(b) for b in block])


def test():
    p = Paillier()

    print("--------------------\nTest Classic\n--------------------")
    val = np.random.randint(1, 100, 5)
    enc = p.encrypt_nparray(val)
    dec = p.decrypt_nparray(enc)

    print(f"Original: {val}")
    print(f"Decrypted: {dec}")

    print("--------------------\nTest Homomorphic property\n--------------------")

    val1 = np.random.randint(1, 100, 5)
    val2 = np.random.randint(1, 100, 5)
    enc1 = p.encrypt_nparray(val1)
    enc2 = p.encrypt_nparray(val2)

    enc = enc1 + enc2
    dec = p.decrypt_nparray(enc)

    print(f"Val1: {val1}, Val2: {val2}, Val1 + Val2: {val1 + val2}")
    print(f"Dec[Enc[Val1]*Enc[Val2]]: {dec}")


if __name__ == "__main__":
    test()
