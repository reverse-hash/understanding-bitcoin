import unittest

from parameterized import parameterized

from understandingbitcoin.hash.sha256 import Sha256


class TestSha256(unittest.TestCase):

    """Unit test for the Sha256 class"""

    @parameterized.expand([
        ('empty string', '', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
        ('only ascii', 'Satoshi Nakamoto', 'a0dc65ffca799873cbea0ac274015b9526505daaaed385155425f7337704883e'),
        ('special chars', 'a¢€𐍈', '9b62a241948066df20ae4a3d66f1e63d2bd8104fd718210500e9ca5ebe41be3b'),
        ('long string',
         'If you don\'t believe it or don\'t get it, I don\'t have the time to try to convince you, sorry.',
         '84bb3fe2326a00fb1be1f248d18e62b7279c6683f8f2c230ceaf626ceb9d853b'),
    ])
    def test_equals(self, _, message, digest):
        message_bytes = bytearray(message, 'utf-8')

        actual_result: str = Sha256.hash(message_bytes).hex()

        self.assertEqual(digest, actual_result)
