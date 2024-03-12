import numpy as np
from numpy.typing import ArrayLike
from utils.obj import Vector
from utils.algo.paillier_enc import Paillier

# pylint: disable=protected-access


class VectorTest:
    vector: Vector
    paillier: Paillier

    block_size: int
    random_premark: ArrayLike

    def __init__(self) -> None:
        self.block_size = 3
        self.random_premark = np.random.randint(0, 2, self.block_size)

        self.vector = Vector(self.block_size, np.random.randint(1, 10000, 10 * self.block_size))
        self.paillier = Paillier(keysize=300)

        self.test1()
        self.test2()

    def test1(self):
        print("--TEST 1--")
        print(self.random_premark)
        print(self.vector._blocks[0])
        self.vector.premark(self.random_premark)
        print("gives")
        print(self.vector._blocks[0])

    def test2(self):
        print("--TEST 2--")
        self.vector.encrypt(self.paillier)
        print([x.ciphertext() for x in self.vector._blocks[0]])
        self.vector.decrypt(self.paillier)
        print(self.vector._blocks[0])


if __name__ == "__main__":
    VectorTest()
