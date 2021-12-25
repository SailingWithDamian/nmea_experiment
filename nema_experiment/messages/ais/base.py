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
from nema_experiment.messages.fields.ais import AisChannel


@dataclass(frozen=True, init=True)
class AisMessage:
    total_fragments: int
    fragment: int
    message_id: Optional[int]
    channel: AisChannel
    payload: str

    def encode_nema_0183(self) -> Tuple[str, str]:
        message = ",".join(
            [
                f"{self.total_fragments:d}",
                f"{self.fragment:d}",
                f"{self.message_id:d}" if self.message_id else "",
                self.channel.value,
                self.payload,
            ]
        )
        return "VDM", message

    @staticmethod
    def decode_nema_0183(payload: str) -> 'AisMessage':
        data = un_format_nema_0183_data(payload).split(',')
        assert data[0] == 'VDM'

        return AisMessage(
            int(data[1]),
            int(data[2]),
            int(data[3]) if data[3] else None,
            AisChannel(data[4]),
            f'{data[5]},{data[6]}',
        )
