"""Tests of the ciphers."""
from string import printable, ascii_uppercase, punctuation

from hypothesis import given
from hypothesis import strategies as h_strats

from pycipher.ciphers.keyword import KeywordCipher
from pycipher.ciphers.substitution import UPPERCASE_LETTERS, SubstitutionCipher


@given(
    h_strats.text(alphabet=printable, max_size=20),
    h_strats.permutations(UPPERCASE_LETTERS).map(lambda x: "".join(x)),
)
def test_substitution_cipher(text, alphabet):
    """Replace this with tests of core (not-extras) functionality."""
    cipher = SubstitutionCipher(alphabet)

    encoded_text = cipher.encode(text)
    decoded_text = cipher.decode(encoded_text)

    assert decoded_text == text.upper()


@given(
    h_strats.text(alphabet=ascii_uppercase + punctuation, max_size=50),
    h_strats.lists(
        h_strats.sampled_from(UPPERCASE_LETTERS),
        unique=True,
        max_size=7,
        min_size=1,
    ).map(lambda x: "".join(x)),
)
def test_keyword_cipher(text, keyword):
    """Replace this with tests of core (not-extras) functionality."""
    cipher = KeywordCipher(keyword)

    encoded_text = cipher.encode(text)
    decoded_text = cipher.decode(encoded_text)

    assert decoded_text[: len(text)] == text.upper()


def test_keyword_cipher_simple():
    """Replace this with tests of core (not-extras) functionality."""
    text = "meetmynigeaxthtdsruh"
    keyword = "frank"
    cipher = KeywordCipher(keyword)

    encoded_text = cipher.encode(text)

    assert encoded_text == "EITR MYAD METH TGHU ENXS"

    decoded_text = cipher.decode(encoded_text)

    assert decoded_text == text.upper()
