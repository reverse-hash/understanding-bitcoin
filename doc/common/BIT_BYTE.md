# Common utilities
In order to make it easier for users to learn about the inner workings of Bitcoin, a number of utilities have been developed that allow operations to be performed at the bit and byte level, but presented in a more accessible string format. While this may not be the most optimized approach, it can make it much simpler to debug code and study how these systems function internally.

## BitStream
Implements an immutable binary sequence, backed by a string representation.

Note that this is not the most efficient way to implement such class, but for didactic and debugging purposes, it is a very convenient and user-friendly option.

To create an instance of a bit sequence we can do it in several ways:

```python
# Given a hexadecimal string
BitStream.from_hex('f731') # 1111011100110001

# Given an integer number
BitStream.from_int(2) # 10
BitStream.from_int(2, zfill=8) # 00000010

# Given a UTF-8 character
BitStream.from_char('a') # 01100001

# Given an array of bytes
bytes_value: bytes = bytes.fromhex('f731')
BitStream.from_bytes(bytes_value) # 1111011100110001

# Given a string representation of a binary number
BitStream.parse_str('00001111') # 00001111
```

It is possible to perform common binary operations with a sequence of bits, where the result will be returned in a new instance:

### Additive operation
Sums arithmetically the two binary sequencies.

```python
bitstream1 = BitStream.from_int(1) # 1
bitstream2 = BitStream.from_int(2) # 10
actual_result = bitstream1 + bitstream2 # 11
```

### Bitwise AND operator
Compares each bit of the first operator with the corresponding bit of the second operator. If both bits are 1, the result is 1, otherwise it is 0.

```python
bitstream1 = BitStream.parse_str('11100')
bitstream2 = BitStream.parse_str('1000')
actual_result = bitstream1 & bitstream2 # 01000
```

### Bitwise inclusive OR operator
Compares each bit of the first operator with the corresponding bit of the second operator. If either bit is 1, the result is 1, otherwise it is 0.

```python
bitstream1 = BitStream.parse_str('11100')
bitstream2 = BitStream.parse_str('1010')
actual_result = bitstream1 | bitstream2 # 11110
```

### Bitwise exclusive OR operator
Compares each bit of the first operator with the corresponding bit of the second operator. If only one of the bits is 1, the result is 1, otherwise it is 0.

```python
bitstream1 = BitStream.parse_str('11100')
bitstream2 = BitStream.parse_str('1010')
actual_result = bitstream1 ^ bitstream2 # 10110
```

### Bitwise NOT operator
Inverts the bits of the sequence.

```python
bitstream = BitStream.parse_str('10')
actual_result = ~bitstream # 01
```

### Bitwise left shift operator
Not implemented.

### Bitwise right shift operator
Shifts the bits to the right. Bits shifted out are discarded, completing with zeros to the left.

```python
bitstream = BitStream.parse_str('111')
actual_result = bitstream >> 2 # 001
```

### Bitwise left rotation operation
Shifts the bits to the left in a circular way. Bits shifted out on the left side are inserted on the right side.

```python
bitstream = BitStream.parse_str('001')
actual_result = bitstream.rotate_left(7) # 010
```

### Bitwise right rotation operation
Shifts the bits to the right in a circular way. Bits shifted out on the right side are inserted on the left side.

```python
bitstream = BitStream.parse_str('001')
actual_result = bitstream.rotate_right(7) # 100
```

### Modulo operation
Returns the modulo (remainder of a division) of the sequence and 2^n. Note that the result is a new sequence with n bits from the least significant bit.

```python
bitstream = BitStream.parse_str('10110110')
actual_result = bitstream.mod(5) # 10110
```

### Other operations
Other types of operations are available, such as:

```python
bitstream = BitStream.parse_str('1010111100010010')

# Returns the string value
str(bitstream) # 1010111100010010 (str)

# Returns the number of bits 
len(bitstream) # 16 (int)

# Concatenates and returns a new sequence
other = BitStream.from_hex('01') # 00000001
bitstream.join(other) # 101011110001001000000001 (BitStream)

# Returns the hexadecimal string value
bitstream.hex() # af12 (str)

# Returns an inmmutable byte array
bitstream.bytes() # b'\xaf\x12' (bytes)
```

