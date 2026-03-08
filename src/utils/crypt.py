import msgpack
from Crypto.Cipher import AES

KEY = bytes.fromhex("df384214b29a3adfbf1bd9ee5b16f884")
IV = bytes.fromhex("7e856c907987f8aec6afc0c54738fc7e")


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes, block_size: int) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]


def encrypt(obj: object) -> bytes:
    """Encrypt a Python object: serialize to msgpack, then AES-CBC encrypt."""
    msgpack_buffer = msgpack.packb(obj, use_bin_type=True, use_single_float=True)
    padded = pkcs7_pad(msgpack_buffer, 16)

    algorithm = AES.MODE_CBC
    cipher = AES.new(KEY, algorithm, IV)
    return cipher.encrypt(padded)


def decrypt(buffer: bytes) -> object:
    """Decrypt AES-CBC encrypted msgpack data back to a Python object."""
    algorithm = AES.MODE_CBC
    decipher = AES.new(KEY, algorithm, IV)
    decrypted = decipher.decrypt(buffer)
    unpadded = pkcs7_unpad(decrypted, 16)
    return msgpack.unpackb(unpadded, raw=False)


def parse_buffer(hex_str: str) -> bytes:
    """Parse a space-separated hex string into bytes."""
    return bytes(int(x, 16) for x in hex_str.strip().split())
