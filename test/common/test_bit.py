import unittest

from understandingbitcoin.common.bit import BitStream


class TestBitStream(unittest.TestCase):
    """Unit test for the BitStream class"""

    def test_from_bytes(self):
        bytes_value: bytes = bytes.fromhex('09af')

        actual_result: BitStream = BitStream.from_bytes(bytes_value)

        self.assertEqual('100110101111', actual_result)

    def test_from_char(self):
        char: str = 'a'

        actual_result: BitStream = BitStream.from_char(char)

        self.assertEqual('01100001', actual_result)

    def test_from_char2(self):
        char: str = '¢'

        actual_result: BitStream = BitStream.from_char(char)

        self.assertEqual('1100001010100010', actual_result)

    def test_from_char3(self):
        char: str = '€'

        actual_result: BitStream = BitStream.from_char(char)

        self.assertEqual('111000101000001010101100', actual_result)

    def test_from_char4(self):
        char: str = '𐍈'

        actual_result: BitStream = BitStream.from_char(char)

        self.assertEqual('11110000100100001000110110001000', actual_result)

    def test_from_hex(self):
        hex_value: str = 'f731'

        actual_result: BitStream = BitStream.from_hex(hex_value)

        self.assertEqual('1111011100110001', actual_result)

    def test_from_int(self):
        integer: int = 2

        actual_result: BitStream = BitStream.from_int(integer)

        self.assertEqual('10', actual_result)

    def test_from_int_zfill(self):
        integer: int = 2

        actual_result: BitStream = BitStream.from_int(integer, zfill=10)

        self.assertEqual('0000000010', actual_result)

    def test_parse_str(self):
        string: str = '01'

        actual_result: BitStream = BitStream.parse_str(string)

        self.assertEqual('01', actual_result)

    def test_join(self):
        bitstream1: BitStream = BitStream.parse_str('01')
        bitstream2: BitStream = BitStream.parse_str('10')

        actual_result: BitStream = BitStream.join(bitstream1, bitstream2)

        self.assertEqual('0110', actual_result)

    def test_join_one_element(self):
        bitstream: BitStream = BitStream.parse_str('01')

        actual_result: BitStream = BitStream.join(bitstream)

        self.assertEqual('01', actual_result)

    def test_join_empty_tuple(self):
        actual_result: BitStream = BitStream.join(tuple())

        self.assertEqual('', actual_result)

    def test_join_list(self):
        bitstream1 = BitStream.parse_str('01')
        bitstream2 = BitStream.parse_str('10')

        actual_result: BitStream = BitStream.join(bitstream1, bitstream2)

        self.assertEqual('0110', actual_result)

    def test_getitem(self):
        bitstream: BitStream = BitStream.parse_str('01')

        actual_result: BitStream = bitstream[1]

        self.assertEqual('1', actual_result)

    def test_getitem_inverse(self):
        bitstream: BitStream = BitStream.parse_str('01')

        actual_result: BitStream = bitstream[-1]

        self.assertEqual('1', actual_result)

    def test_getitem_slice(self):
        bitstream: BitStream = BitStream.parse_str('0110')

        actual_result: BitStream = bitstream[1:3]

        self.assertEqual('11', actual_result)

    def test_getitem_inverse_slice(self):
        bitstream: BitStream = BitStream.parse_str('0110')

        actual_result: BitStream = bitstream[-2:]

        self.assertEqual('10', actual_result)

    def test_add(self):
        bitstream1: BitStream = BitStream.from_int(1)
        bitstream2: BitStream = BitStream.from_int(2)

        actual_result: BitStream = bitstream1 + bitstream2

        self.assertEqual('11', actual_result)

    def test_add_empty_first(self):
        bitstream1: BitStream = BitStream()
        bitstream2: BitStream = BitStream.from_int(2)

        actual_result: BitStream = bitstream1 + bitstream2

        self.assertEqual('10', actual_result)

    def test_add_empty_second(self):
        bitstream1: BitStream = BitStream.from_int(2)
        bitstream2: BitStream = BitStream()

        actual_result: BitStream = bitstream1 + bitstream2

        self.assertEqual('10', actual_result)

    def test_add_int(self):
        bitstream: BitStream = BitStream.from_int(1)
        integer: int = 2

        actual_result: BitStream = bitstream + integer

        self.assertEqual('11', actual_result)

    def test_add_int_empty(self):
        bitstream: BitStream = BitStream()
        integer: int = 2

        actual_result: BitStream = bitstream + integer

        self.assertEqual('10', actual_result)

    def test_add_str(self):
        bitstream: BitStream = BitStream.from_int(1)
        string: str = '10'

        actual_result: BitStream = bitstream + string

        self.assertEqual('11', actual_result)

    def test_add_str_empty(self):
        bitstream: BitStream = BitStream()
        string: str = '10'

        actual_result: BitStream = bitstream + string

        self.assertEqual('10', actual_result)

    def test_and_large_first(self):
        bitstream1: BitStream = BitStream.parse_str('11100')
        bitstream2: BitStream = BitStream.parse_str('1000')

        actual_result: BitStream = bitstream1 & bitstream2

        self.assertEqual('01000', actual_result)

    def test_and_short_first(self):
        bitstream1: BitStream = BitStream.parse_str('1000')
        bitstream2: BitStream = BitStream.parse_str('11100')

        actual_result: BitStream = bitstream1 & bitstream2

        self.assertEqual('01000', actual_result)

    def test_invert(self):
        bitstream: BitStream = BitStream.parse_str('10')

        actual_result: BitStream = ~bitstream

        self.assertEqual('01', actual_result)

    def test_radd_int(self):
        integer: int = 2
        bitstream: BitStream = BitStream('01')

        actual_result: BitStream = integer + bitstream

        self.assertEqual('11', actual_result)

    def test_radd_int_empty(self):
        integer: int = 2
        bitstream: BitStream = BitStream()

        actual_result: BitStream = integer + bitstream

        self.assertEqual('10', actual_result)

    def test_radd_str(self):
        string: str = '01'
        bitstream: BitStream = BitStream('10')

        actual_result: BitStream = string + bitstream

        self.assertEqual('11', actual_result)

    def test_or_larger_first(self):
        bitstream1: BitStream = BitStream.parse_str('11100')
        bitstream2: BitStream = BitStream.parse_str('1010')

        actual_result: BitStream = bitstream1 | bitstream2

        self.assertEqual('11110', actual_result)

    def test_or_shorter_first(self):
        bitstream1: BitStream = BitStream.parse_str('1010')
        bitstream2: BitStream = BitStream.parse_str('11100')

        actual_result: BitStream = bitstream1 | bitstream2

        self.assertEqual('11110', actual_result)

    def test_xor_larger_first(self):
        bitstream1: BitStream = BitStream.parse_str('11100')
        bitstream2: BitStream = BitStream.parse_str('1010')

        actual_result: BitStream = bitstream1 ^ bitstream2

        self.assertEqual('10110', actual_result)

    def test_xor_shorter_first(self):
        bitstream1: BitStream = BitStream.parse_str('1010')
        bitstream2: BitStream = BitStream.parse_str('11100')

        actual_result: BitStream = bitstream1 ^ bitstream2

        self.assertEqual('10110', actual_result)

    def test_rshift(self):
        bitstream: BitStream = BitStream.parse_str('111')

        actual_result: BitStream = bitstream >> 2

        self.assertEqual('001', actual_result)

    def test_rotate_left(self):
        bitstream: BitStream = BitStream.parse_str('001')

        actual_result: BitStream = bitstream.rotate_left(2)

        self.assertEqual('100', actual_result)

    def test_rotate_left_shifts_greater_than_bitstream_length(self):
        bitstream: BitStream = BitStream.parse_str('001')

        actual_result: BitStream = bitstream.rotate_left(7)

        self.assertEqual('010', actual_result)

    def test_rotate_right_shifts_greater_than_bitstream_length(self):
        bitstream: BitStream = BitStream.parse_str('001')

        actual_result: BitStream = bitstream.rotate_right(7)

        self.assertEqual('100', actual_result)

    def test_mod(self):
        bitstream: BitStream = BitStream.parse_str('10110110')

        actual_result: BitStream = bitstream.mod(5)

        self.assertEqual('10110', actual_result)

    def test_len(self):
        bitstream: BitStream = BitStream.parse_str('01')

        actual_result: int = len(bitstream)

        self.assertEqual(2, actual_result)

    def test_hex_int(self):
        integer: int = 0x0f731

        actual_result: str = BitStream.from_int(integer).hex()

        self.assertEqual('f731', actual_result)

    def test_hex_str(self):
        binary_string: str = '00001000'

        actual_result: str = BitStream.parse_str(binary_string).hex()

        self.assertEqual('08', actual_result)

    def test_hex_empty(self):
        actual_result: str = BitStream().hex()

        self.assertEqual('', actual_result)

    def test_bytes(self):
        hex_value: str = 'f731'

        actual_result: bytes = BitStream.from_hex(hex_value).bytes()

        self.assertEqual(bytes.fromhex(hex_value), actual_result)
