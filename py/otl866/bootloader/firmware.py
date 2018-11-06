import binascii
import struct

BLOCK_SIZE = 80
BLOCK_SIZE_CLEAR = 64

ERASE_A = 0x0f
KEY_A = bytes([
    0xd1, 0xff, 0x08, 0x24, 0x56, 0x9d, 0xa4, 0x1e, 0x42, 0x8c, 0x3c, 0x76,
    0x14, 0xc7, 0xb8, 0xb5, 0x81, 0x4a, 0x13, 0x37, 0x7c, 0x0a, 0xfe, 0x3b,
    0x63, 0xc1, 0xd5, 0xfd, 0x8c, 0x39, 0xd1, 0x1f, 0x22, 0xc7, 0x7f, 0x4d,
    0x2f, 0x15, 0x71, 0x21, 0xf9, 0x25, 0x33, 0x44, 0x92, 0x93, 0x80, 0xd7,
    0xab, 0x1b, 0xb6, 0x11, 0xa9, 0x5a, 0x88, 0x29, 0xfb, 0xd9, 0xf3, 0x76,
    0xaa, 0x47, 0x73, 0xd5, 0x31, 0x06, 0x76, 0x4b, 0x90, 0xea, 0x11, 0xeb,
    0x9c, 0x3d, 0xf2, 0xfa, 0x99, 0x06, 0x96, 0x52, 0x0a, 0x8a, 0xbc, 0x04,
    0xc8, 0x14, 0x19, 0x41, 0x52, 0xf2, 0x4d, 0x7b, 0x64, 0xc0, 0x16, 0xc7,
    0xcb, 0xe9, 0xc3, 0x86, 0x77, 0x6a, 0xec, 0x44, 0xd2, 0xd9, 0x61, 0xe0,
    0x50, 0xa6, 0x60, 0xed, 0x47, 0xa2, 0x0b, 0x59, 0x02, 0xbd, 0x18, 0x4c,
    0x11, 0x14, 0xcb, 0x53, 0xe2, 0x2b, 0x21, 0xbe, 0x96, 0x76, 0x4f, 0x47,
    0x0d, 0x1f, 0x6a, 0xf4, 0x43, 0x03, 0x68, 0x3e, 0xe0, 0xfe, 0x47, 0x72,
    0x0a, 0x68, 0x8c, 0x58, 0x7e, 0xdf, 0xef, 0x13, 0xdf, 0x47, 0x55, 0x48,
    0x4d, 0x10, 0xfe, 0x82, 0x3a, 0xb7, 0x00, 0xd5, 0x79, 0x90, 0xf4, 0xc2,
    0x98, 0xc2, 0xef, 0x5b, 0x70, 0x93, 0xb4, 0xa7, 0xfa, 0xe6, 0x27, 0x48,
    0x65, 0x01, 0x05, 0x5b, 0x65, 0x94, 0xd3, 0xa0, 0xcd, 0xf7, 0x14, 0xdb,
    0x60, 0xb4, 0xbf, 0x7a, 0xe4, 0x45, 0xf0, 0x77, 0x79, 0x1f, 0xde, 0x80,
    0x29, 0xef, 0x0d, 0x56, 0xc0, 0x23, 0xc5, 0x73, 0xde, 0xac, 0xc2, 0xef,
    0x4a, 0x02, 0x2d, 0xa4, 0x89, 0x69, 0xcb, 0x91, 0xb0, 0x74, 0x75, 0x7c,
    0x76, 0xc7, 0xc8, 0xdb, 0x8d, 0x20, 0x1d, 0xf5, 0x33, 0x99, 0xbb, 0x45,
    0x04, 0x27, 0x4c, 0x1f, 0x12, 0x67, 0x8e, 0x96, 0x37, 0x9a, 0x4b, 0x9c,
    0xaa, 0xed, 0x8b, 0x6b
])

