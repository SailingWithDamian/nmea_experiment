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
from datetime import datetime

from nema_experiment.helpers import format_nema_0183_data
from nema_experiment.messages.fields.gnss import (LatitudeIndicator,
                                                  LongitudeIndicator,
                                                  RecieverIndicator,
                                                  Latitude,
                                                  Longitude)
from nema_experiment.messages.gnss.minimum_specific_transit import GnssMinimumSpecificTransit


def test_encoder():
    message_type, message = GnssMinimumSpecificTransit(
        datetime(2011, 5, 28, 9, 27, 50, 0),
        RecieverIndicator.OK,
        Latitude(53, 21, 6802, LatitudeIndicator.NORTH),
        Longitude(6, 30, 3372, LongitudeIndicator.WEST),
        0.02,
        31.66,
        None,
    ).encode_nema_0183()

    assert message_type == "GPRMC"
    assert message == "092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A"

    expected_data = b"$GPRMC,092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A*43\r\n"
    assert format_nema_0183_data(message_type, message) == expected_data


def test_decoder():
    expected = GnssMinimumSpecificTransit(
        datetime(11, 5, 28, 9, 27, 50, 0),
        RecieverIndicator.OK,
        Latitude(53, 21, 6802, LatitudeIndicator.NORTH),
        Longitude(6, 30, 3372, LongitudeIndicator.WEST),
        0.02,
        31.66,
        None,
    )

    decoded = GnssMinimumSpecificTransit.decode_nema_0183(
        b"$GPRMC,092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A*43\r\n"
    )
    assert decoded == expected
