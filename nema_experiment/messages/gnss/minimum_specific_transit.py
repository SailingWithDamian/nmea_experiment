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
from datetime import datetime
from typing import Optional

from nema_experiment.messages.base import BaseMessage
from nema_experiment.messages.fields.gnss import (RecieverIndicator,
                                                  Latitude,
                                                  Longitude,
                                                  MagneticVariation)


@dataclass(frozen=True, init=True)
class GnssMinimumSpecificTransit(BaseMessage):
    _IDENTIFIER = "RMC"

    time: datetime
    reciever_status: RecieverIndicator
    latitude: Latitude
    longitude: Longitude
    speed: float
    course: float
    variation: Optional[MagneticVariation]

    def _encode_nema_0183(self) -> str:
        variation = ["", "", "A"]
        if self.variation:
            variation = [
                f"{self.variation.degrees:02d}{self.variation.minutes:02d}.{self.variation.decimal:05d}",
                self.variation.indicator.value,
            ]

        return ",".join([f'{self.time.strftime("%H%M%S")}.{self.time.strftime("%f")[0:3]}',
                         self.reciever_status.value,
                         f"{self.latitude.degrees:02d}{self.latitude.minutes:02d}.{self.latitude.decimal:04d}",
                         self.latitude.indicator.value,
                         f"{self.longitude.degrees:03d}{self.longitude.minutes:02d}.{self.longitude.decimal:04d}",
                         self.longitude.indicator.value,
                         f"{self.speed:.2f}",
                         f"{self.course:.2f}",
                         self.time.strftime("%d%m%y")] + variation)

    @staticmethod
    def _decode_nema_0183(data) -> 'GnssMinimumSpecificTransit':
        return GnssMinimumSpecificTransit(
            datetime(year=int(data[9][4:6]),
                     month=int(data[9][2:4]),
                     day=int(data[9][0:2]),
                     hour=int(data[1][0:2]),
                     minute=int(data[1][2:4]),
                     second=int(data[1][4:6]),
                     microsecond=int(data[1][7:])),
            RecieverIndicator(data[2]),
            Latitude.decode_nema_0183(data[3], data[4]),
            Longitude.decode_nema_0183(data[5], data[6]),
            float(data[7]),
            float(data[8]),
            MagneticVariation.decode_nema_0183(data[10], data[11]) if data[10] else None,
        )
