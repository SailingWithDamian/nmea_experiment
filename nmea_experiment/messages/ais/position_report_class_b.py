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
from nmea_experiment.messages.fields.ais import (AisNavigationStatus,
                                                 AisManeuverIndicator,
                                                 AisRaimStatus,
                                                 AisCSUnitStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LatitudeIndicator,
                                                  LongitudeIndicator)


@dataclass(frozen=True, init=True)
class AisPositionClassBMessage:
    _IDENTIFIERS = {18, }

    message_type: int
    repeat_indicator: Optional[int]
    mmsi: int
    speed_over_ground: float
    position_accuracy: int
    longitude: Longitude
    latitude: Latitude
    course_over_ground: Optional[float]
    true_heading: Optional[float]
    timestamp: int
    cs_unit: AisCSUnitStatus
    display_flag: bool
    dsc_flag: bool
    band_flag: bool
    message_22_flag: bool
    assigned_flag: bool
    raim_flag: AisRaimStatus

    @staticmethod
    def decode(payload: str) -> 'AisPositionClassBMessage':
        def _unpack_coord(payload):
            degrees = (int(payload, 2) / 600000.0)
            min = (degrees - int(degrees)) * 60
            seconds = (min - int(min)) * 60
            return int(degrees), int(min), seconds

        long_degrees, long_minutes, long_decimal = _unpack_coord(payload[57:85])
        lat_degrees, lat_minutes, lat_decimal = _unpack_coord(payload[85:112])

        # Class B
        return AisPositionClassBMessage(
            int(payload[0:6], 2),
            int(payload[6:8], 2) if int(payload[6:8], 2) else None,
            int(payload[8:38], 2),
            int(payload[46:56], 2),
            int(payload[56], 2),
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
            int(payload[112:124], 2) if int(payload[112:124], 2) != 3600 else None,
            int(payload[124:133], 2) if int(payload[124:133], 2) != 511 else None,
            int(payload[133:139], 2),
            # 139-140 reserved
            AisCSUnitStatus(int(payload[141], 2)),
            int(payload[142], 2) == 1,
            int(payload[143], 2) == 1,
            int(payload[144], 2) == 1,
            int(payload[145], 2) == 1,
            int(payload[146], 2) == 1,
            AisRaimStatus(int(payload[147], 2)),
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
            bitstring.Bits("uint:8="),
            bitstring.Bits(f"uint:10={self.speed_over_ground if self.speed_over_ground else 0}"),
            bitstring.Bits(f"uint:1={self.position_accuracy if self.position_accuracy else 0}"),
            bitstring.Bits(f"int:28={long}"),
            bitstring.Bits(f"int:27={lat}"),
            bitstring.Bits(f"uint:12={self.course_over_ground if self.course_over_ground else 3600}"),
            bitstring.Bits(f"uint:9={self.true_heading if self.true_heading else 511}"),
            bitstring.Bits(f"uint:6={self.timestamp if self.timestamp else 60}"),
            bitstring.Bits(f"uint:2={self.cs_unit.value if self.cs_unit else 0}"),
            bitstring.Bits(f"uint:1={1 if self.display_flag else 0}"),
            bitstring.Bits(f"uint:1={1 if self.dsc_flag else 0}"),
            bitstring.Bits(f"uint:1={1 if self.band_flag else 0}"),
            bitstring.Bits(f"uint:1={1 if self.message_22_flag else 0}"),
            bitstring.Bits(f"uint:1={1 if self.assigned_flag else 0}"),
            bitstring.Bits(f"uint:1={self.raim_flag.value if self.raim_flag else 0}"),
        ])
        return f'{payload},{padding}'
