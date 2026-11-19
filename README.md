# Agentic Lab Guide

**From an instrument to an instrument driven by an agent.**

A step-by-step guide to putting an AI agent in the driver's seat of a real lab instrument,
and getting it to perform at the scientist's bar. The path is universal. Chapter one walks
it with a Hamilton STAR.

Written by Di Hu. Draft, November 2026.

**Read the guide: [di-omics.github.io/agentic-lab-guide](https://di-omics.github.io/agentic-lab-guide/)**

**Liquid handling, a part of its own: [di-omics.github.io/agentic-lab-guide/liquid-handling](https://di-omics.github.io/agentic-lab-guide/liquid-handling)**

## From a scientist to one who trains robots

How do you go from being a scientist to one who trains robots to scale science at the
expert's bar? The walk is the same for any instrument.

1. **Reverse engineer your instrument.** First, get to where software can drive it.
   PyLabRobot already drives the Hamilton STAR. For an instrument with no published
   automation API, see
   [plr-reverse-engineer](https://github.com/di-omics/plr-reverse-engineer).
2. **Talk to it through an agentic harness.** Through what matters to you: your own
   protocols, your own Claude Code, whatever you are comfortable with.
3. **Let it drive the instrument.** With your protocol taken into consideration.
4. **First pass.** The deck layout, the protocol, the basic steps.
5. **Second pass.** Go into the deck. With the tips in place, how do you want this to go?
   The blowout volume, the speed and the distance from the bottom are all
   [tunable parameters](#liquid-handling).

Steps 1 to 3 are Layer 1. The 2 passes are Layer 2.

## Liquid handling

A part of its own, for any liquid handler: an expert's guide to tuning one. Use it as a
starting principle for what would work, then tune it on your own instrument, with your own
tips and labware. It has
[its own page](https://di-omics.github.io/agentic-lab-guide/liquid-handling).

Go into the deck and think it through. With the tips in place, how do you want this to go?
By the physics of the tip, the liquid might hang as a drop. So you want a certain degree of
blowout volume, a certain degree of speed, and a certain distance from the bottom. All of
these are tunable parameters. Start with regular parameters, maximum speed for everything,
then tune.

| Tunable parameter | What the expert wants | Start here |
| --- | --- | --- |
| Blowout volume | Sufficient blowout, to ensure proper liquid handling. | For low volume, 20 percent of the volume. |
| Speed | Maximum speed for everything. Gentler into cells. A forceful dispense for lysis. | Maximum. Into cells, 50 to 70 percent of maximum. |
| Distance from the bottom, at aspirate | Low enough that the liquid is not missed. | 1 mm. Placeholder. |
| Distance from the bottom, at dispense | A Z height where every droplet catches the well. Over cells: far enough that the tips do not scrape the cells, close enough that the droplet dips in the well. | 1 mm, and 3 mm over cells. Placeholders. |

There are no exact speeds here. The top speed differs with the instrument, the tips and the
liquid, so that number is yours to set.

The same parameters are in [code/principles.py](code/principles.py), so your agent can
read them. Principles first, then the Rhodamine QC: change one parameter, run the plate,
and read it again.

## 2+ layers of cake

It is universal. Whatever the instrument, the path is the same: plug it into a Raspberry Pi,
or any computer that can stay with it, drive it with [PyLabRobot](https://docs.pylabrobot.org), and make an MCP that connects your
company's context to it. That is layer 1 of the cake. Layer 2 is baking in expert judgment. And
there are more layers of cake than two.

| | | |
| --- | --- | --- |
| **Layer 1** | Get it going | From an instrument, to a Raspberry Pi, to an MCP that connects your company's context to the PyLabRobot that drives it. |
| **Layer 2** | Bake in expert judgment | Expert-guided fine-tuning, to the level that is appropriate for the biological material. |
| **Layer 3** | The Rhodamine QC | Rhodamine B transfers, a plate read, and the CV of the liquid transfer. |
| **Layer 4** | Biological validation | Being written. |

**The guiding principle.** These principles first, then the Rhodamine QC. If it looks good, it
is good for biological validation.

## Chapter 01: Hamilton STAR and STARlet

**Layer 1, get it going.** 5 steps:

1. Start with a Raspberry Pi, or any computer that can stay with the instrument.
2. Get it connected and configured on your network.
3. Cable the Hamilton to the Pi with a USB-A to USB-B cable.
4. Have Claude Code install PyLabRobot and write the driving approach.
5. Make an MCP that connects your company's context to the instrument.

**Layer 2, bake in expert judgment.** You do not always need an optimizer. Instead of
fine-tuning with Bayesian optimization, use an expert-guided approach. It takes 2 passes.

First pass, the deck layout, the protocol, the basic steps:

1. Take a picture of the deck, so Claude Code can code in where the tip carriers and plate
   carriers are.
2. Set up a liquid transfer from the deck: a simple transfer, 100 uL from a 12-well
   reservoir into a 96-well plate, and a serial dilution. Your own protocol goes in the
   same way.

Second pass, go into the deck:

3. Fine-tune with the expert's principles: apply the [liquid handling](#liquid-handling)
   part on this deck. The agent says what the material is, and the rulebook sets the
   speed, the heights and the blowout.

**Layer 3, the Rhodamine QC.**

1. Set up Rhodamine B transfers, at the right concentration. Claude designs this.
2. Plate read.
3. See what is up: look at the numbers, channel by channel.
4. Liquid transfer CV, and readjust: go again until the CV passes.

**Layer 4, biological validation.** Being written.

## The how-to, in code

The guide shows real files, and they live here.

| | |
| --- | --- |
| [code/requirements.txt](code/requirements.txt) | PyLabRobot and the MCP library, pinned to the versions the guide was tested with |
| [code/first_contact.py](code/first_contact.py) | Layer 1: connect, initialize, stop. Simulation unless you pass `--real` |
| [code/instrument_mcp.py](code/instrument_mcp.py) | Layer 1: an MCP server that offers the instrument to Claude Code. Simulation unless `STAR_REAL=1` |
| [code/deck.py](code/deck.py) | Layer 2: the deck in code. Prints the deck so you can compare it with the photo |
| [code/transfer.py](code/transfer.py) | Layer 2: the simple transfer and the serial dilution. It takes a material, not a speed |
| [code/principles.py](code/principles.py) | Liquid handling: the expert's principles as a rulebook. It sets the speed as a share of your top speed, the heights and the blowout |
| [code/dye_design.py](code/dye_design.py) | Layer 3: works out the Rhodamine B concentration and how to make it up |
| [code/read_check.py](code/read_check.py) | Layer 3: the CV, each channel against the median, and per-channel corrections |
| [code/example_reads/](code/example_reads) | Synthetic plate reads, not measurements, from a made-up instrument with one channel 15 percent low |
| [code/example_outputs/](code/example_outputs) | What the commands in the guide print, captured from real runs of the code |
| [tools/bake.py](tools/bake.py) | Copies the code, the outputs and the stylesheet into the pages. `--check` fails if they differ |
| [tools/make_example_reads.py](tools/make_example_reads.py) | Makes the synthetic reads |

Try it with no instrument at all:

```bash
cd code
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python first_contact.py
python deck.py
python principles.py
python transfer.py simple --material cells
python transfer.py dilution
python dye_design.py
python read_check.py simple example_reads/simple_low_channel.csv --blank 0.045 --max-cv 5
```

Status: every file is tested in simulation with the pinned versions. The real-instrument
path uses the same calls and has not been run for this guide yet. No dye has been run and no
plate has been read: the example reads are synthetic, and the Rhodamine B design is a
calculation from public numbers. In the rulebook, the 3 heights are placeholders for the
expert to set. The top speed is left for you to set, and a real simple transfer does not
start without it.

## How this bakes into the rest

This guide is one piece. The same walk runs through the other repositories.

| | | |
| --- | --- | --- |
| **Step 1** | [plr-reverse-engineer](https://github.com/di-omics/plr-reverse-engineer) | Capture, decode and guarded replay for instruments with no automation API. |
| **Steps 2 and 3** | [plr-mcp](https://github.com/di-omics/plr-mcp) | Lab instruments as MCP tools an agent can call. Simulation by default, with hardware permission enforced in code. |
| **The QC gate** | [autonomous-lab](https://github.com/di-omics/autonomous-lab) | Expert QC gates, provenance and permission, across a whole workcell. |
| **The judgment** | [drugdev-gym](https://github.com/di-omics/drugdev-gym) | The same move, one level up. Bench knowledge written down as plain-word rules, and simulated environments where a model can train on them. Simulation only. |
| **The arms** | [robot-lab-handling](https://github.com/di-omics/robot-lab-handling) | Robot arms on everyday lab handling, in simulation. |

## Stay at the instrument

A liquid handler has moving parts. Someone watches the deck for every run and knows how to
stop it. PyLabRobot drives the STAR through its firmware, and its authors are plain that you
use the driver at your own risk and that warranty is between you and your vendor.

## Layout

- `docs/index.html` -- the guide itself. Open it in a browser.
- `docs/liquid-handling.html` -- the liquid handling part, on its own page.
- `shared/style.css` -- the one stylesheet. It is baked into each page, so every page opens
  on its own, with no dependencies.
- `code/` -- the files the guide shows.
- `tools/bake.py` -- keeps the pages, the code and the stylesheet identical.
