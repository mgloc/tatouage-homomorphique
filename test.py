import numpy as np
from numpy.typing import ArrayLike
from utils.objects.vector import Vector
from utils.objects.images import image_to_vector, vector_to_image, get_image
from utils.algo.paillier_enc import Paillier


# pylint: disable=protected-access


class VectorTest:
    vector: Vector
    paillier: Paillier

    block_size: int
    block_number: int
    random_premark: ArrayLike

    def __init__(self) -> None:
        self.block_size = 3
        self.block_number = 10
        self.random_premark = np.random.randint(0, 2, self.block_size)

        self.vector = Vector(
            np.random.randint(0, 255, self.block_number * self.block_size).reshape(self.block_number, self.block_size)
        )

        self.paillier = Paillier(keysize=300)

        self.test1()
        self.test2()
        self.test3()

    def test1(self):
        print("--TEST 1--")
        print(self.random_premark)
        print(self.vector._blocks[0])
        self.vector.premark(self.random_premark)
        print("gives")
        print(self.vector._blocks[0])

    def test2(self):
        print("--TEST 2--")
        print(self.vector._blocks[0])
        enc_vector = self.vector.encrypt(self.paillier)
        print([x.ciphertext() for x in enc_vector._blocks[0]])
        vector = enc_vector.decrypt(self.paillier)
        print(vector._blocks[0])

    def test3(self):
        print("--TEST 3--")
        img = get_image("assets/lena.jpg")
        vector_img = image_to_vector(img)
        vector_to_image(vector_img).show()


if __name__ == "__main__":
    VectorTest()
