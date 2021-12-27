'''
MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import bitstring

from nmea_experiment.messages.ais.helpers import encode_ais_payload, decode_ais_armor


def test_encoder():
    assert encode_ais_payload([
        bitstring.Bits('0b000001'),
        bitstring.Bits('0b00'),
        bitstring.Bits('0b101110010100110110111110100000'),
        bitstring.Bits('0xf'),
        bitstring.Bits('0x80'),
        bitstring.Bits('0b0000000001'),
        bitstring.Bits('0b0'),
        bitstring.Bits('0x064c58e'),
        bitstring.Bits('0b001110001001011000000010010'),
        bitstring.Bits('0xe10'),
        bitstring.Bits('0b111111111'),
        bitstring.Bits('0b111110'),
        bitstring.Bits('0b00'),
        bitstring.Bits('0b100'),
        bitstring.Bits('0b0'),
        bitstring.Bits('0b1100101000010011100')
    ]) == ("1;U=g`?P010jHdLLBh4f4?wtAU2L", 0)


def test_decoder():
    assert decode_ais_armor("1;U=g`?P010jHdLLBh4f4?wtAU2L", 0) == (
        # This is the bin string of the above
        '00000100101110010100'
        '110110111110100000111'
        '110000000000000000100'
        '000011001001100010110'
        '001110001110001001011'
        '000000010010111000010'
        '000111111111111110001'
        '0001100101000010011100'
    )
