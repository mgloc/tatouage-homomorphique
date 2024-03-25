# Objets abstraits pour les structures de données
import random

import numpy as np
from numpy.typing import ArrayLike

from utils.algo.qim import QIM
from utils.algo.paillier_enc import Paillier


class VectorBase:
    block_size: int
    blocks_number: int

    _blocks: ArrayLike = np.array(np.array([]))

    def __init__(self, blocks) -> None:
        # type check blocks
        if not isinstance(blocks, np.ndarray) or not isinstance(blocks[0], np.ndarray):
            raise ValueError("The blocks should be a numpy array of numpy arrays.")

        self._blocks = blocks
        self.block_size = len(blocks[0])
        self.blocks_number = len(blocks)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.block_size}x{self.blocks_number} - {(self._blocks.__repr__() [:50] + '..') if len(self._blocks.__repr__() ) > 75 else self._blocks.__repr__() }>"

    def __add__(self, other):
        if self.block_size != other.block_size or self.blocks_number != other.blocks_number:
            raise ValueError(
                f"""The vectors should have the same size and same block size to be added together.
                Vector 1 : {self} +
                Vector 2 : {other}"""
            )

        new_vector = self.__class__(self._blocks + other._blocks)
        return new_vector

    def get_block(self, block_index: int, ciphertext: bool = False):
        if ciphertext:
            print("Warning: The block is not encrypted, returning the plaintext block.")
        return self._blocks[block_index]

    def premark(self, mark: ArrayLike):
        if mark.size != self.block_size:
            raise ValueError("The mark size should be the same than the vector block size")

        qim = QIM(delta=1)
        for i in range(self.blocks_number):
            self._blocks[i] = qim.modulate(m=self._blocks[i], b=mark)

    # SubClasses methods

    def encrypt(self, paillier: Paillier):
        raise NotImplementedError

    def decrypt(self, paillier: Paillier):
        raise NotImplementedError

    def ins2(self, paillier: Paillier, message: ArrayLike):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError


class Vector(VectorBase):

    def extract(self):
        qim = QIM(delta=1)
        new_vector = Vector(np.array([qim.extraction(block) for block in self._blocks]))
        return new_vector

    def encrypt(self, paillier: Paillier) -> VectorBase:
        new_blocks = paillier.encrypt_nparray(self._blocks)
        return VectorEncrypted(new_blocks)

    def decrypt(self, *args, **kwargs):
        # pylint: disable=unused-argument
        return self

    def ins2(self, paillier: Paillier, message: ArrayLike):
        return NotImplemented


class VectorEncrypted(VectorBase):

    def encrypt(self, *args, **kwargs):
        # pylint: disable=unused-argument
        return self

    def get_block(self, block_index: int, ciphertext: bool = True):
        return (
            np.array([x.ciphertext() for x in self._blocks[block_index]]) if ciphertext else self._blocks[block_index]
        )

    def extract(self):
        return np.array([x.ciphertext() % 2 for x in self._blocks[0]])

    def ins2(self, paillier: Paillier, message: ArrayLike):
        assert len(message) == self.block_size
        for i in range(self.blocks_number):
            for j in range(self.block_size):
                while self._blocks[i][j].ciphertext() % 2 != message[j]:
                    r_value = random.randint(0, 1e10)
                    self._blocks[i][j] = self._blocks[i][j] + paillier.encrypt(0, r=r_value)

    def decrypt(self, paillier: Paillier) -> VectorBase:
        new_blocks = np.array([paillier.decrypt_nparray(self._blocks[i]) for i in range(self.blocks_number)])
        return Vector(new_blocks)
