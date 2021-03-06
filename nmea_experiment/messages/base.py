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
from typing import Tuple, List

from nmea_experiment.helpers import un_format_nmea_0183_data


class BaseMessage:
    _IDENTIFIER = ""

    def _encode_nmea_0183(self) -> str:
        raise NotImplementedError

    @staticmethod
    def _decode_nmea_0183(data: List[str]) -> 'BaseMessage':
        raise NotImplementedError

    def encode_nmea_0183(self) -> Tuple[str, str]:
        """

        :rtype: object
        """
        message = self._encode_nmea_0183()
        return self._IDENTIFIER, message

    @classmethod
    def decode_nmea_0183(cls, payload: str) -> 'BaseMessage':
        data = un_format_nmea_0183_data(payload).split(',')
        assert data[0] == cls._IDENTIFIER
        return cls._decode_nmea_0183(data)