## ByteBuffer

Implements a dynamic array of bytes with a higher level of abstraction to perform read and write operations.

The buffer has an unlimited capacity and all write operations are performed at the end of the buffer. Read operations are limited to the buffer contents and are performed through a relative position.

The **word** is the unit of data handled by the buffer. This unit is measured in bits (8, 16, 32 and 64) and may vary depending on the type of data to be read or written. The most significant byte (MSB) of  word is the byte with the largest values, in the sense of having the highest weight bits. Additionally, the least significant byte (LSB) refers to the byte with the lower weights.

For example, a 32-bit word containing the unsigned integer in ``2009`` in decimal or ``7D9`` in hexadecimal would look like this:

<!-- \underset{MSB}{\underbrace{00000000}}0000000011110100\underset{LSB}{\underbrace{10100010}} -->
<img src="https://latex.codecogs.com/png.image?\bg_white&space;\underset{MSB}{\underbrace{00000000}}0000000011110100\underset{LSB}{\underbrace{10100010}}"/>

When a word is stored in a memory, such as a buffer, the order in which the bytes are stored is important. In computing, the **endianness** refers to the order in which the sequence of bytes is stored in memory. There are multiple orderings, but the most common and the ones we need to know are the **big-endian (BE)** or **little-endian (LE)**. The first stores the most significant byte (MSB) of a word at the smallest memory address and the least significant byte (LSB) at the largest memory address. The other, stores the most significant byte (MSB) of a word in the largest memory address and the least significant (LSB) at the smallest memory address.

To create an instance of a byte buffer we can do it in several ways:

```python
# An empty one
ByteBuffer(order=ByteOrder.BIG_ENDIAN) # or ByteBuffer() is equivalent

# Given a hexadecimal string to initialize the buffer contents
ByteBuffer.from_hex('f731', ByteOrder.LITTLE_ENDIAN)

# Given an UTF-8 string to initialize the buffer contents
ByteBuffer.from_str('ab',  ByteOrder.LITTLE_ENDIAN)
```

### Write operations

There are multiple methods to write a sequences of bytes in the memory taking into consideration the size of the word to follow the ordering settled in the buffer.

| Operation | Description |
|---|---|
| put_byte | Write a byte/8-bit word at the end of the buffer |
| put_word16 | Write a 16-bit word at the end of the buffer |
| put_word32 | Write a 32-bit word at the end of the buffer |
| put_word64 | Write a 64-bit word at the end of the buffer |


To write to the buffer we can do it in the following way:

```python
# Example of a big-endian ordered buffer
bytebuffer = ByteBuffer(order=ByteOrder.BIG_ENDIAN)
bytebuffer.put_word8(0x3f) # 3f 
bytebuffer.put_word16(0xff11) # 3f ff 11
bytebuffer.put_word32(0xff773300) # 3f ff 11 ff 77 33 00

# Example of a little-endian ordered buffer
bytebuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)
bytebuffer.put_word8(0x3f) # 3f 
bytebuffer.put_word16(0xff11) # 3f 11 ff
bytebuffer.put_word32(0xff773300) # 3f 11 ff 00 33 77 ff
```

### Read operations

| Operation | Description |
|---|---|
| get_byte | Read a byte/8-bit word from the buffer |
| get_word16 | Read a 16-bit word from the buffer |
| get_word32 | Read a 32-bit word from the buffer |
| get_word64 | Read a 64-bit word from the buffer |

```python
# Example of a big-endian ordered buffer
bytebuffer = ByteBuffer('00a1b2c3d4e5f6', order=ByteOrder.BIG_ENDIAN)
bytebuffer.get_byte() # 00
bytebuffer.get_word16() # a1 b2
bytebuffer.get_word32() # c3 d4 e5 f6

# Example of a little-endian ordered buffer
bytebuffer = ByteBuffer('00a1b2c3d4e5f6', order=ByteOrder.LITTLE_ENDIAN)
bytebuffer.get_byte() # 00
bytebuffer.get_word16() # b2 a1
bytebuffer.get_word32() # f6 e5 d4 c3
```