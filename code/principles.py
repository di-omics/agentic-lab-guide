"""Expert-guided fine-tuning, as a rulebook.

You do not always need an optimizer. Start with regular parameters and
maximum speed for everything, then fine-tune to the level that is
appropriate for the biological material.

The numbers below are the tunable parameters: the blowout volume, the
speed and the distance from the bottom. Use them as a starting
principle for what would work, then tune them on your own instrument.

The words are the expert's. A number marked PLACEHOLDER is the
expert's to set for the instrument, the tips and the labware.

    python principles.py
"""
from dataclasses import dataclass

MAX_SPEED = 500.0            # uL/s. PLACEHOLDER: the most PyLabRobot
                             # sends a STAR. Set it for your tips.
BLOWOUT_SHARE = 0.20         # blowout air, as a share of the volume
CELLS_SPEED_SHARE = 0.60     # 50 to 70 percent of maximum speed
ASPIRATE_HEIGHT = 1.0        # mm above the bottom. PLACEHOLDER
DISPENSE_HEIGHT = 1.0        # mm above the bottom. PLACEHOLDER
CELLS_DISPENSE_HEIGHT = 3.0  # mm above the bottom. PLACEHOLDER

EVERY_TRANSFER = (
    "Start with regular parameters, maximum speed for everything.",
    "Sufficient blowout volume, to ensure proper liquid handling.",
    "Aspirate low enough that the liquid is not missed.",
)
CATCH = "Dispense at a Z height where every droplet catches the well."


@dataclass(frozen=True)
class Handling:
    aspirate_speed: float
    aspirate_height: float
    dispense_speed: float
    dispense_height: float
    why: tuple


def handling(material: str) -> Handling:
    """What the expert would set for this material."""
    if material == "regular":
        speed, height, why = MAX_SPEED, DISPENSE_HEIGHT, (CATCH,)
    elif material == "cells":
        speed = MAX_SPEED * CELLS_SPEED_SHARE
        height = CELLS_DISPENSE_HEIGHT
        why = ("Gentler into cells: 50 to 70 percent of maximum speed.",
               "Far enough that the tips do not scrape the cells.",
               "Close enough that the droplet dips in the well.")
    elif material == "lysis":
        speed, height = MAX_SPEED, DISPENSE_HEIGHT
        why = ("A forceful dispense for lysis.", CATCH)
    else:
        raise ValueError(
            f"No principle for {material!r}. Ask the expert.")
    return Handling(MAX_SPEED, ASPIRATE_HEIGHT, speed, height,
                    EVERY_TRANSFER + why)


def aspirate_args(h: Handling, vols):
    return {"flow_rates": [h.aspirate_speed] * len(vols),
            "liquid_height": [h.aspirate_height] * len(vols),
            "blow_out_air_volume": [BLOWOUT_SHARE * v for v in vols]}


def dispense_args(h: Handling, vols):
    return {"flow_rates": [h.dispense_speed] * len(vols),
            "liquid_height": [h.dispense_height] * len(vols),
            "blow_out_air_volume": [BLOWOUT_SHARE * v for v in vols]}


def describe(material: str, volume: float) -> str:
    h = handling(material)
    lines = [
        f"{material}, {volume:g} uL",
        f"  aspirate {h.aspirate_speed:g} uL/s,"
        f" {h.aspirate_height:g} mm above the bottom",
        f"  dispense {h.dispense_speed:g} uL/s,"
        f" {h.dispense_height:g} mm above the bottom",
        f"  blowout  {BLOWOUT_SHARE * volume:g} uL",
    ]
    return "\n".join(lines + [f"  - {reason}" for reason in h.why])


if __name__ == "__main__":
    for material in ("regular", "cells", "lysis"):
        print(describe(material, 100))
        print()
