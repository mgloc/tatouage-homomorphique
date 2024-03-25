# Contient tout ce qui touche à l'édition d'image

from PIL import Image
from utils.objects.vector import Vector


def image_to_vector(image: Image, size):
    """Converts an image to vectors"""
    image_height, image_width = image._Size

    for i in range(image_height * image_width // size):
        vector = vector

    return vector
