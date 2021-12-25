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
                                                 AisRaimStatus)
from nmea_experiment.messages.fields.gnss import (Latitude,
                                                  Longitude,
                                                  LatitudeIndicator,
                                                  LongitudeIndicator)


@dataclass(frozen=True, init=True)
class AisPositionMessage:
    message_type: int
    repeat_indicator: Optional[int]
    mmsi: int
    navigation_status: AisNavigationStatus
    rate_of_turn: Optional[int]
    speed_over_ground: float
    position_accuracy: int
    longitude: Longitude
    latitude: Latitude
    course_over_ground: Optional[float]
    true_heading: Optional[float]
    timestamp: int
    maneuver_indicator: AisManeuverIndicator
    reserved: int
    raim_flag: AisRaimStatus
    radio_state: int

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
        return encode_ais_payload([
            bitstring.Bits(f"uint:6={self.message_type}"),
            bitstring.Bits(f"uint:2={self.repeat_indicator if self.repeat_indicator else 0}"),
            bitstring.Bits(f"uint:30={self.mmsi}"),
            bitstring.Bits(f"uint:4={self.navigation_status.value if self.navigation_status else 15}"),
            bitstring.Bits(f"int:8={self.rate_of_turn if self.rate_of_turn else -128}"),
            bitstring.Bits(f"uint:10={self.speed_over_ground if self.speed_over_ground else 0}"),
            bitstring.Bits(f"uint:1={self.position_accuracy if self.position_accuracy else 0}"),
            bitstring.Bits(f"int:28={long}"),
            bitstring.Bits(f"int:27={lat}"),
            bitstring.Bits(f"uint:12={self.course_over_ground if self.course_over_ground else 3600}"),
            bitstring.Bits(f"uint:9={self.true_heading if self.true_heading else 511}"),
            bitstring.Bits(f"uint:6={self.timestamp if self.timestamp else 60}"),
            bitstring.Bits(f"uint:2={self.maneuver_indicator.value if self.maneuver_indicator else 0}"),
            bitstring.Bits(f"uint:3={self.reserved if self.reserved else 0}"),
            bitstring.Bits(f"uint:1={self.raim_flag.value if self.raim_flag else 0}"),
            bitstring.Bits(f"uint:19={self.radio_state if self.radio_state else 0}"),
        ])
