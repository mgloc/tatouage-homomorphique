import numpy as np
from utils.obj import Vector
from utils.algo.paillier_enc import Paillier

# from utils.images import image_to_vector


def main():
    # PARAMETRES
    paillier = Paillier(keysize=300)
    block_size = 3

    # PRE-TRAITEMENT
    vector = Vector(block_size, np.random.randint(0, 255, 5 * block_size))
    print("Vecteur avant le pre-traitement:", vector.get_block(0))

    random_premark = np.random.randint(0, 2, block_size)
    print("Valeurs aléatoires pour le pre-traitement:", random_premark)

    vector.premark(random_premark)
    print("Vecteur après le pre-traitement:", vector.get_block(0))

    vector.encrypt(paillier)
    print("Vecteur chiffré avec Paillier:", vector.get_block_ciphertext(0))

    # INS1
    # ...


if __name__ == "__main__":
    main()
