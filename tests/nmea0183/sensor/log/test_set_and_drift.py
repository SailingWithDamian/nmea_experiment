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
from nmea_experiment.helpers import format_nmea_0183_data
from nmea_experiment.messages.sensor.log import SetAndDrift


def test_encoder():
    message_type, message = SetAndDrift(
        0.9,
        359.2,
        0.0,
    ).encode_nmea_0183()

    assert message_type == "VDR"
    assert message == "0.9,T,359.2,M,0.0,N"

    expected_data = "$YDVDR,0.9,T,359.2,M,0.0,N*20"
    assert format_nmea_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = SetAndDrift(
        23.4,
        21.7,
        0.0,
    )

    decoded = SetAndDrift.decode_nmea_0183(
        "$YDVDR,23.4,T,21.7,M,0.0,N*25",
    )
    assert decoded == expected
