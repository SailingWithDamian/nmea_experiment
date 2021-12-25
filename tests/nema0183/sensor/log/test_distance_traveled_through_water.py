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
from nema_experiment.messages.sensor.log import DistanceTraveledThroughWater


def test_encoder():
    message_type, message = DistanceTraveledThroughWater(
        6982.199,
        0.000,
        None,
        None,
    ).encode_nema_0183()

    assert message_type == "VLW"
    assert message == "6982.199,N,0.000,N"

    expected_data = "$YDVLW,6982.199,N,0.000,N*64"
    assert format_nema_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = DistanceTraveledThroughWater(
        6982.199,
        0.000,
        None,
        None,
    )

    decoded = DistanceTraveledThroughWater.decode_nema_0183(
        "$YDVLW,6982.199,N,0.000,N*64"
    )
    assert decoded == expected
