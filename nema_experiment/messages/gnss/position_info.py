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
from datetime import time
from typing import Optional

from nema_experiment.messages.base import BaseMessage
from nema_experiment.messages.fields.gnss import (GnssQualityIndicator,
                                                  Latitude,
                                                  Longitude)


@dataclass(frozen=True, init=True)
class GnssPositionInformation(BaseMessage):
    _IDENTIFIER = "GGA"

    time: time
    latitude: Latitude
    longitude: Longitude
    quality: GnssQualityIndicator
    satellites: Optional[int]
    hdop: Optional[float]
    altitide: Optional[float]
    geoidal: Optional[float]
    differential_age: Optional[int]
    reference_station: Optional[str]

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f'{self.time.strftime("%H%M%S")}.{self.time.strftime("%f")[0:3]}',
            f"{self.latitude.degrees:02d}{self.latitude.minutes:02d}.{self.latitude.decimal:04d}",
            self.latitude.indicator.value,
            f"{self.longitude.degrees:03d}{self.longitude.minutes:02d}.{self.longitude.decimal:04d}",
            self.longitude.indicator.value,
            f"{self.quality.value:d}",
            f"{self.satellites:d}",
            f"{self.hdop:.2f}",
            f"{self.altitide:.1f}",
            "M",
            f"{self.geoidal:.1f}",
            "M",
            f"{self.differential_age}" if self.differential_age is not None else "",
            self.reference_station if self.reference_station is not None else "",
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'GnssPositionInformation':
        return GnssPositionInformation(
            time(hour=int(data[1][0:2]),
                 minute=int(data[1][2:4]),
                 second=int(data[1][4:6]),
                 microsecond=int(data[1][7:])),
            Latitude.decode_nema_0183(data[2], data[3]),
            Longitude.decode_nema_0183(data[4], data[5]),
            GnssQualityIndicator(int(data[6])),
            int(data[7]) if data[7] else None,
            float(data[8]) if data[8] else None,
            float(data[9]) if data[9] else None,
            float(data[11]) if data[11] else None,
            int(data[13]) if data[13] else None,
            data[14] if data[14] else None,
        )
