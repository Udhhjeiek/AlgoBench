
"""
string_generator.py

Generates reproducible string datasets for
Dynamic Programming algorithms, particularly LCS.
"""

import random
import string


# Default character set
DEFAULT_ALPHABET = string.ascii_uppercase


def _validate_length(length):
    """Validate the requested string length."""

    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("Length must be an integer.")

    if length < 0:
        raise ValueError("Length cannot be negative.")


def _validate_alphabet(alphabet):
    """Validate the character alphabet."""

    if not isinstance(alphabet, str):
        raise TypeError("Alphabet must be a string.")

    if not alphabet:
        raise ValueError("Alphabet cannot be empty.")


def generate_random_string(
    length,
    alphabet=DEFAULT_ALPHABET,
    seed=None
):
    """
    Generate a random string.

    Args:
        length: Desired string length.
        alphabet: Characters available for generation.
        seed: Optional seed for reproducibility.

    Returns:
        A randomly generated string.
    """

    _validate_length(length)
    _validate_alphabet(alphabet)

    rng = random.Random(seed)

    return ''.join(
        rng.choice(alphabet)
        for _ in range(length)
    )


def generate_string_pair(
    length,
    alphabet=DEFAULT_ALPHABET,
    seed=None
):
    """
    Generate two independent random strings of equal length.

    Args:
        length: Length of each string.
        alphabet: Characters available for generation.
        seed: Optional seed for reproducibility.

    Returns:
        A tuple containing two random strings.
    """

    _validate_length(length)
    _validate_alphabet(alphabet)

    rng = random.Random(seed)

    text1 = ''.join(
        rng.choice(alphabet)
        for _ in range(length)
    )

    text2 = ''.join(
        rng.choice(alphabet)
        for _ in range(length)
    )

    return text1, text2


def generate_identical_string_pair(
    length,
    alphabet=DEFAULT_ALPHABET,
    seed=None
):
    """
    Generate two identical random strings.

    The LCS of the generated pair equals their length.
    """

    text = generate_random_string(
        length,
        alphabet,
        seed
    )

    return text, text


def generate_no_common_string_pair(
    length,
    seed=None
):
    """
    Generate two strings with no common characters.

    Uppercase and lowercase letters are treated as
    different characters by the LCS algorithms.

    The LCS of the generated pair is always zero.
    """

    _validate_length(length)

    rng = random.Random(seed)

    text1 = ''.join(
        rng.choice(string.ascii_uppercase)
        for _ in range(length)
    )

    text2 = ''.join(
        rng.choice(string.ascii_lowercase)
        for _ in range(length)
    )

    return text1, text2
