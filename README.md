# Talks

Slides from my talks and webinars, published at https://panyam.github.io/talks/.

Each talk is a [slyds](https://github.com/panyam/slyds) deck in its own folder, with one HTML file per slide. The published site strips speaker notes, which are for the presenter, not the audience.

| Talk | Folder |
| --- | --- |
| Code Got Cheap: how AI-assisted coding is changing teams, metrics, hiring and careers | [`code-got-cheap/`](code-got-cheap/) |

## Working on a talk

```bash
make present TALK=code-got-cheap   # serve one deck locally, with speaker notes (N opens them)
make site                          # build every talk into site/ with notes stripped
make serve                         # preview the public site at localhost:3000
make new TITLE="My Talk" TALK=my-talk
```

Each talk folder has a `talk.yaml` with the title, subtitle, event and date shown on the index page. A talk can keep its research and drafts in a `notes/` folder next to the deck.

Pushing to `main` builds the site with slyds v0.2.10 and deploys it to GitHub Pages (`.github/workflows/pages.yml`).
