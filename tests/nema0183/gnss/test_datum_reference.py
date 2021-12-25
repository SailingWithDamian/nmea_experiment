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
from nema_experiment.messages.fields.gnss import Latitude, LatitudeIndicator, Longitude, LongitudeIndicator

from nema_experiment.helpers import format_nema_0183_data
from nema_experiment.messages.gnss.datum import DatumReference


def test_encoder():
    message_type, message = DatumReference(
        "W84",
        None,
        Latitude(0, 0, 0, LatitudeIndicator.NORTH),
        Longitude(0, 0, 0, LongitudeIndicator.EAST),
        0.0,
        "W84",
    ).encode_nema_0183()

    assert message_type == "DTM"
    assert message == "W84,,0000.0000,N,00000.0000,E,0.00,W84"

    expected_data = "$YDDTM,W84,,0000.0000,N,00000.0000,E,0.00,W84*65"
    assert format_nema_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = DatumReference(
        "W84",
        None,
        Latitude(0, 0, 0, LatitudeIndicator.NORTH),
        Longitude(0, 0, 0, LongitudeIndicator.EAST),
        None,
        "W84",
    )

    decoded = DatumReference.decode_nema_0183(
        "$YDDTM,W84,,0000.0000,N,00000.0000,E,,W84*7B",
    )
    assert decoded == expected
