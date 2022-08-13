"""Defines common components to operate at bit level."""
from __future__ import annotations

import string


class BitStream:

    """Implements an immutable binary sequence, backed by a string
    representation.

    Note that this is not the most efficient way to implement such class, but
    for didactic and debugging purposes, it is a very convenient and
    user-friendly option.
    """
    BIT_0: str = '0'
    BIT_1: str = '1'

    @classmethod
    def from_bytes(cls, byte_value: bytes) -> BitStream:
        """
        Returns a binary sequence represented by the given array of bytes.

        :param byte_value: The array of bytes to convert
        :return: The binary sequence representation
        """
        return BitStream.from_int(int.from_bytes(byte_value, byteorder='big'))

    @classmethod
    def from_char(cls, char: str) -> BitStream:
        """
        Returns a binary sequence represented by the given UTF-8 character.

        :param char: The UTF-8 character to convert
        :return: The binary sequence representation
        """
        assert len(char) == 1
        char_bytes = bytes(char, 'utf-8')
        num_bits = len(char_bytes) * 8
        return BitStream.from_int(
            int.from_bytes(char_bytes, byteorder='big'), num_bits)

    @classmethod
    def from_hex(cls, hex_string: str) -> BitStream:
        """
        Returns a binary sequence represented by the given hexadecimal
        string.

        :param hex_string: The hexadecimal string to convert
        :return: The binary sequence representation
        """
        assert all(c in string.hexdigits for c in hex_string)
        return BitStream.parse_str(''.join(tuple(
            map(lambda i: str(BitStream.from_int(i, zfill=4)),
                map(lambda h: int(h, 16), hex_string)))))

    @classmethod
    def from_int(cls, integer: int, zfill=0) -> BitStream:
        """
        Returns a binary sequence represented by the given integer number.

        :param integer: The integer number to convert
        :param zfill: Desired length of the binary sequence to be filled with
        leading zeros. If the value of the parameter is less than the length
        of binary representation, no filling is done
        :return: The binary sequence representation
        """
        assert integer >= 0
        return BitStream(format(integer, 'b'), zfill)

    @classmethod
    def parse_str(cls, binary_string: str) -> BitStream:
        """
        Returns a binary sequence represented by the string representation of
        a binary number.

        :param binary_string: The string representation of a binary number
        :return: The binary sequence representation
        """
        return BitStream(binary_string)

    def join(self, *others: BitStream | tuple | list | str):
        """
        Returns a new binary sequence whose value is the binary concatenation
        of this and other.

        :param others: The binary sequences to concatenate
        :return: A new binary sequence with the concatenation of this and the
        given binary sequence binary
        """
        if len(others) == 1 and isinstance(others[0], (list, tuple)):
            others = others[0]

        return BitStream.parse_str(self._value
                                   + ''.join(list(map(str, others))))

    def __init__(self, binary_value: str = '', zfill=0):
        """
        Constructs a binary sequence from a string representation of a
        binary number.

        :param binary_value: The string representation of a binary number
        :param zfill: Desired length of the binary sequence to be filled with
        leading zeros. If the value of the parameter is less than the length
        of binary representation, no filling is done
        """
        assert all(char in (self.BIT_0, self.BIT_1) for char in binary_value)
        self._value: str = binary_value.zfill(zfill)

    def __eq__(self, other: BitStream | str) -> bool:
        """Returns true if the value of this is equal to the value of other."""
        return str(self) == str(other)

    def __len__(self) -> int:
        """Returns the number of bits in the binary sequence."""
        return len(self._value)

    def __str__(self) -> str:
        """Returns the string binary representation of the binary sequence."""
        return self._value

    def __add__(self, other: BitStream | str | int) -> BitStream:
        """
        Returns a new binary sequence whose value is the binary addition of
        this and other.

        :param other: The binary sequence, integer or string representation
        of a binary number to add
        :return: A new binary sequence with the binary addition
        """
        if isinstance(other, (BitStream, str)):
            result: int = int(str(self) or self.BIT_0, 2) \
                          + int(str(other) or self.BIT_0, 2)
            return BitStream.from_int(result, max(len(self), len(other)))

        return BitStream.from_int(int(self._value or self.BIT_0, 2) + other)

    def __and__(self, other: BitStream):
        """
        Returns a new binary sequence whose value is the bitwise AND
        operation of this and other.

        :param other: The binary sequence with which to apply the operation
        :return: A new binary sequence with the result of the operation
        """
        value: str = ''
        num_bits, operand1, operand2 = self._normalize_operands(self, other)
        for i in range(num_bits):
            value += self.BIT_1 if self.BIT_1 == operand1[i] == operand2[i] \
                else self.BIT_0

        return BitStream.parse_str(value)

    @staticmethod
    def _normalize_operands(operand1, operand2) -> tuple:
        num_bits: int = max(len(operand1), len(operand2))
        operand1: str = str(operand1).zfill(num_bits)
        operand2: str = str(operand2).zfill(num_bits)
        return num_bits, operand1, operand2

    def __getitem__(self, item: int | slice) -> BitStream:
        """
        Returns a new binary sequence that is a subset of this binary
        sequence.

        :param item: The index or slice of the subset
        :return: The specified binary sequence subset
        """
        return BitStream.parse_str(self._value[item])

    def __invert__(self):
        """
        Returns a new binary sequence whose value is the bitwise NOT
        operation of this.

        :return: A new binary sequence with the result of the operation
        """
        complement: str = ''
        for bit in self._value:
            complement += self.BIT_1 if bit == self.BIT_0 else self.BIT_0

        return BitStream.parse_str(complement)

    def __or__(self, other: BitStream):
        """
        Returns a new binary sequence whose value is the bitwise OR operation
        of this and other.

        :param other: The binary sequence with which to apply the operation
        :return: A new binary sequence with the result of the operation
        """
        value: str = ''
        num_bits, operand1, operand2 = self._normalize_operands(self, other)
        for i in range(num_bits):
            value += self.BIT_1 if self.BIT_1 in ([operand1[i], operand2[i]]) \
                else self.BIT_0

        return self.parse_str(value)

    def __radd__(self, other: BitStream | str | int):
        """
        Returns a new binary sequence whose value is the binary addition of
        this and other.

        :param other: The binary sequence, integer or string representation of
        a binary number to add
        :return: A new binary sequence with the binary addition
        """
        return self + other

    def __rshift__(self, shifts: int):
        """
        Returns a new binary sequence whose value is the result of shifting to
        the right.

        :param shifts: The number of right shifts to apply
        :return: A new binary sequence with the result of the operation
        """
        assert shifts >= 1
        value: str = self.BIT_0 * min(
            len(self._value), shifts) + self._value[0:-shifts]
        return BitStream.parse_str(value)

    def __xor__(self, other: BitStream):
        """
        Returns a new binary sequence whose value is the bitwise XOR operation
        of this and other.

        :param other: The binary sequence with which to apply the operation
        :return: A new binary sequence with the result of the operation
        """
        value: str = ''
        num_bits, operand1, operand2 = self._normalize_operands(self, other)
        for i in range(num_bits):
            value += self.BIT_1 \
                if [operand1[i], operand2[i]].count(self.BIT_1) == 1 \
                else self.BIT_0

        return self.parse_str(value)

    def mod(self, divisor: int) -> BitStream:
        """
        Returns a new binary sequence whose value is the modulo of this and
        2^n.

        :param divisor: The number of bits with which to calculate the modulo
        :return: A new binary sequence with the result of the operation
        """
        assert divisor >= 1
        return BitStream.parse_str(self._value[-divisor::])

    def rotate_left(self, shifts: int) -> BitStream:
        """
        Returns a new binary sequence whose value is the result of shifting
        a specified number of bits to the left but except that the bits that
        fall off at the beginning are moved back to the end.

        :param shifts: The number of left shifts to apply
        :return: A new binary sequence with the result of the operation
        """
        assert shifts >= 0

        if 0 < len(self) < shifts:
            shifts %= len(self)

        value: str = self._value[shifts:] + self._value[:shifts]
        return self.parse_str(value)

    def rotate_right(self, shifts: int) -> BitStream:
        """
        Returns a new binary sequence whose value is the result of shifting
        a specified number of bits to the right but except that the bits that
        fall off at the end are moved back to the beginning.

        :param shifts: The number of right shifts to apply
        :return: A new binary sequence with the result of the operation
        """
        assert shifts >= 0

        if 0 < len(self) < shifts:
            shifts %= len(self)

        value: str = self._value[len(
            self._value) - shifts:] + self._value[:-shifts]
        return self.parse_str(value)

    def bytes(self) -> bytes:
        """
        Returns an immutable byte array representation of the binary sequence.
        """
        assert len(self) % 8 == 0
        return bytes.fromhex(self.hex())

    def hex(self) -> str:
        """
        Returns a hexadecimal string representation of the binary sequence. """
        return f'{hex(int(self._value, 2))[2:]:0>{len(self._value) // 4}}' \
            if len(self) > 0 else ''
