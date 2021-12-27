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
from nmea_experiment.messages.ais.base import AisInternalMessage
from nmea_experiment.messages.ais.position import AisPositionMessage
from nmea_experiment.messages.fields.ais import (AisNavigationStatus,
                                                 AisManeuverIndicator,
                                                 AisRaimStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LongitudeIndicator,
                                                  LatitudeIndicator)


def test_encoder():
    message_type, message = AisInternalMessage(
        1,
        1,
        None,
        AisPositionMessage(
            1,
            None,
            777220000,
            AisNavigationStatus.NOT_DEFINED,
            None,
            1,
            0,
            Longitude(11, 0, 25.044000000117705, LongitudeIndicator.EAST),
            Latitude(49, 26, 44.07600000013127, LatitudeIndicator.NORTH),
            3600,
            511,
            62,
            AisManeuverIndicator.NOT_AVAILABLE,
            4,
            AisRaimStatus.NOT_IN_USE,
            413852,
        ),
        "0000010010111001010011011011111010000011111000"
        "0000000000000100000011001001100010110001110001"
        "11000100101100000001001011100001000011111111111"
        "11100010001100101000010011100",
    ).encode_nmea_0183()

    assert message_type == "VDO"
    assert message == "1,1,,1;U=g`?P010jHdLLBh4f4?wtAU2L,0"
    assert format_nmea_0183_data("AI", message_type, message) == "!AIVDO,1,1,,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*2E"


def test_decoder():
    expected = AisInternalMessage(
        1,
        1,
        None,
        AisPositionMessage(
            1,
            None,
            777220000,
            AisNavigationStatus.NOT_DEFINED,
            None,
            1,
            0,
            Longitude(11, 0, 25.044000000002598, LongitudeIndicator.EAST),
            Latitude(49, 26, 44.07600000000343, LatitudeIndicator.NORTH),
            None,
            None,
            62,
            AisManeuverIndicator.NOT_AVAILABLE,
            4,
            AisRaimStatus.NOT_IN_USE,
            413852,
        ),
        "0000010010111001010011011011111010000011111000"
        "0000000000000100000011001001100010110001110001"
        "11000100101100000001001011100001000011111111111"
        "11100010001100101000010011100",
    )

    decoded = AisInternalMessage.decode_nmea_0183(
        "!AIVDO,1,1,,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*2E"
    )
    assert decoded == expected
