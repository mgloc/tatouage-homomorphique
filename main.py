import numpy as np
from utils.objects.vector import Vector, VectorEncrypted
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

    enc_vector: VectorEncrypted = vector.encrypt(paillier)

    # INS1 : INSERTION EN CLAIR
    print("----------------------------")
    print("INS1 : INSERTION EN CLAIR\n")
    message = "Salut"
    binary_np_msg = string_to_binbparray(message, size=block_size)

    print("Message à insérer:", message)
    print("Message binaire:", binary_np_msg)
    print()

    # On créé un vecteur où le le message est répété pour le mettre dans chaque bloc
    vector_msg = Vector(np.tile(binary_np_msg, (block_number, 1)))  # duplique le message pour chaque bloc
    enc_vector_msg: VectorEncrypted = vector_msg.encrypt(paillier)

    # Insertion du message dans chaque bloc du vecteur
    enc_vector = enc_vector + enc_vector_msg
    print(f"block[0][0] après INS 1 : {enc_vector.get_block(0)[0]}")

    enc_ins1_vector = enc_vector  # copy to try EXT1

    # INS2 : INSERTION CHIFFREE
    print("----------------------------")
    print("INS2 : INSERTION CHIFFRE\n")
    enc_vector.ins2(paillier, binary_np_msg)
    print(f"block[0][0] après INS 2 : {enc_vector.get_block(0)[0]}")

    # EXT2 : EXTRACTION CHIFFREE
    print("----------------------------")
    print("EXT2 : EXTRACTION CHIFFREE\n")
    b_ext2 = enc_vector.extract()

    print("Message original:", message)
    print("Message extrait:", binbparray_to_string(b_ext2))

    # EXT1 : EXTRACTION EN CLAIR

    print("----------------------------")
    print("EXT1 : EXTRACTION EN CLAIR\n")

    ins1_vector = enc_ins1_vector.decrypt(paillier)
    print(f"Iv^{{pr}} : {ins1_vector.get_block(0)[0:5]}\n")
    b_ext1 = ins1_vector.extract().get_block(0)

    print("XOR entre premark et b_ext1:")
    print("b_ext1:", b_ext1)
    print("premark:", random_premark)

    b_ext = np.bitwise_xor(random_premark, b_ext1)

    print("\nb_ext (xor result):", b_ext)

    print("Message original:", message)
    print("Message extrait:", binbparray_to_string(b_ext))


if __name__ == "__main__":
    main()
