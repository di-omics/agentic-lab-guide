# Agentic Lab Guide

**From an instrument to an instrument driven by an agent.**

A step-by-step guide to putting an AI agent in the driver's seat of a real lab instrument.
It starts with one liquid handler and a Raspberry Pi.

Written by Di Hu. Draft, November 2026.

**Read the guide: [di-omics.github.io/agentic-lab-guide](https://di-omics.github.io/agentic-lab-guide/)**

## How it works

Each chapter takes one instrument through the same two layers.

| | | |
| --- | --- | --- |
| **Layer 1** | Get it going | The agent can reach the instrument, connect to it, and drive it. |
| **Layer 2** | Expert level | The agent runs the instrument the way an expert would. |

## Chapters

| | Instrument | Layer 1 | Layer 2 |
| --- | --- | --- | --- |
| 01 | Hamilton STAR and STARlet | first draft | being written |

## Chapter 01 at a glance

Layer 1 for the Hamilton STAR and STARlet is four steps:

1. Start with a Raspberry Pi.
2. Get it connected and configured on your network.
3. Cable the Hamilton to the Pi with a USB-A to USB-B cable.
4. Have Claude install [PyLabRobot](https://docs.pylabrobot.org) and write the driving
   approach.

Layer 1 is done when Claude can connect to the Hamilton, initialize it, and stop it, while
you watch.

## Stay at the instrument

A liquid handler has moving parts. Someone watches the deck for every run and knows how to
stop it. PyLabRobot drives the STAR through its firmware, and its authors are plain that you
use the driver at your own risk and that warranty is between you and your vendor.

## Layout

- `docs/index.html` -- the guide itself, a single page with no build step and no
  dependencies. Open it in a browser.
