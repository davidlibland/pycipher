"""Abstract cipher class"""
from abc import ABC, abstractmethod


class Cipher(ABC):
    """An abstract cipher"""

    @abstractmethod
    def encode(self, text: str) -> str:
        """Encoding method"""
        raise NotImplementedError

    @abstractmethod
    def decode(self, text: str) -> str:
        """Decoding method"""
        raise NotImplementedError
