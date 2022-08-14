import unittest

from parameterized import parameterized

from understandingbitcoin.common.bit import BitStream
from understandingbitcoin.common.byte import ByteBuffer, ByteOrder


class TestByteBuffer(unittest.TestCase):

    """Unit test for the ByteBuffer class"""

    def test_from_hex_big_endian(self):
        byte_buffer = ByteBuffer.from_hex('09af', order=ByteOrder.BIG_ENDIAN)

        actual_result: str = byte_buffer.hex()

        self.assertEqual('09af', actual_result)

    def test_from_hex_little_endian(self):
        byte_buffer = ByteBuffer.from_hex('09af',
                                          order=ByteOrder.LITTLE_ENDIAN)

        actual_result: str = byte_buffer.hex()

        self.assertEqual('09af', actual_result)

    def test_len(self):
        byte_buffer = ByteBuffer.from_hex('09af')

        actual_result: int = len(byte_buffer)

        self.assertEqual(2, actual_result)

    def test_str(self):
        byte_buffer = ByteBuffer.from_hex('09af')

        actual_result: str = str(byte_buffer)

        self.assertEqual('0000100110101111', actual_result)

    def test_getitem(self):
        byte_buffer = ByteBuffer.from_hex('09af')

        actual_result: str = byte_buffer[1].hex()

        self.assertEqual('af', actual_result)

    def test_getitem_inverse(self):
        byte_buffer = ByteBuffer.from_hex('09af')

        actual_result: str = byte_buffer[-1].hex()

        self.assertEqual('af', actual_result)

    def test_getitem_slice(self):
        byte_buffer = ByteBuffer.from_hex('aabbccdd')

        actual_result: str = byte_buffer[1:3].hex()

        self.assertEqual('bbcc', actual_result)

    def test_get_byte(self):
        byte_buffer = ByteBuffer.from_hex('aabb')

        actual_result: str = byte_buffer.get_byte().hex()

        self.assertEqual('aa', actual_result)

    def test_get_byte_relative(self):
        byte_buffer = ByteBuffer.from_hex('aabb')
        byte_buffer.get_byte()

        actual_result: str = byte_buffer.get_byte().hex()

        self.assertEqual('bb', actual_result)

    @parameterized.expand([
        ('big-endian byte buffer', ByteOrder.BIG_ENDIAN),
        ('little-endian byte buffer', ByteOrder.LITTLE_ENDIAN),
    ])
    def test_get_byte_no_data(self, _, order: ByteOrder):
        byte_buffer = ByteBuffer.from_hex('aa', order=order)
        byte_buffer.get_byte()

        actual_result: str = byte_buffer.get_byte()

        self.assertEqual('', actual_result)

    def test_get_word16_big_endian(self):
        byte_buffer = ByteBuffer.from_hex('aabb', order=ByteOrder.BIG_ENDIAN)

        actual_result: str = byte_buffer.get_word16().hex()

        self.assertEqual('aabb', actual_result)

    def test_get_word16_big_endian_relative(self):
        hex32 = 'aabbccdd'
        byte_buffer = ByteBuffer.from_hex(hex32, order=ByteOrder.BIG_ENDIAN)
        byte_buffer.get_word16()

        actual_result: str = byte_buffer.get_word16().hex()

        self.assertEqual('ccdd', actual_result)

    def test_get_word16_little_endian(self):
        hex16 = 'aabb'
        byte_buffer = ByteBuffer.from_hex(hex16, order=ByteOrder.LITTLE_ENDIAN)

        actual_result: str = byte_buffer.get_word16().hex()

        self.assertEqual('bbaa', actual_result)

    def test_get_word16_little_endian_relative(self):
        hex32 = 'aabbccdd'
        byte_buffer = ByteBuffer.from_hex(hex32, order=ByteOrder.LITTLE_ENDIAN)
        byte_buffer.get_word16()

        actual_result: str = byte_buffer.get_word16().hex()

        self.assertEqual('ddcc', actual_result)

    def test_get_word32_big_endian(self):
        hex32 = 'aabbccdd'
        byte_buffer = ByteBuffer.from_hex(hex32, order=ByteOrder.BIG_ENDIAN)

        actual_result: str = byte_buffer.get_word32().hex()

        self.assertEqual('aabbccdd', actual_result)

    def test_get_word32_big_endian_relative(self):
        hex64 = 'aabbccddeeff0011'
        byte_buffer = ByteBuffer.from_hex(hex64, order=ByteOrder.BIG_ENDIAN)
        byte_buffer.get_word32()

        actual_result: str = byte_buffer.get_word32().hex()

        self.assertEqual('eeff0011', actual_result)

    def test_get_word32_little_endian(self):
        hex32 = 'aabbccdd'
        byte_buffer = ByteBuffer.from_hex(hex32, order=ByteOrder.LITTLE_ENDIAN)

        actual_result: str = byte_buffer.get_word32().hex()

        self.assertEqual('ddccbbaa', actual_result)

    def test_get_word32_little_endian_relative(self):
        hex64 = 'aabbccddeeff0011'
        byte_buffer = ByteBuffer.from_hex(hex64, order=ByteOrder.LITTLE_ENDIAN)
        byte_buffer.get_word32()

        actual_result: str = byte_buffer.get_word32().hex()

        self.assertEqual('1100ffee', actual_result)

    def test_get_word64_big_endian(self):
        hex64 = 'aabbccddeeff0011'
        byte_buffer = ByteBuffer.from_hex(hex64, order=ByteOrder.BIG_ENDIAN)

        actual_result: str = byte_buffer.get_word64().hex()

        self.assertEqual('aabbccddeeff0011', actual_result)

    def test_get_word64_big_endian_relative(self):
        hex128 = 'aabbccddeeff001122334455667788'
        byte_buffer = ByteBuffer.from_hex(hex128, order=ByteOrder.BIG_ENDIAN)
        byte_buffer.get_word64()

        actual_result: str = byte_buffer.get_word64().hex()

        self.assertEqual('22334455667788', actual_result)

    def test_get_word64_little_endian(self):
        hex64 = 'aabbccddeeff0011'
        byte_buffer = ByteBuffer.from_hex(hex64, order=ByteOrder.LITTLE_ENDIAN)

        actual_result: str = byte_buffer.get_word64().hex()

        self.assertEqual('1100ffeeddccbbaa', actual_result)

    def test_get_word64_little_endian_relative(self):
        byte_buffer = ByteBuffer.from_hex('aabbccddeeff001122334455667788',
                                          order=ByteOrder.LITTLE_ENDIAN)
        byte_buffer.get_word64()

        actual_result: str = byte_buffer.get_word64().hex()

        self.assertEqual('88776655443322', actual_result)

    def test_put_byte(self):
        bytebuffer = ByteBuffer()
        bytebuffer.put_byte(0x3f)

        actual_result: str = bytebuffer.hex()

        self.assertEqual('3f', actual_result)

    def test_put_word16_big_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        bytebuffer.put_word16(BitStream.from_unsigned_int(10, zfill=16))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('000a', actual_result)

    def test_put_word16_little_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)
        bytebuffer.put_word16(BitStream.from_unsigned_int(10, zfill=16))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0a00', actual_result)

    def test_put_word32_big_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        bytebuffer.put_word32(BitStream.from_unsigned_int(10, zfill=32))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0000000a', actual_result)

    def test_put_word32_little_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)
        bytebuffer.put_word32(BitStream.from_unsigned_int(10, zfill=32))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0a000000', actual_result)

    def test_put_word64_big_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        bytebuffer.put_word64(BitStream.from_unsigned_int(10, zfill=64))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('000000000000000a', actual_result)

    def test_put_word64_little_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)
        bytebuffer.put_word64(BitStream.from_unsigned_int(10, zfill=64))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0a00000000000000', actual_result)

    def test_put_word128_big_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
        bytebuffer.put_word128(BitStream.from_unsigned_int(10, 128))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0000000000000000000000000000000a', actual_result)

    def test_put_word128_little_endian(self):
        bytebuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)
        bytebuffer.put_word128(BitStream.from_unsigned_int(10, 128))

        actual_result: str = bytebuffer.hex()

        self.assertEqual('0a000000000000000000000000000000', actual_result)
