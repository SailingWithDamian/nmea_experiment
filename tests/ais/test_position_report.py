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
from nmea_experiment.messages.ais.position import (AisPositionMessage,
                                                   AisNavigationStatus,
                                                   AisManeuverIndicator,
                                                   AisRaimStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LongitudeIndicator,
                                                  LatitudeIndicator)


def test_encoder():
    payload = AisPositionMessage(
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
    ).encode()

    assert payload == "1;U=g`?P010jHdLLBh4f4?wtAU2L,0"


def test_decoder():
    expected = AisPositionMessage(
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
    )

    payload = (
        '00000100101110010100'
        '110110111110100000111'
        '110000000000000000100'
        '000011001001100010110'
        '001110001110001001011'
        '000000010010111000010'
        '000111111111111110001'
        '0001100101000010011100'
    )
    assert AisPositionMessage.decode(payload) == expected
