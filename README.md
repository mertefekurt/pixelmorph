# PixelMorph

![PixelMorph cover](assets/readme-cover.svg)

PyQt5 desktop image tool for pixel sorting. It loads an image, sorts pixels vertically, horizontally, or by global brightness, and saves the transformed result.

## Run

```bash
git clone https://github.com/mertefekurt/pixelmorph.git
cd pixelmorph
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## File tour

```text
main.py             app entry
ui_elements.py      window and controls
image_processor.py  sorting algorithms
image_loader.py     input flow
image_saver.py      output flow
animations.py       interface motion helpers
```
