# Common utilities
Bitcoin makes use of different technologies and algorithms for block generation, key creation, etc. All these operations usually require operating at bit level or with a set of bytes. To facilitate the development and study of these techniques, we will use a series of utilities designed for this purpose.

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
str(bitstream) # 1010111100010010

# Returns the number of bits 
len(bitstream) # 16

# Returns the hexadecimal string value
bitstream.hex() # af12

# Returns an inmmutable byte array
bitstream.bytes() # b'\xaf\x12'
```
