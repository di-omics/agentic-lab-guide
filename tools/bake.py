"""Bake the code files and the stylesheet into the guide pages.

The guide shows the real files from code/. This script copies them into
every page in docs/, into every <pre data-file="..."> block. It also
copies the one stylesheet into every <style data-file="..."> block, so
each page opens on its own.

    python3 tools/bake.py          # write the pages
    python3 tools/bake.py --check  # fail if a page and the files differ
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted((ROOT / "docs").glob("*.html"))
BLOCK = re.compile(r'(<pre data-file="([^"]+)">)(.*?)(</pre>)', re.DOTALL)
STYLE = re.compile(r'(<style data-file="([^"]+)">\n)(.*?)(</style>)',
                   re.DOTALL)


def baked(page: str) -> str:
    def fill(match: re.Match) -> str:
        source = (ROOT / match.group(2)).read_text().rstrip("\n")
        return match.group(1) + html.escape(source, quote=False) + match.group(4)

    def style(match: re.Match) -> str:
        return match.group(1) + (ROOT / match.group(2)).read_text() + match.group(4)

    return STYLE.sub(style, BLOCK.sub(fill, page))


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for path in PAGES:
        current = path.read_text()
        wanted = baked(current)
        files = {m.group(2) for m in BLOCK.finditer(current)}
        files |= {m.group(2) for m in STYLE.finditer(current)}
        name = path.relative_to(ROOT)
        if not check:
            path.write_text(wanted)
            print(f"Baked {len(files)} files into {name}.")
        elif current != wanted:
            stale.append(str(name))
        else:
            print(f"{name} matches {len(files)} files.")
    if stale:
        print("Stale: " + ", ".join(stale) + ". Run: python3 tools/bake.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
