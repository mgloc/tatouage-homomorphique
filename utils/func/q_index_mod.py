# Fonctions algorithmiques
import numpy as np
from numpy.typing import ArrayLike




class QIM:
    def __init__(self, delta):
        self.delta = delta

    def modulate(self, m:ArrayLike, b:ArrayLike) -> ArrayLike:
        """
        m is a vector of values to be quantized individually
        b is a binary vector of bits to be embeded
        returns: a quantized vector y
        """
        m = m.astype(int)
        d = self.delta

        y = np.floor(m/d) * d + (np.abs(np.floor(m/d)%2 != b)) * d
        return y.astype(int)
    
    def extraction(self,y:ArrayLike) -> ArrayLike:
        """
        y is the quantized message
        returns: the extracted binary sequence
        """
        d = self.delta
        b = np.floor(y/d)%2
        return b.astype(int)


    def random_mark(self, l):
        """
        returns: a random binary sequence of length l
        """
        return np.random.choice((0, 1), l)

if __name__ == "__main__":
    qim = QIM(delta=1)

    m = np.random.randint(0, 255, 10)
    b = qim.random_mark(10)
    y = qim.modulate(m,b)
    e = qim.extraction(y)


    print(f"Message aléatoire {m}")
    print(f"Marque aléatoire {b}")
    print(f"Resultat QIM {y}")
    print(f"Resultat QIM extraction {e} ")
    print(f"Verif {b == e}")
