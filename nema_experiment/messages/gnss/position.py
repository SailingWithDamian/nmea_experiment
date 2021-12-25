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
from nema_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude, RecieverIndicator)


@dataclass(frozen=True, init=True)
class GnssPosition(BaseMessage):
    _IDENTIFIER = "GLL"

    latitude: Latitude
    longitude: Longitude
    time: float
    status: RecieverIndicator
    faa_mode: Optional[bool]

    def _encode_nmea_0183(self) -> str:
        fields = [
            f"{self.latitude.degrees:02d}{self.latitude.minutes:02d}.{self.latitude.decimal:04d}",
            self.latitude.indicator.value,
            f"{self.longitude.degrees:03d}{self.longitude.minutes:02d}.{self.longitude.decimal:04d}",
            self.longitude.indicator.value,
            f"{self.time:.2f}",
            self.status.value,
        ]
        if self.faa_mode is not None:
            fields.append("M" if self.faa_mode else "A")
        return ",".join(fields)

    @staticmethod
    def _decode_nema_0183(data) -> 'GnssPosition':
        return GnssPosition(
            Latitude.decode_nema_0183(data[1], data[2]),
            Longitude.decode_nema_0183(data[3], data[4]),
            float(data[5]),
            RecieverIndicator(data[6]),
            data[7] == "M" if len(data) > 6 else None
        )
