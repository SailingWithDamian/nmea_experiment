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
from nmea_experiment.messages.sensor.wind import WindDirectionAndSpeed


def test_encoder():
    message_type, message = WindDirectionAndSpeed(
        125.4,
        123.7,
        6.9,
        3.5,
    ).encode_nmea_0183()

    assert message_type == "MWD"
    assert message == "125.4,T,123.7,M,6.9,N,3.5,M"

    expected_data = "$YDMWD,125.4,T,123.7,M,6.9,N,3.5,M*55"
    assert format_nmea_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = WindDirectionAndSpeed(
        101.8,
        100.1,
        7.6,
        3.9,
    )

    decoded = WindDirectionAndSpeed.decode_nmea_0183(
        "$YDMWD,101.8,T,100.1,M,7.6,N,3.9,M*5A",
    )
    assert decoded == expected
