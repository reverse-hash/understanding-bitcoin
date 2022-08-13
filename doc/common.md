# Common utilities
Bitcoin makes use of different technologies and algorithms. All these operations usually require operating at bit level or with a set of bytes. To facilitate the understanding and study of these matters, we will use a series of utilities designed for help us in this purpose.

## BitStream
Implements an immutable binary sequence, backed by a string representation.

Note that this is not the most efficient way to implement such class, but for didactic and debugging purposes, it is a very convenient and user-friendly option.

To create an instance of a bit sequence, we can do it in several ways:

```python3
# Given a hexadecimal string
BitStream.from_hex('f731') # 1111011100110001

# Given an integer number
BitStream.from_int(2) # 10
BitStream.from_int(2, zfill=8) # 00000010

# Given a UTF-8 character
BitStraem.from_char('a') # 01100001

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

The buffer has an unlimited capacity and all write operations are performed at the end of the buffer. Read operations are limited to the buffer contents and can be done through an absolute or relative position.

### Preliminary concepts

#### Word
Defined as the unit of data handled by a computer processor instruction. This unit is measured in bits (8, 16, 32...) and may vary depending on the CPU architecture. Let's stick to the fact that a CPU works with a fixed blocks of data called word and it can composed by one or several bytes. The most significant byte (MSB) is the byte with the largest values, in the sense of having the highest weight bits. Additionally, the least significant byte (LSB) refers to the byte with the lower weights.

Let's take as an example a 32-bit word where we want to represent an integer number (``2009`` in decimal, ``7D9`` in hexadecimal, ``11111011001`` in binary):

<!-- w = \underset{MSB}{\underbrace{00000000}}0000000011110100\underset{LSB}{\underbrace{10100010}} -->
<img src="https://latex.codecogs.com/png.image?\bg_white&space;w%20=%20\underset{MSB}{\underbrace{00000000}}0000000011110100\underset{LSB}{\underbrace{10100010}}"/>

#### Endianness
Refers to the order in which the sequence of bytes is stored in a memory. There are multiple orderings, but the most common and the ones we need to know are the **big-endian (BE)** or **little-endian (LE)**.

##### Big-endian

Notation that stores the most significant byte (MSB) of a word at the smallest memory address and the least significant byte (LSB) at the largest memory address.

Let's continue with our example to see how it works. Suppose we want to store in memory the previous 32-bit word. When writing it to memory, it should be ordered as follows:

| Memory Address | Content  |
| --- | --- |
| ... | |
| 0x0006 | 00000000 |
| 0x0007 | 00000000 |
| 0x0008 | 11110100 |
| 0x0009 | 10100010 |
| ... | |

Note that 4 bytes (32 bits) of consecutive memory is reserved for the word. The MSB is stored in the the smallest address (0x0006) and the LSB is stored in the the largest address (0x0009).

### Little-endian

It stores the most significant byte (MSB) of a word in the largest memory address and the least significant (LSB) at the smallest memory address.

Same example as above but following this ordering:

| Memory Address | Content  |
| --- | --- |
| ... | |
| 0x0006 | 10100010 |
| 0x0007 | 11110100 |
| 0x0008 | 00000000 |
| 0x0009 | 00000000 |
| ... | |

Note that the MSB is stored in the the largest address (0x0009) and the LSB is stored in the the smallest address (0x0006).
