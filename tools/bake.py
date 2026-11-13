"""Bake the code files into the guide page.

The guide shows the real files from code/. This script copies them into
docs/index.html, into every <pre data-file="..."> block.

    python3 tools/bake.py          # write the page
    python3 tools/bake.py --check  # fail if the page and the files differ
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "index.html"
BLOCK = re.compile(r'(<pre data-file="([^"]+)">)(.*?)(</pre>)', re.DOTALL)


def baked(page: str) -> str:
    def fill(match: re.Match) -> str:
        source = (ROOT / match.group(2)).read_text().rstrip("\n")
        return match.group(1) + html.escape(source, quote=False) + match.group(4)

    return BLOCK.sub(fill, page)


def main() -> int:
    current = PAGE.read_text()
    wanted = baked(current)
    files = [m.group(2) for m in BLOCK.finditer(current)]
    if "--check" in sys.argv:
        if current != wanted:
            print("The page is stale. Run: python3 tools/bake.py")
            return 1
        print(f"The page matches {len(files)} code files.")
        return 0
    PAGE.write_text(wanted)
    print(f"Baked {len(files)} code files into docs/index.html: {', '.join(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
