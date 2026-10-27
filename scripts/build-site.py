#!/usr/bin/env python3
"""Build every talk into site/ for publishing.

A talk is any top-level folder with a talk.yaml next to a slyds deck. Each one is
built with `slyds build`, its speaker notes are stripped (they're for the
presenter, not the audience), and the result lands at site/<folder>/index.html.
Then site/index.html lists them all.

Usage: build-site.py [--slyds PATH] [--keep-notes]
"""

import argparse
import html
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def read_talk_yaml(path):
    # talk.yaml is flat "key: value" lines, so a full YAML parser isn't needed.
    meta = {}
    for line in path.read_text().splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta


def strip_block(doc, opener):
    """Remove every element that starts with `opener`, matching nested <div>s."""
    out, i, removed = [], 0, 0
    while True:
        start = doc.find(opener, i)
        if start < 0:
            out.append(doc[i:])
            return "".join(out), removed
        out.append(doc[i:start])
        depth, j = 0, start
        tag = re.compile(r"<(/?)div\b", re.I)
        while True:
            m = tag.search(doc, j)
            if not m:
                sys.exit(f"unclosed block starting at offset {start}")
            depth += -1 if m.group(1) else 1
            j = m.end()
            if depth == 0:
                j = doc.index(">", j) + 1
                break
        i, removed = j, removed + 1


def strip_notes(doc):
    doc, n = strip_block(doc, '<div class="speaker-notes"')
    # The notes button would only open an empty window now.
    doc = re.sub(r'<button class="notes-btn".*?</button>', "", doc, flags=re.S)
    return doc, n


def build_talk(folder, slyds, keep_notes):
    subprocess.run([slyds, "build", str(folder)], check=True, stdout=subprocess.DEVNULL)
    doc = (folder / "dist" / "index.html").read_text()
    n = 0
    if not keep_notes:
        doc, n = strip_notes(doc)
        assert 'class="speaker-notes"' not in doc, f"{folder.name}: notes left behind"
    dest = SITE / folder.name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(doc)
    return n


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talks</title>
<style>
  :root {{ --bg: #fbfaf7; --fg: #1f2a33; --muted: #5d6b75; --card: #ffffff; --line: #e4e0d8; --accent: #0d4f4f; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #151a1e; --fg: #e6ebee; --muted: #9aa7b0; --card: #1d2429; --line: #2c353b; --accent: #5cc8c0; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--fg); font: 17px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width: 760px; margin: 0 auto; padding: 56px 16px; }}
  h1 {{ font-size: 2rem; margin: 0 0 4px; }}
  .lede {{ color: var(--muted); margin: 0 0 32px; }}
  a.talk {{ display: block; text-decoration: none; color: inherit; background: var(--card); border: 1px solid var(--line); border-left: 5px solid var(--accent); border-radius: 10px; padding: 18px 20px; margin-bottom: 14px; }}
  a.talk:hover {{ border-color: var(--accent); }}
  .t {{ font-weight: 700; font-size: 1.2rem; }}
  .s {{ margin-top: 2px; }}
  .m {{ margin-top: 6px; color: var(--muted); font-size: 0.9rem; }}
  footer {{ margin-top: 40px; color: var(--muted); font-size: 0.85rem; }}
  footer a {{ color: inherit; }}
</style>
</head>
<body>
<main>
  <h1>Talks</h1>
  <p class="lede">Slides from talks and webinars. Each deck is a single HTML file, so use the arrow keys to move through it.</p>
{cards}
  <footer>Built with <a href="https://github.com/panyam/slyds">slyds</a>. Source on <a href="https://github.com/panyam/talks">GitHub</a>.</footer>
</main>
</body>
</html>
"""


def card(slug, meta):
    bits = [b for b in (meta.get("event"), meta.get("date")) if b]
    return (
        f'  <a class="talk" href="{slug}/">'
        f'<div class="t">{html.escape(meta.get("title", slug))}</div>'
        + (f'<div class="s">{html.escape(meta["subtitle"])}</div>' if meta.get("subtitle") else "")
        + (f'<div class="m">{html.escape(" · ".join(bits))}</div>' if bits else "")
        + "</a>"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slyds", default="slyds")
    ap.add_argument("--keep-notes", action="store_true", help="publish speaker notes too")
    args = ap.parse_args()

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / ".nojekyll").touch()

    talks = sorted(p.parent for p in ROOT.glob("*/talk.yaml"))
    if not talks:
        sys.exit("no talks found (looking for */talk.yaml)")
    cards = []
    for folder in talks:
        meta = read_talk_yaml(folder / "talk.yaml")
        n = build_talk(folder, args.slyds, args.keep_notes)
        print(f"{folder.name}: built, {n} notes blocks stripped")
        cards.append(card(folder.name, meta))
    (SITE / "index.html").write_text(INDEX.format(cards="\n".join(cards)))
    print(f"site/index.html: {len(talks)} talk(s)")


if __name__ == "__main__":
    main()
