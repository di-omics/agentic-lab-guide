"""Make the example plate reads in code/example_reads/.

These are synthetic numbers, not measurements. They exist so that
read_check.py can be tried, and proven, without an instrument.

    python3 tools/make_example_reads.py
"""
import csv
import pathlib
import random

OUT = pathlib.Path(__file__).resolve().parent.parent / "code" / "example_reads"
BLANK = 0.045   # an empty-ish well still reads a little
SIGNAL = 0.800  # what 100 uL of dye reads, above the blank
NOISE = 0.01    # one percent well-to-well scatter


def write(name, grid):
    with open(OUT / name, "w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(
            [f"{value:.3f}" for value in row] for row in grid)


def simple(rng, low_channel=None):
    grid = []
    for r in range(8):
        factor = 0.85 if r == low_channel else 1.0
        grid.append([BLANK + SIGNAL * factor * rng.gauss(1, NOISE)
                     for _ in range(12)])
    return grid


def dilution(rng):
    grid = []
    for _ in range(8):
        row = [BLANK + 2 * SIGNAL * 0.5 ** c * rng.gauss(1, NOISE)
               for c in range(6)]
        row += [0.0] * 5 + [BLANK * rng.gauss(1, NOISE)]
        grid.append(row)
    return grid


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    rng = random.Random(7)
    write("simple_good.csv", simple(rng))
    write("simple_low_channel.csv", simple(rng, low_channel=5))  # channel F
    write("dilution_good.csv", dilution(rng))
    print("Wrote 3 synthetic reads to", OUT)