ERASE_CS = 0x06
KEY_CS = bytes([
    0x42, 0x97, 0xaf, 0x53, 0x10, 0x8d, 0xe6, 0xa1, 0x8e, 0x1c, 0x62, 0xeb,
    0xb1, 0xee, 0x79, 0x0b, 0x08, 0x07, 0x18, 0xec, 0xc7, 0xdf, 0x8c, 0xd6,
    0x76, 0xce, 0x10, 0x9f, 0x61, 0x7c, 0xf5, 0x61, 0x09, 0xfb, 0x59, 0xd0,
    0x24, 0xb4, 0x4f, 0xca, 0xe4, 0xa1, 0x3a, 0x30, 0x7c, 0xbd, 0x7a, 0xf5,
    0xe1, 0xb9, 0x4b, 0x74, 0xcd, 0xf1, 0xe9, 0x07, 0x0a, 0x9e, 0xf9, 0xd5,
    0xed, 0x4d, 0x24, 0xeb, 0x21, 0x90, 0x05, 0x8f, 0xa5, 0xf3, 0x45, 0xd0,
    0x18, 0x31, 0x04, 0x62, 0x35, 0xa8, 0x7b, 0xa9, 0x9a, 0x0b, 0xe0, 0x14,
    0xcd, 0x57, 0x8a, 0xac, 0x80, 0x08, 0x56, 0xed, 0x14, 0x8c, 0x49, 0xd4,
    0x5d, 0xf8, 0x77, 0x39, 0xa5, 0xfa, 0x23, 0x5f, 0xf3, 0x0e, 0x27, 0xca,
    0x8d, 0xf5, 0x97, 0x50, 0xbb, 0x64, 0xa1, 0x73, 0xce, 0xf9, 0xb7, 0xee,
    0x61, 0x72, 0xf1, 0x8e, 0xdf, 0x21, 0xac, 0x43, 0x45, 0x9b, 0x78, 0x77,
    0x29, 0xb1, 0x31, 0x9e, 0xfc, 0xa1, 0x6b, 0x0f, 0x8c, 0x8d, 0x13, 0x12,
    0xcc, 0x2b, 0x54, 0x3a, 0xd8, 0xbf, 0xb8, 0xf5, 0x34, 0x46, 0x90, 0x61,
    0x54, 0xf4, 0x95, 0x61, 0x62, 0xe1, 0xcf, 0xf1, 0x3b, 0x00, 0xb6, 0xb6,
    0xbb, 0x50, 0x98, 0xd9, 0x3a, 0x56, 0x3a, 0x16, 0x56, 0xca, 0xc2, 0x10,
    0xf3, 0x91, 0xd4, 0xe8, 0x81, 0xeb, 0xfc, 0x0d, 0x7e, 0xee, 0x4c, 0x56,
    0x3b, 0x33, 0x46, 0x4e, 0xe2, 0xcf, 0xfc, 0xcf, 0xb8, 0x84, 0x75, 0xd2,
    0xa0, 0x39, 0x53, 0x85, 0xe1, 0xa8, 0xb3, 0x9e, 0x28, 0x57, 0x55, 0xef,
    0xd1, 0xc9, 0xfd, 0x3b, 0x62, 0xf5, 0x18, 0x49, 0x58, 0xf7, 0xa3, 0x36,
    0x27, 0x06, 0x49, 0x0f, 0x7c, 0xa6, 0xcb, 0xa0, 0xc5, 0x1e, 0xa5, 0x86,
    0xf3, 0x2d, 0xef, 0x8c, 0x7e, 0xf9, 0x81, 0x34, 0xaa, 0x48, 0x5a, 0x93,
    0x0a, 0xf2, 0x43, 0x62
])


def extract_key(ciphertext):
    return bytes([
        ~ciphertext[0x1EEDF + 320 * i + j] & 0xFF for i in range(0, 16)
        for j in range(0, 16)
    ])


