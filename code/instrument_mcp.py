"""An MCP server that offers one instrument to Claude Code.

It runs on the Raspberry Pi. Claude Code starts it over SSH and calls
its tools. It simulates unless STAR_REAL=1 is set. Set
STAR_MODEL=STARlet for a STARlet.
"""
import contextlib
import os
import sys

from mcp.server.mcpserver import MCPServer
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import (
    LiquidHandlerChatterboxBackend,
    STARBackend,
)
from pylabrobot.resources.hamilton import STARDeck, STARLetDeck

REAL = os.environ.get("STAR_REAL") == "1"
STARLET = os.environ.get("STAR_MODEL", "STAR").lower() == "starlet"

server = MCPServer("hamilton-star")
lh: LiquidHandler | None = None


@server.tool()
async def status() -> str:
    """Say whether the instrument is connected, and if this is real."""
    state = "connected" if lh is not None else "not connected"
    mode = "real instrument" if REAL else "simulation"
    return f"{state} ({mode})"


@server.tool()
async def connect_and_initialize(someone_is_watching: bool) -> str:
    """Connect and initialize. On the real instrument this moves it."""
    global lh
    if lh is not None:
        return "Already connected."
    if REAL and not someone_is_watching:
        return "Refused. Someone has to be standing at the instrument."
    backend = STARBackend() if REAL else LiquidHandlerChatterboxBackend()
    deck = STARLetDeck() if STARLET else STARDeck()
    handler = LiquidHandler(backend=backend, deck=deck)
    with contextlib.redirect_stdout(sys.stderr):  # stdout belongs to MCP
        await handler.setup()
    lh = handler
    return "Connected and initialized."


@server.tool()
async def stop() -> str:
    """Stop and disconnect from the instrument."""
    global lh
    if lh is None:
        return "Not connected."
    with contextlib.redirect_stdout(sys.stderr):
        await lh.stop()
    lh = None
    return "Stopped."


if __name__ == "__main__":
    server.run()  # stdio: Claude Code talks to it over stdin and stdout
