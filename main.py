import numpy as np
import argparse
from utils.objects.vector import Vector, VectorEncrypted
from utils.objects.images import get_image, image_to_vector, vector_to_image
from utils.algo.paillier_enc import Paillier
from utils.func import binbparray_to_string, string_to_binbparray


def main():
    # STATICS
    paillier = Paillier(keysize=300)

    # ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", type=str, default="This is the biggest msg", help="Message to insert")
    parser.add_argument("--image-path", type=str, default="assets/lena.jpg", help="Image to insert")
    args = parser.parse_args()

    image_path = args.image_path
    message = args.message

    # IMAGE IMPORT
    img = get_image(image_path)
    img_vector = image_to_vector(img)

    block_size = img_vector.block_size
    block_number = img_vector.blocks_number

    binary_np_msg = string_to_binbparray(message, size=block_size)

    # PRE-PROCESSING
    print("----------------------------")
    print("PRE-PROCESSING\n")
    vector = img_vector
    print("Vector extract, before pre-processing:", vector.get_block(0)[0:5])

    random_premark = np.random.randint(0, 2, block_size)
    print("Premark extract:", random_premark[0:5])

    vector.premark(random_premark)
    print("Vector extract, after pre-processing:", vector.get_block(0)[0:5])

    # with open("assets/lena_premark.jpg", "wb") as f: # Save the premarked image
    #     vector_to_image(vector).save(f)

    enc_vector: VectorEncrypted = vector.encrypt(paillier)

    # INS1: PLAINTEXT INSERTION
    print("----------------------------")
    print("INS1: PLAINTEXT INSERTION\n")

    print("Message to insert:", message)
    print("Message to insert (in binary):", binary_np_msg)
    print()

    # Create a vector where the message is repeated to be inserted into each block
    vector_msg = Vector(np.tile(binary_np_msg, (block_number, 1)))  # duplicate the message for each block
    enc_vector_msg: VectorEncrypted = vector_msg.encrypt(paillier)

    # Insert the message into each block of the vector
    enc_vector = enc_vector + enc_vector_msg
    print(f"block[0][0] after INS 1: {enc_vector.get_block(0)[0]}")
    print("Note: Save the encrypted vector to try EXT1 later")

    enc_ins1_vector = enc_vector  # copy to try EXT1

    # INS2: ENCRYPTED INSERTION
    print("----------------------------")
    print("INS2: ENCRYPTED INSERTION\n")
    enc_vector.ins2(paillier, binary_np_msg)
    print(f"block[0][0] after INS 2: {enc_vector.get_block(0)[0]}")

    # EXT2: ENCRYPTED EXTRACTION
    print("----------------------------")
    print("EXT2: ENCRYPTED EXTRACTION\n")
    b_ext2 = enc_vector.extract()

    print("Original message:", message)
    print("Extracted message:", binbparray_to_string(b_ext2))

    # EXT1: PLAINTEXT EXTRACTION
    print("----------------------------")
    print("EXT1: PLAINTEXT EXTRACTION\n")

    ins1_vector = enc_ins1_vector.decrypt(paillier)

    print("Decrypt the encrypted vector from INS1 to try EXT1")
    print(f"Iv^{{pr}}: {ins1_vector.get_block(0)[0:5]}\n")
    ins1_vector_extract = ins1_vector.extract()
    b_ext1 = ins1_vector_extract.get_block(0)

    print("XOR between premark and b_ext1:")
    print("b_ext1 extract:", b_ext1[0:5])
    print("premark extract:", random_premark[0:5])

    b_ext = np.bitwise_xor(random_premark, b_ext1)

    print("\nb_ext (xor result):", b_ext)

    print("Original message:", message)
    print("Extracted message:", binbparray_to_string(b_ext))


if __name__ == "__main__":
    main()
