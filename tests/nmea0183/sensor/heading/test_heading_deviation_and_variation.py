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
from nmea_experiment.messages.fields.gnss import LongitudeIndicator
from nmea_experiment.messages.sensor.heading import HeadingDeviationAndVariation


def test_encoder():
    message_type, message = HeadingDeviationAndVariation(
        222.6,
        None,
        None,
        1.7,
        LongitudeIndicator.EAST,
    ).encode_nmea_0183()

    assert message_type == "HDG"
    assert message == "222.6,,,1.7,E"

    expected_data = "$YDHDG,222.6,,,1.7,E*3D"
    assert format_nmea_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = HeadingDeviationAndVariation(
        222.1,
        None,
        None,
        1.7,
        LongitudeIndicator.EAST,
    )

    decoded = HeadingDeviationAndVariation.decode_nmea_0183(
        "$YDHDG,222.1,,,1.7,E*3A",
    )
    assert decoded == expected
