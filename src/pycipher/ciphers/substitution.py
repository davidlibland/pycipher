"""Mono-alphabetic substitution ciphers"""
from pycipher.ciphers.abstract import Cipher

UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
assert len(UPPERCASE_LETTERS) == 26


class SubstitutionCipher(Cipher):
    """Monoalphabetic substitution cipher"""

    def __init__(self, shuffled_alphabet: str):
        shuffled_alphabet = shuffled_alphabet.upper()
        if set(shuffled_alphabet) != set(UPPERCASE_LETTERS):
            raise ValueError(
                "The provided alphabet does not match the standard letters"
            )
        if len(shuffled_alphabet) != len(UPPERCASE_LETTERS):
            raise ValueError("The provided alphabet is not unique")
        self.encoding_dict = {
            let1: let2
            for let1, let2 in zip(UPPERCASE_LETTERS, shuffled_alphabet)
        }
        self.decoding_dict = {
            let1: let2
            for let1, let2 in zip(shuffled_alphabet, UPPERCASE_LETTERS)
        }

    def encode(self, text: str) -> str:
        text = text.upper()
        output = []
        for letter in text:
            output.append(self.encoding_dict.get(letter, letter))
        return "".join(output)

    def decode(self, text: str) -> str:
        text = text.upper()
        output = []
        for letter in text:
            output.append(self.decoding_dict.get(letter, letter))
        return "".join(output)
