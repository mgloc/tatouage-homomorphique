# Objets abstraits pour les structures de données
import numpy as np
from numpy.typing import ArrayLike

from utils.algo.qim import QIM
from utils.algo.paillier_enc import Paillier


class VectorBase:
    block_size: int
    blocks_number: int

    _blocks: ArrayLike = np.array(np.array([]))

    def __init__(self, blocks) -> None:
        self._blocks = blocks
        self.block_size = blocks[0]
        self.blocks_number = len(blocks)

    def __add__(self, other):
        if self.block_size != other.block_size or self.blocks_number != other.blocks_number:
            raise ValueError(
                f"The vectors should have the same size and same block size to be added together.\n {self._blocks} + {other._blocks}"
            )

        new_vector = Vector(self._blocks + other._blocks)
        return new_vector

    def get_block(self, block_index: int):
        return self._blocks[block_index]

    def premark(self, mark: ArrayLike):
        if mark.size != self.block_size:
            raise ValueError("The mark size should be the same than the vector block size")

        qim = QIM(delta=1)
        for i in range(self.blocks_number):
            self._blocks[i] = qim.modulate(m=self._blocks[i], b=mark)


class Vector(VectorBase):

    def __repr__(self):
        return f"Vector<{self.block_size}x{self.blocks_number} - {self._blocks}>"

    def clear_extract(self):
        qim = QIM(delta=1)
        new_vector = Vector(np.array([qim.extraction(block) for block in self._blocks]))
        return new_vector

    def encrypt(self, paillier: Paillier) -> VectorBase:
        new_blocks = paillier.encrypt_nparray(self._blocks)
        return VectorEncrypted(new_blocks)


class VectorEncrypted(VectorBase):

    def decrypt(self, paillier: Paillier) -> VectorBase:
        new_blocks = np.array([paillier.decrypt_nparray(self._blocks[i]) for i in range(self.blocks_number)])
        return Vector(new_blocks)
