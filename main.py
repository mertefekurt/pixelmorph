"""
PixelMorph - Image Pixel Sorter Application
Entry point for the PyQt5-based image processing application.
"""
import sys
from PyQt5.QtWidgets import QApplication

from ui_elements import PixelMorphApp


def main() -> None:
    """Initialize and run the PixelMorph application."""
    app = QApplication(sys.argv)
    window = PixelMorphApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()