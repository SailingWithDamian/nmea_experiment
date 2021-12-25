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
from nema_experiment.messages.fields.gnss import GpsVisibleSatellite
from nema_experiment.messages.gnss.visible_satellites import GpsVisibleSatellites


def test_encoder_1():
    message_type, message = GpsVisibleSatellites(
        3,
        1,
        11,
        GpsVisibleSatellite(10, 63, 137, 17),
        GpsVisibleSatellite(7, 61, 98, 15),
        GpsVisibleSatellite(5, 59, 290, 20),
        GpsVisibleSatellite(8, 54, 157, 30),
    ).encode_nema_0183()

    assert message_type == "GSV"
    assert message == "3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30"

    expected_data = "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70"
    assert format_nema_0183_data("GP", message_type, message) == expected_data


def test_decoder_1():
    expected = GpsVisibleSatellites(
        3,
        1,
        11,
        GpsVisibleSatellite(10, 63, 137, 17),
        GpsVisibleSatellite(7, 61, 98, 15),
        GpsVisibleSatellite(5, 59, 290, 20),
        GpsVisibleSatellite(8, 54, 157, 30),
    )

    decoded = GpsVisibleSatellites.decode_nema_0183(
        "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70"
    )
    assert decoded == expected


def test_encoder_2():
    message_type, message = GpsVisibleSatellites(
        3,
        2,
        11,
        GpsVisibleSatellite(2, 39, 223, 19),
        GpsVisibleSatellite(13, 28, 70, 17),
        GpsVisibleSatellite(26, 23, 252, None),
        GpsVisibleSatellite(4, 14, 186, 14),
    ).encode_nema_0183()

    assert message_type == "GSV"
    assert message == "3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14"

    expected_data = "$GPGSV,3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14*79"
    assert format_nema_0183_data("GP", message_type, message) == expected_data


def test_decoder_2():
    expected = GpsVisibleSatellites(
        3,
        2,
        11,
        GpsVisibleSatellite(2, 39, 223, 19),
        GpsVisibleSatellite(13, 28, 70, 17),
        GpsVisibleSatellite(26, 23, 252, None),
        GpsVisibleSatellite(4, 14, 186, 14),
    )

    decoded = GpsVisibleSatellites.decode_nema_0183(
        "$GPGSV,3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14*79"
    )
    assert decoded == expected


def test_encoder_3():
    message_type, message = GpsVisibleSatellites(
        3,
        3,
        11,
        GpsVisibleSatellite(29, 9, 301, 24),
        GpsVisibleSatellite(16, 9, 20, None),
        GpsVisibleSatellite(36, None, None, None),
        None,
    ).encode_nema_0183()

    assert message_type == "GSV"
    assert message == "3,3,11,29,09,301,24,16,09,020,,36,,,"

    expected_data = "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76"
    assert format_nema_0183_data("GP", message_type, message) == expected_data


def test_decoder_3():
    expected = GpsVisibleSatellites(
        3,
        3,
        11,
        GpsVisibleSatellite(29, 9, 301, 24),
        GpsVisibleSatellite(16, 9, 20, None),
        GpsVisibleSatellite(36, None, None, None),
        None,
    )

    decoded = GpsVisibleSatellites.decode_nema_0183(
        "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76"
    )
    assert decoded == expected
