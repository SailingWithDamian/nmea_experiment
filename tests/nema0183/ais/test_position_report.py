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
from nema_experiment.helpers import format_nema_0183_data
from nema_experiment.messages.ais.base import AisMessage
from nema_experiment.messages.ais.position import AisPositionMessage
from nema_experiment.messages.fields.ais import (AisChannel,
                                                 AisNavigationStatus,
                                                 AisManeuverIndicator,
                                                 AisRaimStatus)
from nema_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LongitudeIndicator,
                                                  LatitudeIndicator)


def test_encoder():
    message_type, message = AisMessage(
        1,
        1,
        None,
        AisChannel.B,
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
            None,
            None,
            62,
            AisManeuverIndicator.NOT_AVAILABLE,
            4,
            AisRaimStatus.NOT_IN_USE,
            413852,
        ).encode(),
    ).encode_nema_0183()

    assert message_type == "AIVDM"
    assert message == "1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0"
    assert format_nema_0183_data(message_type, message) == b"!AIVDM,1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*42\r\n"


def test_decoder():
    expected = AisMessage(
        1,
        1,
        None,
        AisChannel.B,
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
            None,
            None,
            62,
            AisManeuverIndicator.NOT_AVAILABLE,
            4,
            AisRaimStatus.NOT_IN_USE,
            413852,
        ).encode(),
    )

    decoded = AisMessage.decode_nema_0183(
        b"!AIVDM,1,1,,B,1;U=g`?P010jHdLLBh4f4?wtAU2L,0*42\r\n"
    )
    assert decoded == expected
