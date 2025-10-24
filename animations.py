"""
Animation utilities for PixelMorph application.
Provides smooth UI animations using PyQt5 property animations.
"""
from typing import Optional
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QRect
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect


def create_fade_in_animation(widget: QWidget, duration: int = 1000) -> QPropertyAnimation:
    """
    Create fade-in animation for a widget with opacity effect.
    
    Args:
        widget: Target widget for animation
        duration: Animation duration in milliseconds
        
    Returns:
        QPropertyAnimation object ready to start
    """
    opacity_effect = widget.graphicsEffect()
    if not opacity_effect:
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
    
    animation = QPropertyAnimation(opacity_effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    return animation


def create_fade_out_animation(widget: QWidget, duration: int = 1000) -> QPropertyAnimation:
    """
    Create fade-out animation for a widget with opacity effect.
    
    Args:
        widget: Target widget for animation
        duration: Animation duration in milliseconds
        
    Returns:
        QPropertyAnimation object ready to start
    """
    opacity_effect = widget.graphicsEffect()
    if not opacity_effect:
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
    
    animation = QPropertyAnimation(opacity_effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    return animation


def create_button_click_animation(button: QWidget, scale_factor: float = 1.1) -> QPropertyAnimation:
    """
    Create button click animation with scaling effect.
    
    Args:
        button: Target button widget
        scale_factor: Scale multiplier for the animation
        
    Returns:
        QPropertyAnimation object ready to start
    """
    original_geometry = button.geometry()
    scaled_geometry = _calculate_scaled_geometry(original_geometry, scale_factor)
    
    animation = QPropertyAnimation(button, b"geometry")
    animation.setDuration(150)
    animation.setStartValue(original_geometry)
    animation.setEndValue(scaled_geometry)
    animation.setEasingCurve(QEasingCurve.OutBounce)
    
    # Return to original size after animation
    def reset_geometry():
        button.setGeometry(original_geometry)
    
    animation.finished.connect(reset_geometry)
    return animation


def create_slide_animation(widget: QWidget, start_pos: QPoint, end_pos: QPoint, 
                          duration: int = 500) -> QPropertyAnimation:
    """
    Create slide animation for moving a widget between positions.
    
    Args:
        widget: Target widget for animation
        start_pos: Starting position
        end_pos: Ending position
        duration: Animation duration in milliseconds
        
    Returns:
        QPropertyAnimation object ready to start
    """
    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    return animation


def _calculate_scaled_geometry(original: QRect, scale_factor: float) -> QRect:
    """Calculate scaled geometry maintaining center position."""
    center = original.center()
    new_width = int(original.width() * scale_factor)
    new_height = int(original.height() * scale_factor)
    
    new_x = center.x() - new_width // 2
    new_y = center.y() - new_height // 2
    
    return QRect(new_x, new_y, new_width, new_height)


# Legacy function wrappers for backward compatibility
def fade_in_animation(widget: QWidget, duration: int = 1000) -> None:
    """Legacy wrapper for fade-in animation."""
    animation = create_fade_in_animation(widget, duration)
    animation.start()


def fade_out_animation(widget: QWidget, duration: int = 1000) -> None:
    """Legacy wrapper for fade-out animation."""
    animation = create_fade_out_animation(widget, duration)
    animation.start()


def button_click_animation(button: QWidget) -> None:
    """Legacy wrapper for button click animation."""
    animation = create_button_click_animation(button)
    animation.start()


def slide_in_animation(widget: QWidget, start_pos: QPoint, end_pos: QPoint, 
                      duration: int = 500) -> None:
    """Legacy wrapper for slide animation."""
    animation = create_slide_animation(widget, start_pos, end_pos, duration)
    animation.start()