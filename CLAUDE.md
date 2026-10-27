# talks

Slides for talks and webinars, published to https://panyam.github.io/talks/. Each talk is a
[slyds](https://github.com/panyam/slyds) deck in its own top-level folder. See README.md for the
talk list.

## Commands

```bash
make present TALK=code-got-cheap   # presenter view with speaker notes (N opens them, T starts the timer)
make site                          # build every */talk.yaml deck into site/, notes stripped, plus index.html
make serve                         # preview the public site on :3000
make new TITLE="My Talk" TALK=my-talk
slyds check <talk>                 # validate a deck after edits
```

`make site SLYDS=~/projects/slyds/main/slyds` uses a local slyds build. CI pins slyds v0.2.10
(`.github/workflows/pages.yml`); bump it there when a newer release is needed.

## Layout

- `<talk>/talk.yaml`: title, subtitle, event, date for the index page. A folder without one isn't published.
- `<talk>/slides/NN-name.html`: one slide per file. Order lives in `index.html` and `.slyds.yaml`; change it with `slyds add/mv/rm`, not by hand.
- `<talk>/theme.css`: deck-specific styles, appended per slide feature with a comment header.
- `<talk>/notes/`: research and sources for the talk (not part of the deck).
- `scripts/build-site.py`: builds each deck, strips `.speaker-notes` and the notes button, writes the index.

## Conventions

- **Speaker notes are public in the source** (this repo is public) but stripped from the published site. Don't put anything in notes you wouldn't want read on GitHub.
- **Click-to-reveal**: add `class="step"` to any element. `code-got-cheap/steps.js` handles it and is loaded from a slide file (`<script src="steps.js">`) so `slyds update` leaves it alone. Upstream: panyam/slyds#5. Items that should stay visible and only change state (ticks, filling bars) use `step` plus a class that overrides `opacity`/`transform`.
- **Cartoons are original inline SVG** using theme variables (`var(--slyds-fg)` etc.) so they work in both themes. Third-party cartoons only with a link and licence credit (xkcd is CC BY-NC).
- **Every stat links to its primary source** on the slide (`.src` floater) and on the sources slide. Secondary coverage often misquotes; check the publisher's page before using a number.
- **Prose**: no antithesis-plus-reveal taglines ("X got cheap. Y got expensive. Everything hangs off that."), no em-dashes. Run the ai-tell-sweep / prose-pass skills on slide text.

## Gotchas

- Inserting slides shifts every "slide N" reference in notes and the sources slide. After `slyds add --after`, grep for `[Ss]lides\? [0-9]` and re-check each against `ls slides`.
- `slyds serve` doesn't bust the browser's CSS cache. If new styles don't show (SVGs render solid black), hard-refresh.
- Fixed light colours (cards, "paper" backgrounds) break the dark theme. Use `color-mix()` with theme variables, or set explicit text colours on that element.
- `.slide p` / `.slide li` set font sizes, so a bare class selector loses on specificity. Write `.slide p.myclass`.
- `.slide-floater` has `pointer-events: none`; links inside it need `pointer-events: auto` (already set for `.src a`).
