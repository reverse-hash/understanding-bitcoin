"""Defines common components to operate at byte level."""
from __future__ import annotations

import enum
import string
from abc import ABC, abstractmethod
import abc

from understandingbitcoin.common.bit import BitStream


class ByteOrder(enum.Enum):
    """
    Defines the data ordering types in a digital memory.

    The big-endian (BE) stores the most significant byte (MSB) of a word at the
    smallest memory address and the least significant byte (LSB) at the largest
    memory address. Little-endian (LE) works in the opposite way, it stores the
    most significant byte of a word in the largest memory address and the least
    significant byte at the smallest memory address.
    """
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1


class ByteBuffer:
    """
    Implements a dynamic array of bytes with a higher level of abstraction to
    perform read and write operations.

    The buffer has an unlimited capacity and all write operations are performed
    at the end of the buffer. Read operations are limited to buffer contents
    and can be done through an absolute or relative position.
    """

    @classmethod
    def from_hex(cls, hex_string: str,
                 order: ByteOrder = ByteOrder.BIG_ENDIAN):
        """
        Returns a byte buffer with the given data expressed in a hexadecimal
        string value.

        :param hex_string: The data to store expressed in a hexadecimal string
        value
        :param order: The byte order used for the byte buffer
        :return: The byte buffer
        """
        if not all(c in string.hexdigits for c in hex_string):
            raise ValueError('the given parameter is not a hexadecimal string')

        if len(hex_string) % 2 != 0:
            raise ValueError('the given parameter has an odd number of digits')

        byte_buffer: ByteBuffer = ByteBuffer(order)
        for i in range(0, len(hex_string), 2):
            byte: int = int(hex_string[i:i + 2], 16)
            byte_buffer.put_byte(byte)

        return byte_buffer

    def __init__(self, order: ByteOrder = ByteOrder.BIG_ENDIAN):
        """
        Constructs a byte buffer with the specified byte order.

        :param order: The byte order used for the byte buffer
        """
        self._order: ByteOrder = order
        self._memory: _ByteBufferMemory = self._create_memory(order)

    @staticmethod
    def _create_memory(order: ByteOrder) -> _ByteBufferMemory:
        if ByteOrder.BIG_ENDIAN == order:
            memory = _BigEndianByteBufferMemory()
        else:
            memory = _LittleEndianByteBufferMemory()

        return memory

    def __len__(self) -> int:
        """Returns the number of bytes in the byte buffer."""
        return len(self._memory)

    def __str__(self) -> str:
        """Returns the string binary representation of the byte buffer."""
        return str(self._memory)

    def __getitem__(self, item) -> ByteBuffer:
        """
        Returns a new byte buffer as a subset of this byte buffer.

        :param item: The index or slice of the subset
        :return: The specified byte buffer subset
        """
        if not isinstance(item, int) \
                and not isinstance(item, slice) and item.step is None:
            raise ValueError('the given parameter ist not a valid index or '
                             + 'slice')

        data: BitStream = self._memory[item]
        return ByteBuffer.from_hex(data.hex(), self._order)

    def get_byte(self) -> BitStream:
        """Returns the next relative byte."""
        return self._memory.read(1)

    def get_word16(self) -> BitStream:
        """Returns the next relative 16-bit word."""
        return self._memory.read(2)

    def get_word32(self) -> BitStream:
        """Returns the next relative 32-bit word."""
        return self._memory.read(4)

    def get_word64(self) -> BitStream:
        """Returns the next relative 64-bit word."""
        return self._memory.read(8)

    def get_word128(self) -> BitStream:
        """Returns the next relative 128-bit word."""
        return self._memory.read(16)

    def put_byte(self, byte: int):
        """
        Relative put method to write a byte.

        :param byte: The byte value to write
        """
        if 0 > byte > 255:
            raise ValueError('the given parameter is not between 0 and 255')

        self._memory.write(BitStream.from_unsigned_int(byte, zfill=8))

    def put_word16(self, word: BitStream):
        """
        Relative put method to write a 16-bit word.

        :param word: The 16-bit word to write
        """
        if len(word) != 16:
            raise ValueError('the parameter given is not a 16-bit word')

        self._memory.write(word)

    def put_word32(self, word: BitStream):
        """
        Relative put method to write a 32-bit word.

        :param word: The 32-bit word to write
        """
        if len(word) != 32:
            raise ValueError('the parameter given is not a 32-bit word')

        self._memory.write(word)

    def put_word64(self, word: BitStream):
        """
        Relative put method to write a 64-bit word.

        :param word: The 64-bit word to write
        """
        if len(word) != 64:
            raise ValueError('the parameter given is not a 64-bit word')

        self._memory.write(word)

    def put_word128(self, word: BitStream):
        """
        Relative put method to write a 128-bit word.

        :param word: The 128-bit word to write
        """
        if len(word) != 128:
            raise ValueError('the parameter given is not a 128-bit word')

        self._memory.write(word)

    def hex(self) -> str:
        """Returns a hexadecimal string representation of the byte buffer."""
        return self._memory.hex()

    def bytes(self) -> bytes:
        """Returns an immutable byte array representation of the binary
        buffer. """
        return bytes.fromhex(self.hex())


