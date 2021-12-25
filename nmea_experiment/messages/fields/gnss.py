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
from enum import Enum
from typing import Optional, List


class LatitudeIndicator(Enum):
    NORTH = "N"
    SOUTH = "S"


class LongitudeIndicator(Enum):
    EAST = "E"
    WEST = "W"


class RecieverIndicator(Enum):
    OK = "A"
    INVALID = "V"


class GnssQualityIndicator(Enum):
    NO_POSITION = 0
    NO_DIFFERENTIAL = 1
    DIFFERENTIALLY_CORRECTED = 2
    HIGH_PRECISION_CONVERGED = 4
    HIGH_PRECISION_CONVERGING = 5


class GpsStatus(Enum):
    MANUAL = "M"
    AUTOMATIC = "A"


class GpsMode(Enum):
    NOT_AVAILABLE = 1
    TWO_DIMENSION = 2
    THREE_DIMENSION = 3


@dataclass(frozen=True, init=True)
class Latitude:
    degrees: int
    minutes: int
    decimal: float
    indicator: LatitudeIndicator

    @staticmethod
    def decode_nmea_0183(dms: str, indicator: str) -> 'Latitude':
        return Latitude(
            int(dms[0:2]),
            int(dms[2:4]),
            int(dms[5:]),
            LatitudeIndicator(indicator),
        )


@dataclass(frozen=True, init=True)
class Longitude:
    degrees: int
    minutes: int
    decimal: float
    indicator: LongitudeIndicator

    @staticmethod
    def decode_nmea_0183(dms: str, indicator: str) -> 'Longitude':
        return Longitude(
            int(dms[0:3]),
            int(dms[3:5]),
            int(dms[6:]),
            LongitudeIndicator(indicator),
        )


@dataclass(frozen=True, init=True)
class MagneticVariation:
    degrees: float
    minutes: Optional[int]
    decimal: Optional[int]
    indicator: LongitudeIndicator

    @staticmethod
    def decode_nmea_0183(dms: str, indicator: str) -> 'MagneticVariation':
        return MagneticVariation(
            float(dms[0:3]),
            int(dms[3:5]) if dms[3:5] else None,
            int(dms[6:]) if dms[6:] else None,
            LongitudeIndicator(indicator),
        )


@dataclass(frozen=True, init=True)
class GpsVisibleSatellite:
    prn: Optional[int]
    elevation: Optional[int]
    azimuth: Optional[int]
    snr: Optional[int]

    def encode_nmea_0183(self) -> List[str]:
        return [
            f"{self.prn:02d}",
            f"{self.elevation:02d}" if self.elevation is not None else "",
            f"{self.azimuth:03d}" if self.azimuth is not None else "",
            f"{self.snr:02d}" if self.snr is not None else "",
        ]

    @staticmethod
    def decode_nmea_0183(payload: List[str]) -> 'GpsVisibleSatellite':
        return GpsVisibleSatellite(
            int(payload[0]) if payload[0] else None,
            int(payload[1]) if payload[1] else None,
            int(payload[2]) if payload[2] else None,
            int(payload[3]) if payload[3] else None,
        )
