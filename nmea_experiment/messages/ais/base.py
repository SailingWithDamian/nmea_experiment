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
import logging
from dataclasses import dataclass
from typing import Optional, List, Union

from nmea_experiment.messages.ais.helpers import decode_ais_armor
from nmea_experiment.messages.ais.position_report_class_a import AisPositionClassAMessage
from nmea_experiment.messages.ais.position_report_class_b import AisPositionClassBMessage
from nmea_experiment.messages.ais.base_station_report import AisBaseStationReportMessage
from nmea_experiment.messages.base import BaseMessage
from nmea_experiment.messages.fields.ais import AisChannel

logger = logging.getLogger(__name__)
IDENTIFIER_MAP = {
    identifier: message
    for message in {AisPositionClassAMessage,
                    AisPositionClassBMessage,
                    AisBaseStationReportMessage}
    for identifier in message._IDENTIFIERS  # type: ignore
}


@dataclass(frozen=True, init=True)
class AisExternalMessage(BaseMessage):
    _IDENTIFIER = "VDM"

    total_fragments: int
    fragment: int
    message_id: Optional[int]
    channel: AisChannel
    payload: Union[None,
                   AisPositionClassAMessage,
                   AisPositionClassBMessage,
                   AisBaseStationReportMessage]
    raw: str

    def _encode_nmea_0183(self) -> str:
        return ",".join(
            [
                f"{self.total_fragments:d}",
                f"{self.fragment:d}",
                f"{self.message_id:d}" if self.message_id is not None else "",
                self.channel.value,
                self.payload.encode() if self.payload is not None else "",
            ]
        )

    @staticmethod
    def _decode_nmea_0183(data: List[str]) -> 'AisExternalMessage':
        model = None
        payload = decode_ais_armor(data[5], int(data[6]))
        message_id = int(payload[0:6], 2)

        try:
            model = IDENTIFIER_MAP[message_id].decode(payload)  # type: ignore
        except KeyError:
            logger.warning(f'Unsupported AIS message type ({message_id}): {payload}')
        except Exception as e:
            logger.exception(f'AIS decoder for {message_id} failed: {payload}. {e}')

        return AisExternalMessage(
            int(data[1]),
            int(data[2]),
            message_id,
            AisChannel(data[4]),
            model,
            payload,
        )


@dataclass(frozen=True, init=True)
class AisInternalMessage(BaseMessage):
    _IDENTIFIER = "VDO"

    total_fragments: int
    fragment: int
    message_id: Optional[int]
    payload: Union[None,
                   AisPositionClassAMessage,
                   AisPositionClassBMessage,
                   AisBaseStationReportMessage]
    raw: str

    def _encode_nmea_0183(self) -> str:
        return ",".join(
            [
                f"{self.total_fragments:d}",
                f"{self.fragment:d}",
                f"{self.message_id:d}" if self.message_id is not None else "",
                self.payload.encode() if self.payload is not None else "",
            ]
        )

    @staticmethod
    def _decode_nmea_0183(data: List[str]) -> 'AisInternalMessage':
        model = None
        payload = (decode_ais_armor(data[5], int(data[6]))
                   if len(data) == 7 else
                   decode_ais_armor(data[4], int(data[5])))
        message_id = int(payload[0:6], 2)
        try:
            model = IDENTIFIER_MAP[message_id].decode(payload)  # type: ignore
        except KeyError:
            logger.warning(f'Unsupported AIS message type ({message_id}): {payload}')
        except Exception as e:
            logger.exception(f'AIS decoder for {message_id} failed: {payload}. {e}')

        return AisInternalMessage(
            int(data[1]),
            int(data[2]),
            message_id,
            model,
            payload,
        )
