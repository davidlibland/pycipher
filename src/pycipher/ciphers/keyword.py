"""Keyword transposition ciphers"""
import random
from string import ascii_uppercase, punctuation

import numpy as np

from pycipher.ciphers.abstract import Cipher


class KeywordCipher(Cipher):
    """keyword transposition cipher"""

    def __init__(self, keyword: str):
        if len(set(keyword)) != len(keyword):
            raise ValueError("Keyword must have unique letters.")
        self.shuffled_ixs = np.argsort(list(keyword))
        self.unshuffled_ixs = np.argsort(self.shuffled_ixs)

    def encode(self, text: str) -> str:
        text = text.upper()
        text = [x for x in text if x in ascii_uppercase+punctuation]
        while len(text) % len(self.shuffled_ixs):
            text.append(random.choice(ascii_uppercase))
        ixs = np.arange(len(text)).reshape([-1, len(self.shuffled_ixs)])
        chunks = []
        for ix in self.shuffled_ixs:
            jxs = ixs[:, ix]
            chunk = "".join([text[j] for j in jxs])
            chunks.append(chunk)
        return " ".join(chunks)

    def decode(self, text: str) -> str:
        chunks = text.split(" ")
        text = "".join(chunks)
        ixs = np.arange(len(text)).reshape([-1, len(self.shuffled_ixs)])
        ixs = ixs[:, self.shuffled_ixs]
        letters = []
        for ix in np.argsort(ixs.T.flatten()):
            letters.append(text[ix])
        return "".join(letters)
