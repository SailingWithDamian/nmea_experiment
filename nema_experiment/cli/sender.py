#!/usr/bin/env python3
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
import sys

import click

from nema_experiment.emitter.ais import anchor_near_square
from nema_experiment.emitter.gps import make_a_square


@click.command()
@click.option('--address', default='0.0.0.0')
@click.option('--port', default=2000)
def main(address: str, port: int) -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.create_task(make_a_square(address, port))
    loop.create_task(anchor_near_square(address, port))
    loop.run_forever()


if __name__ == "__main__":
    main()
