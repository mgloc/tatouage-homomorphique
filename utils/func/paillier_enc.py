import phe as paillier

class Paillier:

    public_key: paillier.PaillierPublicKey
    private_key: paillier.PaillierPrivateKey

    def __init__(self, keysize=1024) -> None:
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=keysize)

    def encrypt(self, value:int, r:int) :
        encrypted = self.public_key.encrypt(value=value,r_value=r)
        return

    def decrypt(self,encrypted):
        pass

class EncryptedNumber:
    value: paillier.EncryptedNumber
    alea: int
