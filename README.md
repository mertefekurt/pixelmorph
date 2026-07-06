# PixelMorph

![PixelMorph cover](assets/readme-cover.svg)

PixelMorph is a PyQt5 desktop image tool for pixel-sorting effects. It loads an image, sorts pixels vertically, horizontally, or by global brightness, then lets you save the transformed result.

## Run

```bash
git clone https://github.com/mertefekurt/pixelmorph.git
cd pixelmorph
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Features

- PyQt5 interface for loading and previewing images
- vertical, horizontal, and brightness-based sorting
- Pillow and NumPy processing pipeline
- save flow for processed images

## Files

```text
main.py             application entry point
ui_elements.py      PyQt5 window and controls
image_loader.py     image selection helpers
image_processor.py  pixel sorting algorithms
image_saver.py      output writing
animations.py       small interface animations
```