class _ByteBufferMemory(ABC):
    """Defines an abstract byte buffer memory with common logic."""

    def __init__(self):
        """Constructs a memory and initialize the internal read index."""
        self._index: int = 0
        self._data: BitStream = BitStream()

    def __len__(self) -> int:
        """Returns the size in bytes of the data stored ."""
        return len(self._data) // 8

    def __str__(self) -> str:
        """Returns the string binary representation of the data stored."""
        return str(self._data)

    def __getitem__(self, item: int | slice) -> BitStream:
        """
        Returns a binary sequence of the data stored for the specified index
        or slice.

        :param item: The index or slice of the data
        :return: The specified binary sequence of the data
        """
        if not isinstance(item, int) \
                and not (isinstance(item, slice) and item.step is None):
            raise ValueError('the given parameter ist not a valid index or '
                             + 'slice')

        if isinstance(item, int):
            item: slice = slice(item, None)

        start: int = item.start * 8 if isinstance(item.start, int) else None
        stop: int = item.stop * 8 if isinstance(item.stop, int) else None

        return self._data[start:stop]

    def hex(self) -> str:
        return self._data.hex()

    @abstractmethod
    def read(self, num_bytes) -> BitStream:
        pass

    @abstractmethod
    def write(self, data: BitStream):
        pass


class _BigEndianByteBufferMemory(_ByteBufferMemory):

    """Concrete implementation for the big-endian byte buffer memory."""

    def read(self, num_bytes: int) -> BitStream | None:
        """
        Reads the specified number of bytes from the memory.

        :param num_bytes: The number of bytes to read
        """

        if num_bytes < 0:
            raise ValueError('the given parameter is not greater than or '
                             + 'equal to zero')

        if self._index >= len(self._data):
            return BitStream()

        start: int = self._index
        end: int = self._index + (num_bytes * 8)
        self._index += num_bytes * 8

        return self._data[start:end]

    def write(self, data: BitStream):
        """
        Writes the specified data at the end of the memory. The most
        significant byte is stored in the smallest memory address and the
        least significant byte at the largest memory address.

        :param data: The binary sequences to write
        """
        self._data = BitStream.join(self._data, data)


class _LittleEndianByteBufferMemory(_ByteBufferMemory):

    """Concrete implementation for the little-endian byte buffer memory."""

    def read(self, num_bytes: int) -> BitStream:
        """
        Reads the specified number of bytes from the memory.

        :param num_bytes: The number of bytes to read
        """
        if num_bytes < 0:
            raise ValueError('the given parameter is not greater than or '
                             + 'equal to zero')

        if self._index >= len(self._data):
            return BitStream()

        word: str = ''
        for i in range(num_bytes * 8, 0, -8):
            end: int = self._index + i
            start: int = end - 8
            word += str(self._data[start:end])

        self._index += num_bytes * 8

        return BitStream.parse_str(word)

    def write(self, data: BitStream):
        """
        Writes the specified data at the end of the memory. The most
        significant byte is stored in the largest memory address and the least
        significant at the smallest memory address.

        :param data: The binary sequences to write
        """
        word: str = ''
        for i in range(len(data), 0, -8):
            word += str(data[i - 8:i])

        self._data = BitStream.join(self._data, word)
