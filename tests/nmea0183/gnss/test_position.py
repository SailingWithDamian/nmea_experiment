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
from nmea_experiment.messages.fields.gnss import Latitude, Longitude, LatitudeIndicator, LongitudeIndicator, \
    RecieverIndicator
from nmea_experiment.messages.gnss.position import GnssPosition


def test_encoder():
    message_type, message = GnssPosition(
        Latitude(52, 24, 2942, LatitudeIndicator.NORTH),
        Longitude(4, 53, 1544, LongitudeIndicator.EAST),
        220212.49,
        RecieverIndicator.OK,
        False,
    ).encode_nmea_0183()

    assert message_type == "GLL"
    assert message == "5224.2942,N,00453.1544,E,220212.49,A,A"

    expected_data = "$YDGLL,5224.2942,N,00453.1544,E,220212.49,A,A*65"
    assert format_nmea_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = GnssPosition(
        Latitude(52, 24, 2942, LatitudeIndicator.NORTH),
        Longitude(4, 53, 1542, LongitudeIndicator.EAST),
        220231.55,
        RecieverIndicator.OK,
        False,
    )

    decoded = GnssPosition.decode_nmea_0183(
        "$YDGLL,5224.2942,N,00453.1542,E,220231.55,A,A*6F",
    )
    assert decoded == expected
