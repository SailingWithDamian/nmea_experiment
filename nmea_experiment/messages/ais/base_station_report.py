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

import bitstring  # type: ignore

from nmea_experiment.messages.ais.helpers import encode_ais_payload
from nmea_experiment.messages.fields.ais import (AisManeuverIndicator,
                                                 AisRaimStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LatitudeIndicator,
                                                  LongitudeIndicator)


@dataclass(frozen=True, init=True)
class AisBaseStationReportMessage:
    _IDENTIFIERS = {4, }

    message_type: int
    repeat_indicator: Optional[int]
    mmsi: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    quality: int
    longitude: Longitude
    latitude: Latitude
    epfd_type: int
    raim_flag: AisRaimStatus
    # sotdma_state: ??

    @staticmethod
    def decode(payload: str) -> 'AisBaseStationReportMessage':
        def _unpack_coord(payload):
            degrees = (int(payload, 2) / 600000.0)
            min = (degrees - int(degrees)) * 60
            seconds = (min - int(min)) * 60
            return int(degrees), int(min), seconds

        long_degrees, long_minutes, long_decimal = _unpack_coord(payload[79:107])
        lat_degrees, lat_minutes, lat_decimal = _unpack_coord(payload[107:134])
        return AisBaseStationReportMessage(
            int(payload[0:6], 2),
            int(payload[6:8], 2) if int(payload[6:8], 2) else None,
            int(payload[8:38], 2),
            int(payload[38:52], 2),
            int(payload[52:56], 2),
            int(payload[56:61], 2),
            int(payload[61:66], 2),
            int(payload[66:72], 2),
            int(payload[72:78], 2),
            int(payload[78], 2),
            Longitude(
                long_degrees,
                long_minutes,
                long_decimal,
                LongitudeIndicator.EAST if long_degrees > 0 else LongitudeIndicator.WEST,
            ),
            Latitude(
                lat_degrees,
                lat_minutes,
                lat_decimal,
                LatitudeIndicator.NORTH if long_degrees > 0 else LatitudeIndicator.SOUTH,
            ),
            int(payload[134:138], 2),
            # 138-147 spare
            AisRaimStatus(int(payload[148], 2)),
        )

    def encode(self) -> str:
        long = 181

        if self.longitude:
            long = int((self.longitude.degrees +
                        (self.longitude.minutes / 60) +
                        (self.longitude.decimal / 3600)) * 600000)

            if self.longitude.indicator == LongitudeIndicator.WEST:
                long = 0 - long

        lat = 91 * 600000
        if self.latitude:
            lat = int((self.latitude.degrees +
                       (self.latitude.minutes / 60) +
                       (self.latitude.decimal / 3600)) * 600000)

            if self.latitude.indicator == LatitudeIndicator.SOUTH:
                lat = 0 - lat

        # x-ref https://gpsd.gitlab.io/gpsd/AIVDM.html
        payload, padding = encode_ais_payload([
            bitstring.Bits(f"uint:6={self.message_type}"),
            bitstring.Bits(f"uint:2={self.repeat_indicator if self.repeat_indicator else 0}"),
            bitstring.Bits(f"uint:30={self.mmsi}"),
            bitstring.Bits(f"uint:14={self.year if self.year else 0}"),
            bitstring.Bits(f"uint:4={self.month if self.year else 0}"),
            bitstring.Bits(f"uint:5={self.day if self.day else 0}"),
            bitstring.Bits(f"uint:5={self.hour if self.hour else 0}"),
            bitstring.Bits(f"uint:6={self.minute if self.minute else 0}"),
            bitstring.Bits(f"uint:6={self.second if self.second else 0}"),
            bitstring.Bits(f"uint:1={self.quality if self.quality else 0}"),
            bitstring.Bits(f"int:28={long}"),
            bitstring.Bits(f"int:27={lat}"),
            bitstring.Bits(f"uint:4={self.epfd_type if self.epfd_type else 0}"),
            bitstring.Bits("uint:10="),
            bitstring.Bits(f"uint:1={self.raim_flag.value if self.raim_flag else 0}"),
        ])
        return f'{payload},{padding}'
