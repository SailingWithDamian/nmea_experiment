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

from nema_experiment.messages.base import BaseMessage


@dataclass(frozen=True, init=True)
class DepthBelowSurface(BaseMessage):
    _IDENTIFIER = "DBS"

    feet: Optional[float]
    meters: Optional[float]
    fathoms: Optional[float]

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f"{self.feet:.1f}" if self.feet is not None else '',
            'f',
            f"{self.meters:.2f}" if self.meters is not None else '',
            'M',
            f"{self.fathoms:.2f}" if self.fathoms is not None else '',
            'F',
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'DepthBelowSurface':
        return DepthBelowSurface(
            float(data[1]) if data[1] else None,
            float(data[3]) if data[3] else None,
            float(data[5]) if data[5] else None,
        )


@dataclass(frozen=True, init=True)
class DepthBelowTransducer(BaseMessage):
    _IDENTIFIER = "DBT"

    feet: Optional[float]
    meters: Optional[float]
    fathoms: Optional[float]

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f"{self.feet:.1f}" if self.feet is not None else '',
            'f',
            f"{self.meters:.2f}" if self.meters is not None else '',
            'M',
            f"{self.fathoms:.2f}" if self.fathoms is not None else '',
            'F',
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'DepthBelowTransducer':
        return DepthBelowTransducer(
            float(data[1]) if data[1] else None,
            float(data[3]) if data[3] else None,
            float(data[5]) if data[5] else None,
        )


@dataclass(frozen=True, init=True)
class DepthOfWater(BaseMessage):
    _IDENTIFIER = "DPT"

    meters: float
    offset: float
    maximum: Optional[float]

    def _encode_nema_0183(self) -> str:
        fields = [
            f"{self.meters:.2f}",
            f"{self.offset:.2f}",
        ]
        if self.maximum is not None:
            fields.append(f"{self.maximum:.2f}")
        return ",".join(fields)

    @staticmethod
    def _decode_nema_0183(data) -> 'DepthOfWater':
        return DepthOfWater(
            float(data[1]),
            float(data[2]),
            float(data[3]) if len(data) > 3 else None,
        )
