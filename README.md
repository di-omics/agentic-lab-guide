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
| **Layer 2** | Bake in expert judgment | Stay tuned. |

## Chapters

| | Instrument | Layer 1 | Layer 2 |
| --- | --- | --- | --- |
| 01 | Hamilton STAR and STARlet | first draft | being written |

## Chapter 01 at a glance

Layer 1 for the Hamilton STAR and STARlet is five steps:

1. Start with a Raspberry Pi.
2. Get it connected and configured on your network.
3. Cable the Hamilton to the Pi with a USB-A to USB-B cable.
4. Have Claude install PyLabRobot and write the driving approach.
5. Make an MCP that connects your company's context to the instrument.

Layer 1 is done when your agent, with your company's context, can connect to the instrument
through the MCP, initialize it, and stop it, while you watch.

## Stay at the instrument

A liquid handler has moving parts. Someone watches the deck for every run and knows how to
stop it. PyLabRobot drives the STAR through its firmware, and its authors are plain that you
use the driver at your own risk and that warranty is between you and your vendor.

## Layout

- `docs/index.html` -- the guide itself, a single page with no build step and no
  dependencies. Open it in a browser.
