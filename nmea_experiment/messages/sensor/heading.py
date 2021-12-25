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
from dataclasses import dataclass
from typing import Optional

from nmea_experiment.messages.base import BaseMessage
from nmea_experiment.messages.fields.gnss import (LongitudeIndicator)


@dataclass(frozen=True, init=True)
class HeadingDeviationAndVariation(BaseMessage):
    _IDENTIFIER = "HDG"

    heading: float
    deviation: Optional[float]
    deviation_indication: Optional[LongitudeIndicator]
    variation: Optional[float]
    variation_indication: Optional[LongitudeIndicator]

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.heading:.1f}',
            f'{self.deviation:.1f}' if self.deviation is not None else '',
            self.deviation_indication.value if self.deviation_indication is not None else '',
            f'{self.variation:.1f}' if self.variation is not None else '',
            self.variation_indication.value if self.variation_indication is not None else '',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'HeadingDeviationAndVariation':
        return HeadingDeviationAndVariation(
            float(data[1]),
            float(data[2]) if data[2] else None,
            LongitudeIndicator(data[3]) if data[3] else None,
            float(data[4]) if data[4] else None,
            LongitudeIndicator(data[5]) if data[5] else None,
        )


@dataclass(frozen=True, init=True)
class HeadingMagnetic(BaseMessage):
    _IDENTIFIER = "HDM"

    degrees: float

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.degrees:.1f}',
            'M',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'HeadingMagnetic':
        return HeadingMagnetic(
            float(data[1]),
        )


@dataclass(frozen=True, init=True)
class HeadingTrue(BaseMessage):
    _IDENTIFIER = "HDT"

    degrees: float

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.degrees:.1f}',
            'T',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'HeadingTrue':
        return HeadingTrue(
            float(data[1]),
        )
