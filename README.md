# Agentic Lab Guide

**From an instrument to an instrument driven by an agent.**

A step-by-step guide to putting an AI agent in the driver's seat of a real lab instrument.
The path is universal. Chapter one walks it with a Hamilton STAR.

Written by Di Hu. Draft, November 2026.

**Read the guide: [di-omics.github.io/agentic-lab-guide](https://di-omics.github.io/agentic-lab-guide/)**

## Two layers of the cake

It is universal. Whatever the instrument, the path is the same: plug it into a Raspberry Pi,
drive it with [PyLabRobot](https://docs.pylabrobot.org), and make an MCP that connects your
company's context to it. That is layer 1 of the cake. Layer 2 is baking in expert judgment.

| | | |
| --- | --- | --- |
| **Layer 1** | Get it going | From an instrument, to a Raspberry Pi, to an MCP that connects your company's context to the PyLabRobot that drives it. |
| **Layer 2** | Bake in expert judgment | Take a picture of the deck, do a transfer, read it in a plate reader. More is being written. |

## Chapters

| | Instrument | Layer 1 | Layer 2 |
| --- | --- | --- | --- |
| 01 | Hamilton STAR and STARlet | first draft, with code | first three steps, with code |

## Chapter 01 at a glance

Layer 1 for the Hamilton STAR and STARlet is five steps:

1. Start with a Raspberry Pi.
2. Get it connected and configured on your network.
3. Cable the Hamilton to the Pi with a USB-A to USB-B cable.
4. Have Claude Code install PyLabRobot and write the driving approach.
5. Make an MCP that connects your company's context to the instrument.

Layer 1 is done when Claude Code, with your company's context, can connect to the instrument
through the MCP, initialize it, and stop it, while you watch.

Layer 2 starts with three steps:

1. Take a picture of the deck, so Claude Code can code in where the tip carriers and plate
   carriers are.
2. Do a transfer: a simple transfer, 100 uL from a 12-well reservoir into a 96-well plate,
   and a serial dilution.
3. Read it in a plate reader, with a standard liquid handling dye at the right
   concentration. Claude designs the dye check.

## The how-to, in code

The guide shows real files, and they live here.

| | |
| --- | --- |
| [code/requirements.txt](code/requirements.txt) | PyLabRobot and the MCP library, pinned to the versions the guide was tested with |
| [code/first_contact.py](code/first_contact.py) | Step 4: connect, initialize, stop. Simulation unless you pass `--real` |
| [code/instrument_mcp.py](code/instrument_mcp.py) | Step 5: an MCP server that offers the instrument to Claude Code. Simulation unless `STAR_REAL=1` |
| [code/deck.py](code/deck.py) | Layer 2, step 1: the deck in code. Prints the deck so you can compare it with the photo |
| [code/transfer.py](code/transfer.py) | Layer 2, step 2: the simple transfer and the serial dilution. Simulation unless you pass `--real` |
| [code/read_check.py](code/read_check.py) | Layer 2, step 3: checks a plate read against what the transfer should have made |
| [code/example_reads/](code/example_reads) | Three synthetic plate reads, not measurements. One has a planted fault |
| [tools/bake.py](tools/bake.py) | Copies the code files into the page. `--check` fails if the page and the files differ |
| [tools/make_example_reads.py](tools/make_example_reads.py) | Makes the synthetic reads |

Try it with no instrument at all:

```bash
cd code
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python first_contact.py
python deck.py
python transfer.py simple
python transfer.py dilution
python read_check.py simple example_reads/simple_low_channel.csv --max-off 5
```

Status: every file is tested in simulation with the pinned versions. The real-instrument
path uses the same calls and has not been run for this guide yet. No dye has been run and no
plate has been read: the example reads are synthetic.

## Stay at the instrument

A liquid handler has moving parts. Someone watches the deck for every run and knows how to
stop it. PyLabRobot drives the STAR through its firmware, and its authors are plain that you
use the driver at your own risk and that warranty is between you and your vendor.

## Layout

- `docs/index.html` -- the guide itself, a single page with no dependencies. Open it in a
  browser.
- `code/` -- the files the guide shows.
- `tools/bake.py` -- keeps the page and the code identical.
