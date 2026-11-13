"""The deck, in code. Yours comes from a photo of your own deck.

This example deck has one tip carrier and one plate carrier. Print it
and compare it with the photo:

    python deck.py
"""
import asyncio

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import (
    LiquidHandlerChatterboxBackend,
    STARBackend,
)
from pylabrobot.resources import (
    PLT_CAR_L5AC_A00,
    TIP_CAR_480_A00,
    cor_96_wellplate_360uL_Fb,
    hamilton_96_tiprack_300uL_filter,
    nest_12_troughplate_15000uL_Vb,
    set_tip_tracking,
    set_volume_tracking,
)
from pylabrobot.resources.hamilton import STARDeck, STARLetDeck

# Where the carriers sit. Read these off the photo of your deck.
TIP_CARRIER_RAIL = 3
PLATE_CARRIER_RAIL = 15


def build_deck(lh: LiquidHandler):
    """Put the carriers and labware on the deck, as in the photo."""
    tip_carrier = TIP_CAR_480_A00(name="tip carrier")
    tip_carrier[0] = tips = hamilton_96_tiprack_300uL_filter(name="tips")

    plate_carrier = PLT_CAR_L5AC_A00(name="plate carrier")
    plate_carrier[0] = reservoir = nest_12_troughplate_15000uL_Vb(
        name="reservoir")
    plate_carrier[1] = plate = cor_96_wellplate_360uL_Fb(name="plate")

    lh.deck.assign_child_resource(tip_carrier, rails=TIP_CARRIER_RAIL)
    lh.deck.assign_child_resource(plate_carrier, rails=PLATE_CARRIER_RAIL)
    return tips, reservoir, plate


async def connect(real: bool = False, starlet: bool = False):
    """Connect, initialize, and build the deck. Simulation unless real."""
    set_tip_tracking(True)      # no picking up a tip that is not there
    set_volume_tracking(True)   # no aspirating liquid that is not there
    backend = STARBackend() if real else LiquidHandlerChatterboxBackend()
    deck = STARLetDeck() if starlet else STARDeck()
    lh = LiquidHandler(backend=backend, deck=deck)
    await lh.setup()
    tips, reservoir, plate = build_deck(lh)
    return lh, tips, reservoir, plate


async def main() -> None:
    lh, *_ = await connect()
    lh.summary()
    await lh.stop()


if __name__ == "__main__":
    asyncio.run(main())
