"""
Image saving functionality for PixelMorph application.
Handles file dialog operations and image saving with proper error handling.
"""
from typing import Optional
from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap


def save_image(image: Optional[QPixmap], parent_widget: QWidget) -> bool:
    """
    Open file dialog to save an image file.
    
    Args:
        image: QPixmap object to save
        parent_widget: Parent widget for the file dialog
        
    Returns:
        True if image was saved successfully, False otherwise
    """
    if not image or image.isNull():
        _show_error_message(parent_widget, "No image to save")
        return False

    save_path, selected_filter = QFileDialog.getSaveFileName(
        parent_widget, 
        "Save Image", 
        "", 
        "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
    )

    if save_path:
        try:
            image_format = _determine_format(save_path, selected_filter)
            success = image.save(save_path, image_format)
            
            if success:
                _show_success_message(parent_widget, f"Image saved successfully to {save_path}")
                return True
            else:
                _show_error_message(parent_widget, "Failed to save image")
                return False
                
        except Exception as e:
            _show_error_message(parent_widget, f"Error saving image: {e}")
            return False
    
    return False


def _determine_format(file_path: str, selected_filter: str) -> str:
    """Determine image format from file path or selected filter."""
    if "PNG" in selected_filter or file_path.lower().endswith('.png'):
        return "PNG"
    if "JPEG" in selected_filter or file_path.lower().endswith(('.jpg', '.jpeg')):
        return "JPEG"
    if "BMP" in selected_filter or file_path.lower().endswith('.bmp'):
        return "BMP"
    return "PNG"


def _show_success_message(parent: QWidget, message: str) -> None:
    """Show success message to user."""
    QMessageBox.information(parent, "Success", message)


def _show_error_message(parent: QWidget, message: str) -> None:
    """Show error message to user."""
    QMessageBox.critical(parent, "Error", message)
