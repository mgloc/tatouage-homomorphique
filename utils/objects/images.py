# Contient tout ce qui touche à l'édition d'image
import numpy as np
from numpy.typing import ArrayLike

from PIL import Image

from utils.objects.vector import Vector


def get_image(path: str) -> Image:
    """Returns an image from a path"""
    return Image.open(path)


def image_to_nparray(image: Image) -> ArrayLike:
    """Converts an image to an np array"""
    return np.array(image.convert("L"))


def nparray_to_image(array: ArrayLike) -> Image:
    """Converts an np array to an image"""
    array = np.clip(array, 0, 255)
    return Image.fromarray(array, mode="L")


def image_to_vector(image: Image) -> Vector:
    """Converts an image to a vector"""
    return Vector(blocks=image_to_nparray(image))


def vector_to_image(vector: Vector) -> Image:
    """Converts a vector to an image"""
    return nparray_to_image(vector.get_array())


def test():
    img = Image.open("assets/lena.jpg")

    # Test image to nparray
    img_arr = image_to_nparray(img)
    print(img_arr)
    img = nparray_to_image(img_arr)
    # img.show()


if __name__ == "__main__":
    test()
