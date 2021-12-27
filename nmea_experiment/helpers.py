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
import operator
from functools import reduce


def checksum_nmea_0183_data(payload: str) -> str:
    # The checksum is the bitwise exclusive OR of ASCII codes of all
    # characters between the $ and *, not inclusive.
    checksum = reduce(operator.xor, map(lambda x: ord(x), payload))
    return f'{checksum:02X}'


def un_format_nmea_0183_data(payload: str) -> str:
    identifier, payload = payload[0], payload[1:].rstrip()

    assert identifier in {'$', '!'}
    assert payload[-3] == '*'

    data, checksum = payload[0:-3], payload[-2:]
    assert checksum_nmea_0183_data(data) == checksum

    return data[2:]  # First 2 characters are the talker ID


def format_nmea_0183_data(talker_id: str, message_type: str, message: str) -> str:
    # Message type comes first
    data = f"{talker_id}{message_type},{message}"

    # The checksum is the bitwise exclusive OR of ASCII codes of all
    # characters between the $ and *, not inclusive.
    checksum = checksum_nmea_0183_data(data)

    # Calculate if this is a standard NMEA message
    # or an encapsulated message requiring a specific decoder
    payload_type = '$'
    if message_type in ('VDM', 'VDO'):
        payload_type = '!'

    # Messages have a maximum length of 82 characters
    payload = f"{payload_type}{data}*{checksum}"
    assert len(payload) <= 82

    return payload
