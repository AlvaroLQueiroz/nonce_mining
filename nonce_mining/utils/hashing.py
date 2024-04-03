import uuid
from hashlib import sha256
import random


def gen_nonce() -> str:
    """Generates a nonce
    Returns:
        str: A new nonce

    Note: You can change the mining difficult changing this function.
    """
    return str(random.randint(0, 10))
    # return str(random.randint(0, 100000))
    # return uuid.uuid4().hex


def gen_hash(nonce: str) -> str:
    """Creates a sha256 hash from the input string and return the hex representation.
    Returns:
        str: The hex representation of the hash on the input
    """
    return sha256(nonce.encode()).digest().hex()
