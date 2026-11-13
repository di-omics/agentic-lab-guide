"""Layer 2 transfers: a simple transfer and a serial dilution.

Both go from a 12-column reservoir into a 96-well plate, with all
eight channels at once. Simulation unless you pass --real.

    python transfer.py simple      # 100 uL of dye into every well
    python transfer.py dilution    # a two-fold serial dilution
    python transfer.py simple --corrections corrections.json
    python transfer.py simple --material cells

The agent says what the material is. The rulebook in principles.py
sets the speed, the heights and the blowout.

Reservoir column 1 holds the Rhodamine B, column 2 the water, and
column 12 takes waste.
"""
import argparse
import asyncio
import json

from pylabrobot.resources import Coordinate

from deck import connect
from principles import aspirate_args, describe, dispense_args, handling

VOLUME = 100        # uL in every well at the end
MIX_CYCLES = 3      # times to draw up and push out when mixing
DILUTION_COLUMNS = 6    # columns 1 to 6 hold the series
BLANK_COLUMN = 12       # diluent only, for the reader's background

# Eight channels in one reservoir column: 9 mm apart, like rows A to H.
IN_RESERVOIR = [Coordinate(0, (3.5 - i) * 9, 0) for i in range(8)]


def column(plate, number):
    return plate[f"A{number}:H{number}"]


async def from_reservoir(lh, reservoir, number, vols, **how):
    well = reservoir[f"A{number}"][0]
    await lh.aspirate([well] * 8, vols=vols,
                      offsets=IN_RESERVOIR, spread="custom", **how)


async def to_reservoir(lh, reservoir, number, vols):
    well = reservoir[f"A{number}"][0]
    await lh.dispense([well] * 8, vols=vols,
                      offsets=IN_RESERVOIR, spread="custom")


async def simple(lh, tips, reservoir, plate, corrections=None,
                 material="regular", volume=VOLUME):
    """The same volume from reservoir column 1 into every well."""
    reservoir["A1"][0].tracker.set_volume(12000)  # what you loaded, in uL

    # The expert's principles set how the liquid is handled.
    how = handling(material)
    print(describe(material, volume))

    # One volume per channel, rows A to H. Corrections come from a read.
    factors = corrections or {}
    vols = [round(volume * factors.get(row, 1), 1) for row in "ABCDEFGH"]
    print("asking each channel for, in uL:", vols)

    await lh.pick_up_tips(column(tips, 1))
    for number in range(1, 13):
        await from_reservoir(lh, reservoir, 1, vols,
                             **aspirate_args(how, vols))
        await lh.dispense(column(plate, number), vols=vols,
                          **dispense_args(how, vols))
    await lh.discard_tips()


async def dilution(lh, tips, reservoir, plate):
    """Two-fold dilution across columns 1 to 6. Column 12 is the blank."""
    reservoir["A1"][0].tracker.set_volume(5000)   # dye
    reservoir["A2"][0].tracker.set_volume(10000)  # diluent
    tip_column = iter(range(1, 13))

    # Diluent first: every column after the first, and the blank.
    await lh.pick_up_tips(column(tips, next(tip_column)))
    for number in [*range(2, DILUTION_COLUMNS + 1), BLANK_COLUMN]:
        await from_reservoir(lh, reservoir, 2, [VOLUME] * 8)
        await lh.dispense(column(plate, number), vols=[VOLUME] * 8)
    await lh.discard_tips()

    # Dye into column 1, twice the final volume.
    await lh.pick_up_tips(column(tips, next(tip_column)))
    await from_reservoir(lh, reservoir, 1, [2 * VOLUME] * 8)
    await lh.dispense(column(plate, 1), vols=[2 * VOLUME] * 8)

    # Carry half into the next column, mix, change tips, repeat.
    for number in range(1, DILUTION_COLUMNS):
        here, there = column(plate, number), column(plate, number + 1)
        await lh.aspirate(here, vols=[VOLUME] * 8)
        await lh.dispense(there, vols=[VOLUME] * 8)
        for _ in range(MIX_CYCLES):
            await lh.aspirate(there, vols=[VOLUME] * 8)
            await lh.dispense(there, vols=[VOLUME] * 8)
        if number < DILUTION_COLUMNS - 1:
            await lh.discard_tips()
            await lh.pick_up_tips(column(tips, next(tip_column)))

    # Take the extra out of the last column so every well reads alike.
    await lh.aspirate(column(plate, DILUTION_COLUMNS), vols=[VOLUME] * 8)
    await to_reservoir(lh, reservoir, 12, [VOLUME] * 8)
    await lh.discard_tips()


def report(plate):
    """Print what the plate should now hold, column by column."""
    for number in range(1, 13):
        volumes = {round(well.tracker.get_used_volume(), 1)
                   for well in column(plate, number)}
        print(f"column {number:2}: {sorted(volumes)} uL")


async def main(args) -> None:
    lh, tips, reservoir, plate = await connect(args.real, args.starlet)
    if args.task == "simple":
        corrections = None
        if args.corrections:
            with open(args.corrections) as handle:
                corrections = json.load(handle)
        await simple(lh, tips, reservoir, plate, corrections,
                     args.material, args.volume)
    else:
        await dilution(lh, tips, reservoir, plate)
    report(plate)
    await lh.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["simple", "dilution"])
    parser.add_argument("--real", action="store_true",
                        help="drive the real instrument")
    parser.add_argument("--starlet", action="store_true",
                        help="the instrument is a STARlet")
    parser.add_argument("--corrections", metavar="FILE",
                        help="per-channel corrections from read_check.py")
    parser.add_argument("--material", default="regular",
                        help="regular, cells or lysis")
    parser.add_argument("--volume", type=float, default=VOLUME,
                        help="uL per well, for the simple transfer")
    asyncio.run(main(parser.parse_args()))
