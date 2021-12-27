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

from nmea_experiment.messages.base import BaseMessage


@dataclass(frozen=True, init=True)
class WindDirectionAndSpeed(BaseMessage):
    _IDENTIFIER = "MWD"

    angle_true: float
    angle_magnetic: float
    speed_knots: float
    speed_meters: float

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.angle_true:.1f}' if self.angle_true is not None else '',
            'T',
            f'{self.angle_magnetic:.1f}' if self.angle_magnetic is not None else '',
            'M',
            f'{self.speed_knots:.1f}' if self.speed_knots is not None else '',
            'N',
            f'{self.speed_meters:.1f}' if self.speed_meters is not None else '',
            'M',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'WindDirectionAndSpeed':
        return WindDirectionAndSpeed(
            float(data[1]),
            float(data[3]),
            float(data[5]),
            float(data[7]),
        )


@dataclass(frozen=True, init=True)
class WindSpeedAndAngle(BaseMessage):
    _IDENTIFIER = "MWV"

    angle: float
    reference: str
    speed: float
    unit: str
    valid: bool

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.angle:.1f}',
            'R' if self.reference == 'Relative' else 'T',
            f'{self.speed:.1f}',
            f'{self.unit}',
            "A" if self.valid else "V",
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'WindSpeedAndAngle':
        return WindSpeedAndAngle(
            float(data[1]),
            "Relative" if data[2] == "R" else "True",
            float(data[3]),
            data[4],
            data[5] == "A",
        )


@dataclass(frozen=True, init=True)
class RelativeWindSpeedAndAngle(BaseMessage):
    _IDENTIFIER = "VWR"

    direction_degrees: float
    direction_bow: str
    speed_knots: float
    speed_meters: float
    speed_kilometers: float

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.direction_degrees:.1f}',
            "L" if self.direction_bow == "PORT" else "R",
            f'{self.speed_knots:.1f}',
            'N',
            f'{self.speed_meters:.1f}',
            'M',
            f'{self.speed_kilometers:.1f}',
            'K',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'RelativeWindSpeedAndAngle':
        return RelativeWindSpeedAndAngle(
            float(data[1]),
            "PORT" if data[2] == "L" else "STARBOARD",
            float(data[3]),
            float(data[5]),
            float(data[7]),  # TODO: verify
        )


@dataclass(frozen=True, init=True)
class TrueWindSpeedAndAngle(BaseMessage):
    _IDENTIFIER = "VWT"

    direction_degrees: float
    direction_bow: str
    speed_knots: float
    speed_meters: float
    speed_kilometers: float

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.direction_degrees:.1f}',
            "L" if self.direction_bow == "PORT" else "R",
            f'{self.speed_knots:.1f}',
            'N',
            f'{self.speed_meters:.1f}',
            'M',
            f'{self.speed_kilometers:.1f}',
            'K',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'TrueWindSpeedAndAngle':
        # TODO: Verify when moving
        return TrueWindSpeedAndAngle(
            float(data[1]),
            "PORT" if data[2] == "L" else "STARBOARD",
            float(data[3]),
            float(data[5]),
            float(data[7]),
        )
