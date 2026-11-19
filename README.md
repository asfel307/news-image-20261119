# The World in One Day — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/asfel307/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/asfel307/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday, 19 November 2026:
a masthead with the date, a lead story on the global launch of GTA VI,
and five more stories from diplomacy, politics, weather, space and Asia.

## The six stories

1. **GTA VI launches worldwide** — unlocks at midnight in each market,
   starting in New Zealand, 13 years after GTA V; early reviews give it
   99 on Metacritic. *(Reuters, AP)*
2. **Trump, Xi and Putin meet in Shenzhen** — the first three-way talks,
   held on the APEC sidelines, with nuclear arms and Ukraine on the
   agenda. *(Yonhap, Reuters)*
3. **Jeffries nominated as Speaker** — House Democrats pick Hakeem
   Jeffries 251–11; the full House votes on 3 January, when he would
   become the first Black Speaker. *(AP, NPR)*
4. **Cyclone Akvan nears India** — a severe storm under a red alert,
   with schools shut in Odisha; landfall expected Friday. *(IMD,
   The Hindu)*
5. **Voyager 1 reaches one light-day** — NASA marks the milestone
   today for the farthest human-made object from Earth. *(NASA, Reuters)*
6. **India–Japan 2+2 talks in Tokyo** — the foreign and defence
   ministers discuss defence ties and a free Indo-Pacific. *(PIB,
   The Hindu)*

Every story is drawn as its own card with a small pictogram, and the
sources are listed in the footer of the image.

## How it is built

`render.py` draws the whole 1024×1024 infographic from scratch with
Pillow (no network, no downloaded assets) and saves it as `entry.png`.
`main.py` is the competition entry point: it copies `entry.png` next to
it into `$MAKEFUN_OUTPUT_DIR` (or `/output` when that variable is
unset), so both grading runs write identical bytes.

## Running it

```sh
python3 render.py          # redraw entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy entry.png into out/
```

Requirements: Python 3.13 (standard library only for `main.py`) and
Pillow plus the DejaVu fonts for `render.py`.

## License

MIT — see `LICENSE`.
