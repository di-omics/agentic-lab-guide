"""Expert-guided fine-tuning, as a rulebook.

You do not always need an optimizer. Start with regular parameters and
maximum speed for everything, then fine-tune to the level that is
appropriate for the biological material.

These are the tunable parameters: the blowout volume, the speed and
the distance from the bottom. Use them as a starting principle for
what would work, then tune them on your own instrument.

There are no exact speeds or heights here. Speed is a share of the
top speed. The top speed and the heights differ with the instrument,
the tips, the labware and the liquid, so they are yours to set. A
real run needs them.

    python principles.py
"""
from dataclasses import dataclass
from typing import Optional

TOP_SPEED = None              # uL/s. Yours to set.
ASPIRATE_HEIGHT = None        # mm above the bottom. Yours to set.
DISPENSE_HEIGHT = None        # mm above the bottom. Yours to set.
CELLS_DISPENSE_HEIGHT = None  # mm above the bottom. Yours to set.
BLOWOUT_SHARE = 0.20          # blowout air, as a share of the volume
CELLS_SPEED_SHARE = 0.60      # 50 to 70 percent of the top speed

EVERY_TRANSFER = (
    "Start with regular parameters, maximum speed for everything.",
    "Sufficient blowout volume, to ensure proper liquid handling.",
    "Aspirate low enough that the liquid is not missed.",
)
CATCH = "Dispense at a Z height where every droplet catches the well."


@dataclass(frozen=True)
class Handling:
    aspirate_speed: float              # a share of the top speed
    aspirate_height: Optional[float]   # mm above the bottom
    dispense_speed: float              # a share of the top speed
    dispense_height: Optional[float]   # mm above the bottom
    why: tuple


def handling(material: str) -> Handling:
    """What the expert would set for this material."""
    if material == "regular":
        speed, height, why = 1.0, DISPENSE_HEIGHT, (CATCH,)
    elif material == "cells":
        speed = CELLS_SPEED_SHARE
        height = CELLS_DISPENSE_HEIGHT
        why = ("Gentler into cells: 50 to 70 percent of maximum speed.",
               "Far enough that the tips do not scrape the cells.",
               "Close enough that the droplet dips in the well.")
    elif material == "lysis":
        speed, height = 1.0, DISPENSE_HEIGHT
        why = ("A forceful dispense for lysis.", CATCH)
    else:
        raise ValueError(
            f"No principle for {material!r}. Ask the expert.")
    return Handling(1.0, ASPIRATE_HEIGHT, speed, height,
                    EVERY_TRANSFER + why)


def not_set(material: str = "") -> str:
    """Say which of your numbers this material still needs."""
    names = ["TOP_SPEED", "ASPIRATE_HEIGHT", "DISPENSE_HEIGHT",
             "CELLS_DISPENSE_HEIGHT"]
    if material == "cells":
        names.remove("DISPENSE_HEIGHT")
    elif material:
        names.remove("CELLS_DISPENSE_HEIGHT")
    missing = [name for name in names if globals()[name] is None]
    if not missing:
        return ""
    return ("Not set: " + ", ".join(missing) + ".\n"
            "They differ with the instrument, the tips, the labware and"
            " the\nliquid. Set yours in principles.py.")


def _args(share: float, height: Optional[float], vols):
    how = {"blow_out_air_volume": [BLOWOUT_SHARE * v for v in vols]}
    if height is not None:
        how["liquid_height"] = [height] * len(vols)
    if TOP_SPEED is not None:
        how["flow_rates"] = [share * TOP_SPEED] * len(vols)
    return how    # what is not set is left to PyLabRobot


def aspirate_args(h: Handling, vols):
    return _args(h.aspirate_speed, h.aspirate_height, vols)


def dispense_args(h: Handling, vols):
    return _args(h.dispense_speed, h.dispense_height, vols)


def speed(share: float) -> str:
    words = ("top speed" if share == 1
             else f"{share * 100:g} percent of top speed")
    if TOP_SPEED is None:
        return words
    return f"{words}, {share * TOP_SPEED:g} uL/s"


def height(mm: Optional[float]) -> str:
    if mm is None:
        return "height not set"
    return f"{mm:g} mm above the bottom"


def describe(material: str, volume: float) -> str:
    h = handling(material)
    lines = [
        f"{material}, {volume:g} uL",
        f"  aspirate at {speed(h.aspirate_speed)},"
        f" {height(h.aspirate_height)}",
        f"  dispense at {speed(h.dispense_speed)},"
        f" {height(h.dispense_height)}",
        f"  blowout  {BLOWOUT_SHARE * volume:g} uL",
    ]
    return "\n".join(lines + [f"  - {reason}" for reason in h.why])


if __name__ == "__main__":
    for material in ("regular", "cells", "lysis"):
        print(describe(material, 100))
        print()
    if not_set():
        print(not_set())
