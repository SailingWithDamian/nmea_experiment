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
import asyncio
import logging
import socket

from nema_experiment.helpers import format_nema_0183_data
from nema_experiment.messages.ais.base import AisMessage
from nema_experiment.messages.ais.position import AisPositionMessage
from nema_experiment.messages.fields.ais import (AisChannel,
                                                 AisRaimStatus,
                                                 AisNavigationStatus,
                                                 AisManeuverIndicator)
from nema_experiment.messages.fields.gnss import (LatitudeIndicator,
                                                  LongitudeIndicator,
                                                  Latitude,
                                                  Longitude)

logger = logging.getLogger(__name__)


async def anchor_near_square(address: str, port: int) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        for mmsi, lon, lat in [
            (777220000, Longitude(45, 0, 10, LongitudeIndicator.WEST), Latitude(55, 0, 10, LatitudeIndicator.NORTH)),
            (777220001, Longitude(20, 0, 10, LongitudeIndicator.WEST), Latitude(55, 0, 10, LatitudeIndicator.NORTH)),
            (777220002, Longitude(45, 0, 10, LongitudeIndicator.WEST), Latitude(40, 0, 10, LatitudeIndicator.NORTH)),
            (777220003, Longitude(20, 0, 10, LongitudeIndicator.WEST), Latitude(40, 0, 10, LatitudeIndicator.NORTH)),
        ]:
            logger.info(f'Sending AisPositionMessage for {mmsi} @ {lat} / {lon}')
            message_type, message = AisMessage(
                1,
                1,
                None,
                AisChannel.B,
                AisPositionMessage(
                    1,
                    None,
                    mmsi,
                    AisNavigationStatus.NOT_UNDER_COMMAND,
                    None,
                    1,
                    0,
                    lon,
                    lat,
                    None,
                    None,
                    62,
                    AisManeuverIndicator.NOT_AVAILABLE,
                    4,
                    AisRaimStatus.NOT_IN_USE,
                    413852,
                ).encode(),
            ).encode_nema_0183()
            s.sendto(format_nema_0183_data(message_type, message), (address, port))

        await asyncio.sleep(2)
