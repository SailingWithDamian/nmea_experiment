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
from nema_experiment.messages.fields.gnss import (Latitude, Longitude)


@dataclass(frozen=True, init=True)
class DatumReference(BaseMessage):
    _IDENTIFIER = "DTM"

    local_code: str
    local_sub_code: Optional[str]
    latitude: Latitude
    longitude: Longitude
    altitude: Optional[float]
    name: str

    def _encode_nema_0183(self) -> str:
        return ",".join([
            self.local_code,
            self.local_sub_code if self.local_sub_code is not None else '',
            f"{self.latitude.degrees:02d}{self.latitude.minutes:02d}.{self.latitude.decimal:04d}",
            self.latitude.indicator.value,
            f"{self.longitude.degrees:03d}{self.longitude.minutes:02d}.{self.longitude.decimal:04d}",
            self.longitude.indicator.value,
            f"{self.altitude:.2f}" if self.altitude is not None else '',
            self.name,
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'DatumReference':
        return DatumReference(
            data[1],
            data[2] if data[2] else None,
            Latitude.decode_nema_0183(data[3], data[4]),
            Longitude.decode_nema_0183(data[5], data[6]),
            float(data[7]) if data[7] else None,
            data[8],
        )
