import numpy as np
from utils.objects.vector import Vector
from utils.algo.paillier_enc import Paillier
from utils.func import binbparray_to_string, string_to_binbparray

# from utils.images import image_to_vector


def main():
    # PARAMETRES
    paillier = Paillier(keysize=300)
    block_size = 56
    block_number = 10

    # PRE-TRAITEMENT
    print("----------------------------")
    print("PRE-TRAITEMENT")
    vector = Vector(np.random.randint(0, 255, block_number * block_size).reshape(block_number, block_size))
    print("Vecteur avant le pre-traitement:", vector.get_block(0)[0:5])

    random_premark = np.random.randint(0, 2, block_size)
    print("Prémarque:", random_premark[0:5])

    vector.premark(random_premark)
    print("Vecteur après le pre-traitement:", vector.get_block(0)[0:5])

    vector.encrypt(paillier)

    # INS1 : INSERTION EN CLAIR
    print("----------------------------")
    print("INS1 : INSERTION EN CLAIR")
    message = "Salut"
    binary_np_msg = string_to_binbparray(message, size=block_size)

    print("Message à insérer:", message)
    print("Message binaire:", binary_np_msg)

    # On créé un vecteur où le le message est répété pour le mettre dans chaque bloc
    vector_msg = Vector(np.tile(binary_np_msg, (1, vector.blocks_number)))
    vector_msg.encrypt(paillier)

    # Insertion du message dans chaque bloc du vecteur
    vector = vector + vector_msg
    print(vector)

    # INS2 : INSERTION CHIFFREE
    # TODO

    # EXT2 : EXTRACTION CHIFFREE
    # TODO

    # EXT1 : EXTRACTION EN CLAIR

    vector.decrypt(paillier)
    print(vector)
    b_ext1 = vector.clear_extract().get_block(0)

    print("----------------------------")
    print("XOR entre premark et b_ext1:")
    print("b_ext1:", b_ext1)
    print("premark:", random_premark)

    b_ext = np.bitwise_xor(random_premark, b_ext1)

    print("\nb_ext:", b_ext)
    print("----------------------------")

    print("Message original:", message)
    print("Message extrait:", binbparray_to_string(b_ext))


if __name__ == "__main__":
    main()
