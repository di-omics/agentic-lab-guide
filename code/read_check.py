"""Check a plate read against what the transfer should have made.

The read is a CSV of 8 rows and 12 columns of numbers: rows A to H,
columns 1 to 12, exactly as the plate looks from above.

    python read_check.py simple reads.csv
    python read_check.py dilution reads.csv

Options, all for the expert to set:
    --blank 0.045        what a well of water reads, taken off first
    --max-cv 5           fail if the CV is over this many percent
    --max-off 5          fail if a channel or a step is further off
    --readjust FILE      write per-channel volume corrections to FILE
"""
import argparse
import csv
import json
import statistics
import sys

ROWS = "ABCDEFGH"
DILUTION_COLUMNS = 6
BLANK_COLUMN = 12
MAX_READJUST = 20   # percent. Further off than this needs a person.


def load(path, blank):
    with open(path, newline="") as handle:
        rows = [row for row in csv.reader(handle) if row]
    grid = [[float(x) - blank for x in row] for row in rows]
    if len(grid) != 8 or any(len(row) != 12 for row in grid):
        sys.exit("Expected 8 rows of 12 numbers.")
    return grid


def percent_off(value, target):
    return 100 * (value - target) / target


def simple(grid, args):
    """Every well got the same volume, so every well should read alike."""
    wells = [x for row in grid for x in row]
    mean = statistics.mean(wells)
    cv = 100 * statistics.stdev(wells) / mean
    print(f"plate mean {mean:.3f}   CV {cv:.1f}%")

    channels = [statistics.mean(row) for row in grid]
    middle = statistics.median(channels)
    offs = [percent_off(channel, middle) for channel in channels]
    for letter, off in zip(ROWS, offs):
        print(f"  channel {letter}: {off:+5.1f}% from the median channel")
    worst = max(abs(off) for off in offs)

    if args.readjust:
        if worst > MAX_READJUST:
            sys.exit(f"A channel is {worst:.1f}% off. That needs a person"
                     " at the instrument, not a correction.")
        factors = {letter: round(middle / channel, 3)
                   for letter, channel in zip(ROWS, channels)}
        with open(args.readjust, "w") as handle:
            json.dump(factors, handle, indent=2)
        print(f"readjust: wrote {args.readjust}")

    failed = []
    if args.max_cv is not None and cv > args.max_cv:
        failed.append(f"CV {cv:.1f}% is over {args.max_cv:g}%")
    if args.max_off is not None and worst > args.max_off:
        failed.append(f"a channel is {worst:.1f}% off,"
                      f" over {args.max_off:g}%")
    return failed


def dilution(grid, args):
    """Each column should read half of the one before it."""
    blank = statistics.mean(row[BLANK_COLUMN - 1] for row in grid)
    means = [statistics.mean(row[c] for row in grid) - blank
             for c in range(DILUTION_COLUMNS)]

    worst = 0.0
    for c in range(1, DILUTION_COLUMNS):
        ratio = means[c] / means[c - 1]
        off = percent_off(ratio, 0.5)
        worst = max(worst, abs(off))
        print(f"  column {c} to {c + 1}: x{ratio:.3f}"
              f"   ({off:+5.1f}% from a clean half)")

    failed = []
    if args.max_off is not None and worst > args.max_off:
        failed.append(f"a step is {worst:.1f}% off,"
                      f" over {args.max_off:g}%")
    return failed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["simple", "dilution"])
    parser.add_argument("reads", help="CSV, 8 rows of 12 numbers")
    parser.add_argument("--blank", type=float, default=0.0)
    parser.add_argument("--max-cv", type=float)
    parser.add_argument("--max-off", type=float)
    parser.add_argument("--readjust", metavar="FILE")
    args = parser.parse_args()

    check = {"simple": simple, "dilution": dilution}[args.task]
    failed = check(load(args.reads, args.blank), args)
    if failed:
        sys.exit("FAIL: " + "; ".join(failed))
    if args.max_cv is not None or args.max_off is not None:
        print("PASS")
