"""
Image processing functionality for PixelMorph application.
Provides pixel sorting algorithms with optimized performance.
"""
from typing import Optional
import numpy as np
from PIL import Image
from PyQt5.QtGui import QImage


def process_image(image_path: str, sort_method: str = "vertical") -> Optional[QImage]:
    """
    Process image by sorting pixels using specified method.
    
    Args:
        image_path: Path to the input image file
        sort_method: Sorting method ("vertical", "horizontal", "brightness")
        
    Returns:
        QImage object with sorted pixels, or None if processing fails
    """
    try:
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            pixels = np.array(image, dtype=np.uint8)

            if sort_method == "vertical":
                sorted_pixels = _sort_pixels_vertically(pixels)
            elif sort_method == "horizontal":
                sorted_pixels = _sort_pixels_horizontally(pixels)
            elif sort_method == "brightness":
                sorted_pixels = _sort_pixels_by_brightness(pixels)
            else:
                sorted_pixels = _sort_pixels_vertically(pixels)

            sorted_image = Image.fromarray(sorted_pixels)
            return _convert_to_qimage(sorted_image)

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def _sort_pixels_vertically(pixels: np.ndarray) -> np.ndarray:
    """Sort pixels vertically by brightness within each column."""
    width = pixels.shape[1]
    sorted_pixels = pixels.copy()

    for x in range(width):
        column_pixels = pixels[:, x, :]
        brightness = np.sum(column_pixels, axis=1)
        sorted_indices = np.argsort(brightness)
        sorted_pixels[:, x, :] = column_pixels[sorted_indices]

    return sorted_pixels


def _sort_pixels_horizontally(pixels: np.ndarray) -> np.ndarray:
    """Sort pixels horizontally by brightness within each row."""
    height = pixels.shape[0]
    sorted_pixels = pixels.copy()

    for y in range(height):
        row_pixels = pixels[y, :, :]
        brightness = np.sum(row_pixels, axis=1)
        sorted_indices = np.argsort(brightness)
        sorted_pixels[y, :, :] = row_pixels[sorted_indices]

    return sorted_pixels


def _sort_pixels_by_brightness(pixels: np.ndarray) -> np.ndarray:
    """Sort all pixels by brightness globally."""
    height, width, channels = pixels.shape
    flat_pixels = pixels.reshape(-1, channels)
    brightness = np.sum(flat_pixels, axis=1)
    sorted_indices = np.argsort(brightness)
    sorted_flat = flat_pixels[sorted_indices]
    return sorted_flat.reshape(height, width, channels)


def _convert_to_qimage(pil_image: Image.Image) -> QImage:
    """Convert PIL Image to QImage format."""
    return QImage(
        pil_image.tobytes(),
        pil_image.width,
        pil_image.height,
        pil_image.width * 3,
        QImage.Format_RGB888
    )
