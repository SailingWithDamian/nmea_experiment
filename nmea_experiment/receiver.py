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
from datetime import datetime
from typing import List

from nmea_experiment.messages.ais.base import AisInternalMessage, AisExternalMessage
from nmea_experiment.messages.gnss.active_satellites import GpsActiveSatellites
from nmea_experiment.messages.gnss.datum import DatumReference
from nmea_experiment.messages.gnss.minimum_specific_transit import GnssMinimumSpecificTransit
from nmea_experiment.messages.gnss.position import GnssPosition
from nmea_experiment.messages.gnss.position_info import GnssPositionInformation
from nmea_experiment.messages.gnss.visible_satellites import GpsVisibleSatellites
from nmea_experiment.messages.sensor.depth import DepthBelowSurface, DepthBelowTransducer, DepthOfWater
from nmea_experiment.messages.sensor.environment import TimeAndDate, MeteorologicalComposite, AverageWaterTemperature
from nmea_experiment.messages.sensor.heading import HeadingTrue, HeadingMagnetic, HeadingDeviationAndVariation
from nmea_experiment.messages.sensor.log import (TrackMadeGoodAndGroundSpeed,
                                                 DistanceTraveledThroughWater,
                                                 SetAndDrift,
                                                 WaterSpeedAndHeading)
from nmea_experiment.messages.sensor.rudder import RudderAngle
from nmea_experiment.messages.sensor.wind import (WindDirectionAndSpeed,
                                                  WindSpeedAndAngle,
                                                  RelativeWindSpeedAndAngle,
                                                  TrueWindSpeedAndAngle)

logger = logging.getLogger(__name__)
_IDENTIFIER_MAP = {
    cls._IDENTIFIER: cls  # type: ignore
    for cls in {GpsActiveSatellites, DatumReference, GnssMinimumSpecificTransit,
                GnssPosition, GnssPositionInformation, GpsVisibleSatellites,
                DepthBelowSurface, DepthBelowTransducer, DepthOfWater,
                TimeAndDate, MeteorologicalComposite, AverageWaterTemperature,
                HeadingTrue, HeadingMagnetic, HeadingDeviationAndVariation,
                TrackMadeGoodAndGroundSpeed, DistanceTraveledThroughWater,
                SetAndDrift, WaterSpeedAndHeading, RudderAngle,
                WindDirectionAndSpeed, WindSpeedAndAngle, RelativeWindSpeedAndAngle,
                TrueWindSpeedAndAngle, AisInternalMessage, AisExternalMessage}
}


async def decode_data_stream(address: str, port: int, filter: List[str], raw: bool):
    r, w = await asyncio.open_connection(address, port)
    while data := (await r.readline()).decode('ascii').rstrip():
        talker_id = data[1:3]
        message_type = data[3:6]
        try:
            model = _IDENTIFIER_MAP[message_type].decode_nmea_0183(data)  # type: ignore
        except KeyError:
            logger.warning(f'Unsupported message type ({message_type}) from {talker_id}: {data!r}')
        except Exception as e:
            logger.exception(f'Decoder for {message_type} failed: {data!r}. {e}')
        else:
            if filter and message_type not in filter:
                logger.debug(f'Received from {talker_id}: {model}')
            else:
                if raw:
                    print(f'[{datetime.utcnow()}] {data}')
                else:
                    logger.info(f'Received from {talker_id}: {model}')
