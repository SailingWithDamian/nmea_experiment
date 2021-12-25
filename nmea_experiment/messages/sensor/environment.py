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

from nmea_experiment.messages.base import BaseMessage


@dataclass(frozen=True, init=True)
class MeteorologicalComposite(BaseMessage):
    _IDENTIFIER = "MDA"

    barometric_mercury: Optional[float]
    barometric_bar: Optional[float]
    air_temperature: Optional[float]
    water_temperature: Optional[float]
    humidity_relative: Optional[float]
    humidity_absolute: Optional[float]
    dew_point: Optional[float]
    wind_direction_true: Optional[float]
    wind_direction_magnetic: Optional[float]
    wind_speed_knots: Optional[float]
    wind_speed_meters: Optional[float]

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f"{self.barometric_mercury:.1f}" if self.barometric_mercury is not None else '',
            "I",
            f"{self.barometric_bar:.1f}" if self.barometric_bar is not None else '',
            "B",
            f"{self.air_temperature:.1f}" if self.air_temperature is not None else '',
            "C",
            f"{self.water_temperature:.1f}" if self.water_temperature is not None else '',
            "C",
            f"{self.humidity_relative:.1f}" if self.humidity_relative is not None else '',
            f"{self.humidity_absolute:.1f}" if self.humidity_absolute is not None else '',
            f"{self.dew_point:.1f}" if self.dew_point is not None else '',
            "C",
            f"{self.wind_direction_true:.1f}" if self.wind_direction_true is not None else '',
            "T",
            f"{self.wind_direction_magnetic:.1f}" if self.wind_direction_magnetic is not None else '',
            "M",
            f"{self.wind_speed_knots:.1f}" if self.wind_speed_knots is not None else '',
            "N",
            f"{self.wind_speed_meters:.1f}" if self.wind_speed_meters is not None else '',
            "M",
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'MeteorologicalComposite':
        return MeteorologicalComposite(
            float(data[1]) if data[1] else None,
            float(data[3]) if data[3] else None,
            float(data[5]) if data[5] else None,
            float(data[7]) if data[7] else None,
            float(data[9]) if data[9] else None,
            float(data[10]) if data[10] else None,
            float(data[11]) if data[11] else None,
            float(data[13]) if data[13] else None,
            float(data[15]) if data[15] else None,
            float(data[17]) if data[17] else None,
            float(data[19]) if data[19] else None,
        )


@dataclass(frozen=True, init=True)
class TimeAndDate(BaseMessage):
    _IDENTIFIER = "ZDA"
    datetime: datetime
    local_offset_hours: int
    local_offset_minutes: int

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.datetime.hour}{self.datetime.minute}{self.datetime.second}.{self.datetime.microsecond}',
            f'{self.datetime.day}',
            f'{self.datetime.month}',
            f'{self.datetime.year}',
            f'{self.local_offset_hours:02d}',
            f'{self.local_offset_minutes:02d}',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'TimeAndDate':
        return TimeAndDate(
            datetime(
                hour=int(data[1][0:2]),
                minute=int(data[1][2:4]),
                second=int(data[1][4:6]),
                microsecond=int(data[1][7:9]),
                day=int(data[2]),
                month=int(data[3]),
                year=int(data[4]),
            ),
            int(data[5]),
            int(data[6]),
        )


@dataclass(frozen=True, init=True)
class AverageWaterTemperature(BaseMessage):
    _IDENTIFIER = "MTW"

    temperature: float
    unit: str

    def _encode_nmea_0183(self) -> str:
        return ",".join([
            f'{self.temperature:.1f}',
            f'{self.unit}',
        ])

    @staticmethod
    def _decode_nmea_0183(data) -> 'AverageWaterTemperature':
        return AverageWaterTemperature(
            float(data[1]),
            data[2],
        )