def decrypt_image(ciphertext, key):
    key_off = 0x15
    cleartext = bytearray()
    for block_off in range(0, len(ciphertext), BLOCK_SIZE):
        block = bytearray(ciphertext[block_off:block_off + BLOCK_SIZE])

        # xor the block with the keystream
        for i in range(0, BLOCK_SIZE):
            block[i] ^= key[(key_off + i) & 0xFF]

        # shift the entire block right by three bits
        carry = 0
        for i in range(0, BLOCK_SIZE):
            block[i], carry = ((block[i] >> 3) | carry) & 0xFF, block[i] << 5

        # swap bytes around
        for i in range(0, BLOCK_SIZE // 2, 4):
            opposite = BLOCK_SIZE - i - 1
            (block[i], block[opposite]) = (block[opposite], block[i])

        cleartext += block[:BLOCK_SIZE_CLEAR]
        key_off = (key_off + 4) & 0xFF

    return cleartext


def encrypt_image(cleartext, key):
    key_off = 0x15
    ciphertext = bytearray()
    for block_off in range(0, len(cleartext), BLOCK_SIZE_CLEAR):
        block = bytearray(cleartext[block_off:block_off + BLOCK_SIZE_CLEAR])

        # pad out the cipher block with zeroes
        # this is supposed to be random padding, but we don't care
        block += bytearray(BLOCK_SIZE - BLOCK_SIZE_CLEAR)

        # swap bytes around
        for i in range(0, BLOCK_SIZE // 2, 4):
            opposite = BLOCK_SIZE - i - 1
            (block[i], block[opposite]) = (block[opposite], block[i])

        # shift the entire block left by three bits
        carry = 0
        for i in reversed(range(0, BLOCK_SIZE)):
            block[i], carry = ((block[i] << 3) | carry) & 0xFF, block[i] >> 5

        # xor the block with the keystream
        for i in range(0, BLOCK_SIZE):
            block[i] ^= key[(key_off + i) & 0xFF]

        ciphertext += block
        key_off = (key_off + 4) & 0xFF

    return ciphertext


class Firmware():
    SIGNATURE = bytes([0x55, 0xAA, 0xA5, 0x5A])

    def __init__(self, image, encrypted=False):
        if encrypted:
            self.ciphertext = bytes(image)
            self.key = extract_key(self.ciphertext)
            self.image = decrypt_image(self.ciphertext, self.key)
        else:
            self.image = bytearray(image)
            self.ciphertext = None
            self.key = None

    @property
    def valid(self):
        return self.image[-4:] == self.SIGNATURE

    def encrypt(self, key, force=False):
        if key == self.key and not force:
            return self.ciphertext
        return encrypt_image(self.image, key)


class UpdateFile():
    def __init__(self, source):
        (
            self.header,
            self.a_checksum,
            self.a_erase,
            self.cs_checksum,
            self.cs_erase,
            self.a_index,
            self.a_short_key,
            self.a_long_key,
            self.cs_index,
            self.cs_short_key,
            self.cs_long_key,
            self.a_ciphertext,
            self.cs_ciphertext,
        ) = struct.unpack(
            ('< 4s' + 'I x B xx' * 2 + 'I 256s 1024s' * 2 + '154880s' * 2),
            source)

        self.a_firmware = bytes([(b ^ self.a_short_key[(i // 80) & 0xFF] ^
                                  self.a_long_key[(i + self.a_index) & 0x3FF])
                                 for i, b in enumerate(self.a_ciphertext)])

        self.cs_firmware = bytes(
            [(b ^ self.cs_short_key[(i // 80) & 0xFF] ^
              self.cs_long_key[(i + self.cs_index) & 0x3FF])
             for i, b in enumerate(self.cs_ciphertext)])

        self.valid = (self.a_checksum == binascii.crc32(self.a_firmware)
                      and self.cs_checksum == binascii.crc32(self.cs_firmware))