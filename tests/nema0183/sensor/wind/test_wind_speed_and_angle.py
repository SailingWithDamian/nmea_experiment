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
from nema_experiment.messages.sensor.wind import WindSpeedAndAngle


def test_encoder():
    message_type, message = WindSpeedAndAngle(
        222.0,
        "True",
        3.4,
        "M",
        True,
    ).encode_nema_0183()

    assert message_type == "MWV"
    assert message == "222.0,T,3.4,M,A"

    expected_data = "$YDMWV,222.0,T,3.4,M,A*20"
    assert format_nema_0183_data("YD", message_type, message) == expected_data


def test_decoder():
    expected = WindSpeedAndAngle(
        242.0,
        "Relative",
        4.2,
        "M",
        True,
    )

    decoded = WindSpeedAndAngle.decode_nema_0183(
        "$YDMWV,242.0,R,4.2,M,A*21",
    )
    assert decoded == expected
