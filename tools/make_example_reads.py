"""Make the example plate reads in code/example_reads/.

These are synthetic numbers, not measurements. They exist so that
read_check.py can be tried, and proven, without an instrument.

The made-up instrument has one fault: channel F delivers 15 percent
low. If code/example_reads/corrections.json exists, the readjusted
read applies those corrections to the same faulty instrument.

    python3 tools/make_example_reads.py
"""
import csv
import json
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "code" / "example_reads"
BLANK = 0.045   # a well of water still reads a little
SIGNAL = 0.800  # what 100 uL of dye reads, above the blank
NOISE = 0.01    # one percent well-to-well scatter
GOOD = [1.0] * 8
FAULTY = [1, 1, 1, 1, 1, 0.85, 1, 1]   # channel F


def write(name, grid):
    with open(OUT / name, "w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(
            [f"{value:.3f}" for value in row] for row in grid)


def simple(seed, delivered):
    rng = random.Random(seed)
    return [[BLANK + SIGNAL * share * rng.gauss(1, NOISE)
             for _ in range(12)] for share in delivered]


def dilution(seed):
    rng = random.Random(seed)
    grid = []
    for _ in range(8):
        row = [BLANK + SIGNAL * 0.5 ** c * rng.gauss(1, NOISE)
               for c in range(6)]
        row += [0.0] * 5 + [BLANK * rng.gauss(1, NOISE)]
        grid.append(row)
    return grid


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    write("simple_good.csv", simple(7, GOOD))
    write("simple_low_channel.csv", simple(8, FAULTY))
    write("dilution_good.csv", dilution(9))
    corrections = OUT / "corrections.json"
    if corrections.exists():
        factors = json.loads(corrections.read_text())
        delivered = [share * factors[row]
                     for share, row in zip(FAULTY, "ABCDEFGH")]
        write("simple_readjusted.csv", simple(10, delivered))
    print("Wrote synthetic reads to", OUT)
