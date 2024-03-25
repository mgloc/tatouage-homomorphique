import numpy as np
from numpy.typing import ArrayLike


def string_to_string_bin(string: str) -> str:
    """Renvoie une chaîne de caractères transformée en une chaîne de 0 et 1"""
    return "".join(format(ord(char), "08b") for char in string)


def string_bin_to_string(string: str) -> str:
    """Renvoie une chaîne de 0 et 1 transformée en une chaîne de caractères"""
    return "".join(chr(int(string[i : i + 8], 2)) for i in range(0, len(string), 8))


def string_bin_to_nparray(string: str, size: int | None = None) -> ArrayLike:
    """Renvoie un tableau numpy d'une chaîne composée de 0 et 1 transformée en un tableau
    d'entiers de taille spécifiée. Retourne de taille size quitte à ajouter des 0 si la taille est trop grande."""
    n = len(string)
    if size is None:
        size = n

    for i in range(size):
        if i >= n:
            string += "0"

    return np.array([int(string[i]) for i in range(size)])


def nparray_to_string_bin(array: ArrayLike) -> str:
    """Renvoie un tableau numpy transformé en une chaîne de 0 et 1"""
    return "".join(str(x) for x in array)


def string_to_binbparray(string: str, size: int | None = None) -> ArrayLike:
    """Renvoie un tableau numpy d'une chaîne de caractères transformée en un tableau
    d'entiers de taille spécifiée. Remplit avec des 0 si la taille est trop grande."""
    return string_bin_to_nparray(string_to_string_bin(string), size)


def binbparray_to_string(string: str) -> str:
    """Renvoie un tableau numpy transformé en une chaîne de caractères"""
    return string_bin_to_string(nparray_to_string_bin(string))


def test():
    b_salut = string_to_binbparray("Salut")
    print(b_salut)
    print(binbparray_to_string(b_salut))


if __name__ == "__main__":
    test()
