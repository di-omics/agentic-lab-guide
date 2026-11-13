"""First contact: connect to the Hamilton, initialize it, and stop.

Simulation first. Nothing moves:

    python first_contact.py

Then the real instrument, with someone standing at it:

    python first_contact.py --real

Add --starlet if the instrument is a STARlet.
"""
import argparse
import asyncio

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import (
    LiquidHandlerChatterboxBackend,
    STARBackend,
)
from pylabrobot.resources.hamilton import STARDeck, STARLetDeck


async def main(real: bool, starlet: bool) -> None:
    backend = STARBackend() if real else LiquidHandlerChatterboxBackend()
    deck = STARLetDeck() if starlet else STARDeck()
    lh = LiquidHandler(backend=backend, deck=deck)

    # On the real instrument, setup initializes it. It moves.
    await lh.setup()
    print("Connected and initialized." + ("" if real else " (simulated)"))

    await lh.stop()
    print("Stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true",
                        help="drive the real instrument")
    parser.add_argument("--starlet", action="store_true",
                        help="the instrument is a STARlet")
    args = parser.parse_args()
    asyncio.run(main(args.real, args.starlet))
