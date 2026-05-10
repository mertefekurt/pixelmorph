"""
Image loading functionality for PixelMorph application.
Handles file dialog operations and image loading with proper error handling.
"""
from typing import Optional, Tuple
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import QPixmap


def load_image(parent_widget: QWidget) -> Tuple[Optional[str], Optional[QPixmap]]:
    """
    Open file dialog to select and load an image file.
    
    Args:
        parent_widget: Parent widget for the file dialog
        
    Returns:
        Tuple containing file path and QPixmap object, or (None, None) if cancelled
    """
    file_path, _ = QFileDialog.getOpenFileName(
        parent_widget, 
        "Select Image", 
        "", 
        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
    )

    if file_path:
        try:
            image = QPixmap(file_path)
            if image.isNull():
                return None, None
            return file_path, image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None, None
    
    return None, None
