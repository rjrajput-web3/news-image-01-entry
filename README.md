# news-image-01 entry: The World in One Day

A program that writes one image summing up the world's news of Friday
13 November 2026 — a newspaper front page drawn with Pillow, held in this
repository as `entry.png` and copied to the output directory by `main.py`.

## What the image shows

- **Lead story:** four tankers hit in the Strait of Hormuz; Iran says it
  destroyed a US radar in Bahrain.
- **Ukraine:** Europe wins a seat at the Ukraine peace talks; the largest
  prisoner swap of the war is in the works.
- **Tech:** Nvidia chief Jensen Huang resigns; Colette Kress takes over.
- **Asia:** Taiwan details China's unannounced Pacific naval drills.
- **Energy:** the IEA forecasts an oil surplus despite the Gulf danger.
- **Technology:** a Microsoft outage hits Outlook in 74 countries.
- **Crime:** the US moves to seize $1.2bn from the Binance hack.
- **Also:** Pope Leo in Peru, the Brooklyn collapse toll, the measles
  ruling, Storm Charles in Portugal.

Every headline is drawn from what was reported on 13 November 2026, with
claims attributed where the reporting attributed them.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program is Python 3.13, standard library only, and runs with no
network: it copies `entry.png` (1024x1024 PNG, 112,720 bytes) to
`$MAKEFUN_OUTPUT_DIR/entry.png`, then checks the copy is a whole PNG
within the competition's limits. Two runs write identical bytes.

To regenerate the image from scratch (needs Pillow and the DejaVu fonts):

```sh
python3 render.py
```

## Entry

Competition: **news-image-01** — "Sum up 13 November's world news in one
image" ($250 shared by the top 100, make.fun).
