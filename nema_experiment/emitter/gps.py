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
from datetime import time

from nema_experiment.helpers import format_nema_0183_data
from nema_experiment.messages.fields.gnss import (LatitudeIndicator,
                                                  LongitudeIndicator,
                                                  GnssQualityIndicator,
                                                  Latitude,
                                                  Longitude)
from nema_experiment.messages.gnss.position_info import GnssPositionInformation

logger = logging.getLogger(__name__)


async def make_a_square(address: str, port: int) -> None:
    offset = 0
    positions = [
        # Left line down
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(50, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(45, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),

        # Bottom line right
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(40, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(35, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(30, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(25, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),

        # Right line up
        (Latitude(40, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(45, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(50, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),

        # Top line left
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(20, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(25, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(30, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(35, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(40, 0, 0, LongitudeIndicator.WEST)),
        (Latitude(55, 00, 0, LatitudeIndicator.NORTH), Longitude(45, 0, 0, LongitudeIndicator.WEST)),
    ]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if offset >= len(positions):
            offset = 0
        lat, lon = positions[offset]
        offset += 1

        logger.info(f'Sending GnssPositionInformation for @ {lat} / {lon}')
        message_type, message = GnssPositionInformation(
            time(9, 27, 50, 0),
            lat,
            lon,
            GnssQualityIndicator.NO_DIFFERENTIAL,
            8,
            1.03,
            61.7,
            55.2,
            None,
            None,
        ).encode_nema_0183()
        s.sendto(format_nema_0183_data(message_type, message), (address, port))

        await asyncio.sleep(2)
