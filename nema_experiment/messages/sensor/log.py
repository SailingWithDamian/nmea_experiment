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
class WaterSpeedAndHeading(BaseMessage):
    _IDENTIFIER = "VHW"

    heading_true: float
    heading_magnetic: float
    speed_knots: float
    speed_km: float

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f'{self.heading_true:.1f}',
            "T",
            f'{self.heading_magnetic:.1f}',
            "M",
            f'{self.speed_knots:.1f}',
            "N",
            f'{self.speed_km:.1f}',
            "K",
            "",
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'WaterSpeedAndHeading':
        return WaterSpeedAndHeading(
            float(data[1]),
            float(data[3]),
            float(data[5]),
            float(data[7]),
        )


@dataclass(frozen=True, init=True)
class SetAndDrift(BaseMessage):
    _IDENTIFIER = "VDR"

    direction_true: float
    direction_magnetic: float
    speed_knots: float

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f'{self.direction_true:.1f}',
            "T",
            f'{self.direction_magnetic:.1f}',
            "M",
            f'{self.speed_knots:.1f}',
            "N",
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'SetAndDrift':
        return SetAndDrift(
            float(data[1]),
            float(data[3]),
            float(data[5]),
        )


@dataclass(frozen=True, init=True)
class DistanceTraveledThroughWater(BaseMessage):
    _IDENTIFIER = "VLW"

    water_total_distance: float
    water_reset_distance: float
    ground_total_distance: Optional[float]
    ground_reset_distance: Optional[float]

    def _encode_nema_0183(self) -> str:
        fields = [
            f'{self.water_total_distance:.3f}',
            "N",
            f'{self.water_reset_distance:.3f}',
            "N",
        ]
        if self.ground_total_distance or self.ground_reset_distance:
            fields.extend([
                f'{self.ground_total_distance:.1f}' if self.ground_total_distance is not None else '',
                "N",
                f'{self.ground_reset_distance:.1f}' if self.ground_reset_distance is not None else '',
                "N",
            ])
        return ",".join(fields)

    @staticmethod
    def _decode_nema_0183(data) -> 'DistanceTraveledThroughWater':
        return DistanceTraveledThroughWater(
            float(data[1]),
            float(data[3]),
            float(data[5]) if len(data) > 5 else None,
            float(data[7]) if len(data) > 5 else None,
        )


@dataclass(frozen=True, init=True)
class TrackMadeGoodAndGroundSpeed(BaseMessage):
    _IDENTIFIER = "VTG"

    course_over_ground_true: Optional[float]
    course_over_ground_magnetic: Optional[float]
    speed_over_ground_knots: Optional[float]
    speed_over_ground_km: Optional[float]
    faa_mode: bool

    def _encode_nema_0183(self) -> str:
        return ",".join([
            f'{self.course_over_ground_true:.1f}' if self.course_over_ground_true is not None else '',
            'T',
            f'{self.course_over_ground_magnetic:.1f}' if self.course_over_ground_magnetic is not None else '',
            'M',
            f'{self.speed_over_ground_knots:.1f}' if self.speed_over_ground_knots is not None else '',
            'N',
            f'{self.speed_over_ground_km:.1f}' if self.speed_over_ground_km is not None else '',
            'K',
            "M" if self.faa_mode else "A",  # ???
        ])

    @staticmethod
    def _decode_nema_0183(data) -> 'TrackMadeGoodAndGroundSpeed':
        return TrackMadeGoodAndGroundSpeed(
            float(data[1]) if data[1] else None,
            float(data[3]) if data[3] else None,
            float(data[5]) if data[5] else None,
            float(data[7]) if data[7] else None,
            data[9] == "M",
        )
