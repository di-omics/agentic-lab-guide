"""Check a plate read against what the transfer should have made.

The read is a CSV of 8 rows and 12 columns of numbers: rows A to H,
columns 1 to 12, exactly as the plate looks from above.

    python read_check.py simple reads.csv
    python read_check.py dilution reads.csv

Add --max-cv or --max-off (both in percent) to turn the numbers into a
pass or a fail. The pass mark is the expert's call.
"""
import argparse
import csv
import statistics
import sys

ROWS = "ABCDEFGH"
DILUTION_COLUMNS = 6
BLANK_COLUMN = 12


def load(path):
    with open(path, newline="") as handle:
        rows = [row for row in csv.reader(handle) if row]
    grid = [[float(x) for x in row] for row in rows]
    if len(grid) != 8 or any(len(row) != 12 for row in grid):
        sys.exit("Expected 8 rows of 12 numbers.")
    return grid


def percent_off(value, target):
    return 100 * (value - target) / target


def simple(grid, max_cv, max_off):
    """Every well got the same volume, so every well should read alike."""
    wells = [x for row in grid for x in row]
    mean = statistics.mean(wells)
    cv = 100 * statistics.stdev(wells) / mean
    print(f"plate mean {mean:.3f}   CV {cv:.1f}%")

    worst = 0.0
    for letter, row in zip(ROWS, grid):
        off = percent_off(statistics.mean(row), mean)
        worst = max(worst, abs(off))
        print(f"  channel {letter}: {off:+5.1f}% from the plate mean")

    failed = []
    if max_cv is not None and cv > max_cv:
        failed.append(f"CV {cv:.1f}% is over {max_cv}%")
    if max_off is not None and worst > max_off:
        failed.append(f"a channel is {worst:.1f}% off, over {max_off}%")
    return failed


def dilution(grid, max_cv, max_off):
    """Each column should read half of the one before it."""
    blank = statistics.mean(row[BLANK_COLUMN - 1] for row in grid)
    means = [statistics.mean(row[c] for row in grid) - blank
             for c in range(DILUTION_COLUMNS)]
    print(f"blank {blank:.3f}")

    worst = 0.0
    for c in range(1, DILUTION_COLUMNS):
        ratio = means[c] / means[c - 1]
        off = percent_off(ratio, 0.5)
        worst = max(worst, abs(off))
        print(f"  column {c} to {c + 1}: x{ratio:.3f}"
              f"   ({off:+5.1f}% from a clean half)")

    failed = []
    if max_off is not None and worst > max_off:
        failed.append(f"a step is {worst:.1f}% off, over {max_off}%")
    return failed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["simple", "dilution"])
    parser.add_argument("reads", help="CSV, 8 rows of 12 numbers")
    parser.add_argument("--max-cv", type=float, help="percent")
    parser.add_argument("--max-off", type=float, help="percent")
    args = parser.parse_args()

    check = {"simple": simple, "dilution": dilution}[args.task]
    failed = check(load(args.reads), args.max_cv, args.max_off)
    if failed:
        sys.exit("FAIL: " + "; ".join(failed))
    if args.max_cv is not None or args.max_off is not None:
        print("PASS")
