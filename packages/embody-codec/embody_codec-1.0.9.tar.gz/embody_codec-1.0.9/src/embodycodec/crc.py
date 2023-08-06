"""CRC Utility method(s) used by the embodycodec to generate CRC footers."""


def crc16(data: bytes, poly: int = 0x1021):
    data = bytearray(data)
    crc = 0xFFFF
    for byte in data:
        for i in range(0, 8):
            bit = (byte >> (7 - i) & 1) == 1
            c15 = (crc >> 15 & 1) == 1
            crc <<= 1
            if c15 ^ bit:
                crc ^= poly
    crc &= 0xFFFF
    return crc
