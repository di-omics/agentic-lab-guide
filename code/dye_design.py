"""Design the Rhodamine B for the QC transfers.

This is a starting point worked out from public numbers. Read the dye
once on your own plate reader and adjust before you trust it.

    python dye_design.py
    python dye_design.py --target 0.8 --stock 100 --make 20
"""
import argparse

MOLAR_MASS = 479.01    # g/mol, Rhodamine B
EXTINCTION = 110000    # per M per cm near 554 nm. The supplier's range
                       # is 104,500 to 115,800, measured in methanol.
PATH_LENGTH = 0.3      # cm, about how deep 100 uL sits in a 96-well plate
DILUTION_COLUMNS = 6

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=float, default=0.8,
                        help="absorbance wanted from 100 uL")
    parser.add_argument("--stock", type=float, default=100,
                        help="your stock, in ug/mL")
    parser.add_argument("--make", type=float, default=20,
                        help="mL of working dye to make")
    args = parser.parse_args()

    molar = args.target / (EXTINCTION * PATH_LENGTH)
    ug_per_ml = molar * MOLAR_MASS * 1000
    stock_ml = args.make * ug_per_ml / args.stock

    print("Read absorbance near 554 nm, 100 uL per well.")
    print(f"Working dye: {molar * 1e6:.0f} uM, which is"
          f" {ug_per_ml:.1f} ug/mL.")
    print(f"To make {args.make:.0f} mL: {stock_ml:.2f} mL of"
          f" {args.stock:.0f} ug/mL stock,"
          f" topped up to {args.make:.0f} mL with water.")
    print("Reservoir: dye in column 1, water in column 2,"
          " column 12 empty for waste.")
    print("Simple transfer: every well should read about"
          f" {args.target:.2f} above the blank.")
    series = [args.target * 0.5 ** n for n in range(DILUTION_COLUMNS)]
    print("Serial dilution, columns 1 to 6: "
          + ", ".join(f"{value:.3f}" for value in series))
    print("The last columns sit near a reader's floor."
          " Check yours can read them.")
