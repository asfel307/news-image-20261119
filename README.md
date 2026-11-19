# The World in One Day — Thursday, 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/asfel307/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/asfel307/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for the [make.fun bounty "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119): a 1024×1024 front-page infographic of Thursday 19 November 2026, drawn programmatically with PIL so every letter is crisp.

## The day's news

- **Lead — gaming:** Grand Theft Auto VI unlocks worldwide after 13 years, rolling out at midnight in each market from New Zealand; early reviews score 99 on Metacritic, and Sensor Tower counts about 16 million copies already sold (Reuters, AP, 19 Nov).
- **Diplomacy — Shenzhen:** Trump, Xi and Putin hold their first-ever trilateral meeting on the sidelines of the APEC summit, with nuclear arms and Ukraine on the table (Yonhap, Reuters, 19 Nov).
- **US politics:** House Democrats nominate Hakeem Jeffries for Speaker by 251–11; the full House votes on 3 January, and he would be the first Black Speaker (AP, NPR).
- **Weather — India:** Severe Cyclone Akvan nears India's east coast; red alerts and school closures in Odisha, landfall due Friday (IMD, The Hindu, 19 Nov).
- **Space — NASA:** NASA marks Voyager 1 reaching one light-day from Earth — a radio signal now takes a full day to reach the probe (NASA, Reuters).
- **Asia — defence:** India and Japan hold their fourth 2+2 foreign and defence ministers' dialogue in Tokyo (PIB, The Hindu, 19 Nov).

Every story happened, or was first reported, on Thursday 19 November 2026; sources are listed on the image itself.

## How to run

```sh
# Re-draw the image (needs Pillow, only for the build step):
python3 render.py

# The entry program (Python 3.13, standard library only):
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` copies the repository's `entry.png` to the output directory, so both grading runs write identical bytes. The image is a whole PNG, 1024×1024, under 1 MiB.

## License

MIT — see [LICENSE](LICENSE).
