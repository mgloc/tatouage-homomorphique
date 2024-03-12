# Objets abstraits pour les structures de données
import numpy as np
from numpy.typing import ArrayLike

from utils.algo.qim import QIM
from utils.algo.paillier_enc import Paillier


class Vector:
    vector_size: int
    block_size: int

    _blocks: list[ArrayLike] = []

    def __init__(self, block_size: int, values: list):
        self.vector_size = len(values)
        self.block_size = block_size
        self._blocks = self.create_blocks(block_size, values)

    def create_blocks(self, block_size: int, values: list):
        return [np.array(values[i : i + block_size]) for i in range(0, len(values), block_size)]

    def set_blocks(self, blocks: list[ArrayLike]):
        self._blocks = blocks

    def get_block(self, block_index: int):
        return self._blocks[block_index]

    def get_block_ciphertext(self, block_index: int):
        return [x.ciphertext() for x in self._blocks[block_index]]

    def premark(self, mark: ArrayLike):
        if mark.size != self.block_size:
            raise ValueError("The mark size should be the same than the vector block size")

        qim = QIM(delta=1)
        for i, block in enumerate(self._blocks):
            self._blocks[i] = qim.modulate(m=block, b=mark)

    def encrypt(self, paillier: Paillier):
        for i, block in enumerate(self._blocks):
            self._blocks[i] = paillier.encrypt_block(block)

    def decrypt(self, paillier: Paillier):
        for i, block in enumerate(self._blocks):
            self._blocks[i] = paillier.decrypt_block(block)
