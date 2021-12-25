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
from datetime import time

from nmea_experiment.helpers import format_nmea_0183_data
from nmea_experiment.messages.fields.gnss import (LatitudeIndicator,
                                                  LongitudeIndicator,
                                                  GnssQualityIndicator,
                                                  Latitude,
                                                  Longitude)
from nmea_experiment.messages.gnss.position_info import GnssPositionInformation


def test_encoder():
    message_type, message = GnssPositionInformation(
        time(9, 27, 50, 0),
        Latitude(53, 21, 6802, LatitudeIndicator.NORTH),
        Longitude(6, 30, 3372, LongitudeIndicator.WEST),
        GnssQualityIndicator.NO_DIFFERENTIAL,
        8,
        1.03,
        61.7,
        55.2,
        None,
        None,
    ).encode_nmea_0183()

    assert message_type == "GGA"
    assert message == "092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,"

    expected_data = "$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76"
    assert format_nmea_0183_data("GP", message_type, message) == expected_data


def test_decoder():
    expected = GnssPositionInformation(
        time(9, 27, 50, 0),
        Latitude(53, 21, 6802, LatitudeIndicator.NORTH),
        Longitude(6, 30, 3372, LongitudeIndicator.WEST),
        GnssQualityIndicator.NO_DIFFERENTIAL,
        8,
        1.03,
        61.7,
        55.2,
        None,
        None,
    )

    decoded = GnssPositionInformation.decode_nmea_0183(
        "$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76"
    )
    assert decoded == expected
