# Objets abstraits pour les structures de données
import numpy as np
from numpy.typing import ArrayLike

from utils.func import QIM

class Vector:
    vector_size:int
    block_size:int

    _blocks:list[ArrayLike] = []

    def __init__(self, vector_size:int, block_size:int, blocks: list[ArrayLike] = []):
        self.vector_size = vector_size
        self.block_size = block_size
        self._blocks = blocks

    def set_blocks(self, blocks: list[ArrayLike]):
        self._blocks = blocks

    def premark(self,mark:ArrayLike):
        if mark.size != self.block_size :
            raise ValueError("The mark size should be the same than the vector block size")
        
        qim = QIM(delta=1)
        for i,block in enumerate(self._blocks):
            self._blocks[i] = qim.modulate(m=block, b=mark)


class EncryptedVector:
    vector:Vector
    def __init__(self, vector:Vector):
        self.vector = vector
