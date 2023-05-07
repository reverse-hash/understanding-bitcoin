"""Implements the SHA-256 hash function."""
from understandingbitcoin.common.bit import BitStream
from understandingbitcoin.common.byte import ByteBuffer, ByteOrder


class Sha256:
    """
    SHA-256 is a cryptographic hash function that generates a 256-bit
    (32-byte) hash value and is used for digital signatures, data integrity
    checks, and password hashing.
    """

    # size in bytes of a block of data processed in the algorithm
    _BLOCK_SIZE_BYTES: int = 64  # 512 bits
    # size in bytes of the message length
    _MESSAGE_LENGTH_SIZE_BYTES: int = 8  # 64 bits
    # size in bits of a word in the algorithm
    _WORD_SIZE_BITS: int = 32  # 4 bytes

    # constant values used to initialize the eight 32-bit registers required
    # in the hashing process
    _H: tuple[8] = (
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c,
        0x1f83d9ab, 0x5be0cd19)

    # constants values used in addition to nonlinear functions in the
    # compression step to mix the processed data in a different way
    _K: tuple[64] = (
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
        0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
        0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
        0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
        0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)

    @classmethod
    def hash(cls, message: bytes) -> bytes:
        """
        Returns a 256-bit (32-byte) hash value in bytes using the SHA-256
        algorithm for the given message.

        :param message: The message to be hashed.
        :return: The SHA-256 hash value in bytes.
        """
        # message is extended so that the total length of the message is a
        # multiple of 512 bits
        extended_message: ByteBuffer = cls._extend_message(message)

        # extended message is divided into blocks of 512 bits
        blocks: tuple = cls._split_extended_message(extended_message)

        # hash values are initialized with the precalculated values in H
        hash_values: list[8] = cls._init_hash()

        # each block is processed separately using a compression function, and
        # the output of each block is used to update the hash values
        block: ByteBuffer
        for block in blocks:
            # block is divided into 16 32-bit words and expanded to 64 32-bit
            # words
            words: tuple[64] = cls._expand_block(block)

            # words are processed through a series of rounds
            block_output: tuple[8] = cls._compress_words(hash_values, words)

            # hash values are updated using the output of each block
            cls._update_hash(hash_values, block_output)

        # final hash output is generated once all blocks of the message have
        # been processed
        return cls._generate_digest(hash_values)

    @classmethod
    def _extend_message(cls, message: bytes) -> ByteBuffer:
        # copy the message into the buffer
        extended_message: ByteBuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        byte: int
        for byte in message:
            extended_message.put_byte(byte)

        # padding is performed with a single bit '1' appended to the message
        # and k bytes 0x00 so that the length in bits of the padded message
        # becomes congruent to 448, modulo 512
        extended_message.put_byte(0x80)
        k: int = cls._BLOCK_SIZE_BYTES - ((len(message)
                                           + 1  # byte added previously
                                           + cls._MESSAGE_LENGTH_SIZE_BYTES)
                                          % cls._BLOCK_SIZE_BYTES)
        for _ in range(k):
            extended_message.put_byte(0x00)

        # length in bits of the message represented in 64-bit is appended at
        # the end completing a multiple of 512 bits
        message_length = BitStream.from_unsigned_int(len(message) * 8,
                                                     zfill=64)
        extended_message.put_word64(message_length)

        return extended_message

    @classmethod
    def _split_extended_message(cls, extended_message: ByteBuffer) -> tuple:
        blocks: list = []
        num_blocks: int = len(extended_message) // cls._BLOCK_SIZE_BYTES
        for i in range(num_blocks):
            block_start: int = i * cls._BLOCK_SIZE_BYTES
            block_end: int = block_start + cls._BLOCK_SIZE_BYTES
            block: ByteBuffer = extended_message[block_start:block_end]
            blocks.append(block)

        return tuple(blocks)

    @classmethod
    def _init_hash(cls) -> list[8]:
        init_hash = []
        n: int
        for n in cls._H:
            value = BitStream.from_unsigned_int(n, cls._WORD_SIZE_BITS)
            init_hash.append(value)

        return init_hash

    @classmethod
    def _expand_block(cls, block: ByteBuffer) -> tuple[64]:
        # create a 64 entry list
        words: list[64] = [None] * 64

        # w[0..15] is a copy of the block
        i: int
        for i in range(16):
            words[i] = block.get_word32()

        # the rest w[16..63] expand the first 16 words to complete the 48 words
        for i in range(16, 64):
            words[i] = (words[i - 16] + cls._σ0(words[i - 15]) + words[i - 7]
                        + cls._σ1(words[i - 2])).mod(cls._WORD_SIZE_BITS)

        return tuple(words)

    @classmethod
    def _compress_words(cls, hash_values: list[8], words: tuple[64]) -> tuple:
        # unpack and copy current hash values
        (a, b, c, d, e, f, g, h) = hash_values

        # compresses the chunk in a loop of 64 iterations
        for i in range(64):
            t1 = h + cls._Σ1(e) + cls._choice(e, f, g) + cls._K[i] + words[i]
            t2 = cls._Σ0(a) + cls._majority(a, b, c)
            h = g
            g = f
            f = e
            e = (d + t1).mod(cls._WORD_SIZE_BITS)
            d = c
            c = b
            b = a
            a = (t1 + t2).mod(cls._WORD_SIZE_BITS)

        return a, b, c, d, e, f, g, h

    @staticmethod
    def _σ0(x: BitStream) -> BitStream:
        return x.rotate_right(7) ^ x.rotate_right(18) ^ x >> 3

    @staticmethod
    def _σ1(x: BitStream) -> BitStream:
        return x.rotate_right(17) ^ x.rotate_right(19) ^ x >> 10

    @staticmethod
    def _Σ0(x: BitStream) -> BitStream:
        return x.rotate_right(2) ^ x.rotate_right(13) ^ x.rotate_right(22)

    @staticmethod
    def _Σ1(x: BitStream) -> BitStream:
        return x.rotate_right(6) ^ x.rotate_right(11) ^ x.rotate_right(25)

    @staticmethod
    def _choice(x: BitStream, y: BitStream, z: BitStream) -> BitStream:
        return (x & y) ^ (~x & z)

    @staticmethod
    def _majority(x: BitStream, y: BitStream, z: BitStream) -> BitStream:
        return (x & y) ^ (x & z) ^ (y & z)

    @classmethod
    def _update_hash(cls, hash_values: list[8], block_output: tuple):
        (a, b, c, d, e, f, g, h) = block_output

        # update hash values with the compressed chuck
        hash_values[0] = (hash_values[0] + a).mod(cls._WORD_SIZE_BITS)
        hash_values[1] = (hash_values[1] + b).mod(cls._WORD_SIZE_BITS)
        hash_values[2] = (hash_values[2] + c).mod(cls._WORD_SIZE_BITS)
        hash_values[3] = (hash_values[3] + d).mod(cls._WORD_SIZE_BITS)
        hash_values[4] = (hash_values[4] + e).mod(cls._WORD_SIZE_BITS)
        hash_values[5] = (hash_values[5] + f).mod(cls._WORD_SIZE_BITS)
        hash_values[6] = (hash_values[6] + g).mod(cls._WORD_SIZE_BITS)
        hash_values[7] = (hash_values[7] + h).mod(cls._WORD_SIZE_BITS)

    @staticmethod
    def _generate_digest(hash_values: list[8]) -> bytes:
        digest: ByteBuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        value: BitStream
        for value in hash_values:
            digest.put_word32(value)

        return digest.bytes()
