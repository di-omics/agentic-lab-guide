# Agentic Lab Guide

**From an instrument to an instrument driven by an agent.**

A step-by-step guide to putting an AI agent in the driver's seat of a real lab instrument.
The path is universal. Chapter one walks it with a Hamilton STAR.

Written by Di Hu. Draft, November 2026.

**Read the guide: [di-omics.github.io/agentic-lab-guide](https://di-omics.github.io/agentic-lab-guide/)**

## 2+ layers of cake

It is universal. Whatever the instrument, the path is the same: plug it into a Raspberry Pi,
drive it with [PyLabRobot](https://docs.pylabrobot.org), and make an MCP that connects your
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

**Layer 1, get it going.** Five steps:

1. Start with a Raspberry Pi.
2. Get it connected and configured on your network.
3. Cable the Hamilton to the Pi with a USB-A to USB-B cable.
4. Have Claude Code install PyLabRobot and write the driving approach.
5. Make an MCP that connects your company's context to the instrument.

**Layer 2, bake in expert judgment.** You do not always need an optimizer. Instead of
fine-tuning with Bayesian optimization, use an expert-guided approach.

1. Take a picture of the deck, so Claude Code can code in where the tip carriers and plate
   carriers are.
2. Set up a liquid transfer from the deck: a simple transfer, 100 uL from a 12-well
   reservoir into a 96-well plate, and a serial dilution.
3. Fine-tune with the expert's principles. Start with regular parameters, maximum speed for
   everything. Then: sufficient blowout volume; a low enough aspirate height that the liquid
   is not missed; a Z height at dispense where every droplet catches the well; into cells, a
   gentler speed and a distance where the tips do not scrape the cells; for lysis, a forceful
   dispense.

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
| [code/principles.py](code/principles.py) | Layer 2: the expert's principles as a rulebook. It sets the speed, the heights and the blowout |
| [code/dye_design.py](code/dye_design.py) | Layer 3: works out the Rhodamine B concentration and how to make it up |
| [code/read_check.py](code/read_check.py) | Layer 3: the CV, each channel against the median, and per-channel corrections |
| [code/example_reads/](code/example_reads) | Synthetic plate reads, not measurements, from a made-up instrument with one channel 15 percent low |
| [code/example_outputs/](code/example_outputs) | What the commands in the guide print, captured from real runs of the code |
| [tools/bake.py](tools/bake.py) | Copies the code and the outputs into the page. `--check` fails if they differ |
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
calculation from public numbers. In the rulebook, the top speed and the three heights are
placeholders for the expert to set.

## Stay at the instrument

A liquid handler has moving parts. Someone watches the deck for every run and knows how to
stop it. PyLabRobot drives the STAR through its firmware, and its authors are plain that you
use the driver at your own risk and that warranty is between you and your vendor.

## Layout

- `docs/index.html` -- the guide itself, a single page with no dependencies. Open it in a
  browser.
- `code/` -- the files the guide shows.
- `tools/bake.py` -- keeps the page and the code identical.
