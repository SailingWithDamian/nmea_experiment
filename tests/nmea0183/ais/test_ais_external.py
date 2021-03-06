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
from nmea_experiment.messages.ais.base import AisExternalMessage
from nmea_experiment.messages.ais.position_report_class_a import AisPositionClassAMessage
from nmea_experiment.messages.fields.ais import (AisChannel,
                                                 AisNavigationStatus,
                                                 AisManeuverIndicator,
                                                 AisRaimStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LongitudeIndicator,
                                                  LatitudeIndicator)


def test_encoder():
    message_type, message = AisExternalMessage(
        1,
        1,
        None,
        AisChannel.B,
        AisPositionClassAMessage(
            1,
            None,
            777220000,
            AisNavigationStatus.NOT_DEFINED,
            None,
            1,
            0,
            Longitude(11, 0, 25.044000000117705, LongitudeIndicator.EAST),
            Latitude(49, 26, 44.07600000013127, LatitudeIndicator.NORTH),
            None,
            None,
            62,
            AisManeuverIndicator.NOT_AVAILABLE,
            4,
            AisRaimStatus.NOT_IN_USE,
            413852,
        ),
        "000001001011100101001101101111101000001111100000000000000"
        "001000000110010011000101100011100011100010010110000000100"
        "101110000100001111111111111100010001100101000010011100",
    ).encode_nmea_0183()

    assert message_type == "VDM"
    assert message == "1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0"
    assert format_nmea_0183_data("AI", message_type, message) == "!AIVDM,1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*42"


def test_decoder():
    expected = AisExternalMessage(
        1,
        1,
        1,
        AisChannel.B,
        AisPositionClassAMessage(
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
        "000001001011100101001101101111101000001111100000000000000"
        "001000000110010011000101100011100011100010010110000000100"
        "101110000100001111111111111100010001100101000010011100",
    )

    decoded = AisExternalMessage.decode_nmea_0183(
        "!AIVDM,1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*42"
    )
    assert decoded == expected
