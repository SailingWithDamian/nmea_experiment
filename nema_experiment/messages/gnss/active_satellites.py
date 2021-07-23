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
from typing import Optional, Tuple

from nema_experiment.helpers import un_format_nema_0183_data
from nema_experiment.messages.fields.gnss import (GpsStatus,
                                                  GpsMode)


@dataclass(frozen=True, init=True)
class GpsActiveSatellites:
    gps_status: GpsStatus
    gps_mode: GpsMode
    sv_1: Optional[int]
    sv_2: Optional[int]
    sv_3: Optional[int]
    sv_4: Optional[int]
    sv_5: Optional[int]
    sv_6: Optional[int]
    sv_7: Optional[int]
    sv_8: Optional[int]
    sv_9: Optional[int]
    sv_10: Optional[int]
    sv_11: Optional[int]
    sv_12: Optional[int]
    pdop: float
    hdop: float
    vdop: float

    def encode_nema_0183(self) -> Tuple[str, str]:
        message = ",".join([
            self.gps_status.value,
            f"{self.gps_mode.value:d}",
            f"{self.sv_1:02d}" if self.sv_1 else "",
            f"{self.sv_2:02d}" if self.sv_2 else "",
            f"{self.sv_3:02d}" if self.sv_3 else "",
            f"{self.sv_4:02d}" if self.sv_4 else "",
            f"{self.sv_5:02d}" if self.sv_5 else "",
            f"{self.sv_6:02d}" if self.sv_6 else "",
            f"{self.sv_7:02d}" if self.sv_7 else "",
            f"{self.sv_8:02d}" if self.sv_8 else "",
            f"{self.sv_9:02d}" if self.sv_9 else "",
            f"{self.sv_10:02d}" if self.sv_10 else "",
            f"{self.sv_11:02d}" if self.sv_11 else "",
            f"{self.sv_12:02d}" if self.sv_12 else "",
            f"{self.pdop:.2f}",
            f"{self.hdop:.2f}",
            f"{self.vdop:.2f}",
        ])
        return "GPGSA", message

    @staticmethod
    def decode_nema_0183(payload: bytes) -> 'GpsActiveSatellites':
        data = un_format_nema_0183_data(payload.decode('utf-8')).split(',')
        assert data[0] == 'GPGSA'

        return GpsActiveSatellites(
            GpsStatus(data[1]),
            GpsMode(int(data[2])),
            int(data[3]) if data[3] else None,
            int(data[4]) if data[4] else None,
            int(data[5]) if data[5] else None,
            int(data[6]) if data[6] else None,
            int(data[7]) if data[7] else None,
            int(data[8]) if data[8] else None,
            int(data[9]) if data[9] else None,
            int(data[10]) if data[10] else None,
            int(data[11]) if data[11] else None,
            int(data[12]) if data[12] else None,
            int(data[13]) if data[13] else None,
            int(data[14]) if data[14] else None,
            float(data[15]),
            float(data[16]),
            float(data[17]),
        )
