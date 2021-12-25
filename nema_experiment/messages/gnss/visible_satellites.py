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
from nema_experiment.messages.fields.gnss import GpsVisibleSatellite


@dataclass(frozen=True, init=True)
class GpsVisibleSatellites(BaseMessage):
    _IDENTIFIER = "GSV"

    total_messages: int
    current_message: int
    total_sv: int
    sv_1: Optional[GpsVisibleSatellite]
    sv_2: Optional[GpsVisibleSatellite]
    sv_3: Optional[GpsVisibleSatellite]
    sv_4: Optional[GpsVisibleSatellite]

    def _encode_nema_0183(self) -> str:
        return ",".join([f"{self.total_messages:d}",
                         f"{self.current_message:d}",
                         f"{self.total_sv:d}"] +
                        (self.sv_1.encode_nema_0183() if self.sv_1 else ['', '', '', '']) +
                        (self.sv_2.encode_nema_0183() if self.sv_2 else ['', '', '', '']) +
                        (self.sv_3.encode_nema_0183() if self.sv_3 else ['', '', '', '']) +
                        (self.sv_4.encode_nema_0183() if self.sv_4 else []))

    @staticmethod
    def _decode_nema_0183(data) -> 'GpsVisibleSatellites':
        return GpsVisibleSatellites(
            int(data[1]),
            int(data[2]),
            int(data[3]),
            GpsVisibleSatellite.decode_nema_0183(data[4:8]) if data[4:8] else None,
            GpsVisibleSatellite.decode_nema_0183(data[8:12]) if data[8:12] else None,
            GpsVisibleSatellite.decode_nema_0183(data[12:16]) if data[12:16] else None,
            GpsVisibleSatellite.decode_nema_0183(data[16:20]) if data[16:20] else None,
        )
