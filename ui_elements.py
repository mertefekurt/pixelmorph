"""
UI elements for PixelMorph application.
Provides the main application window with enhanced user interface.
"""
from typing import Callable, Optional
from PyQt5.QtCore import Qt, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QWidget, QGraphicsOpacityEffect, QComboBox, 
    QProgressBar, QMessageBox, QSizePolicy
)

from animations import create_fade_in_animation
from image_loader import load_image
from image_processor import process_image
from image_saver import save_image as save_image_func


class ImageProcessingThread(QThread):
    """Background thread for image processing to keep UI responsive."""
    finished = pyqtSignal(object)
    progress = pyqtSignal(int)
    
    def __init__(self, image_path: str, sort_method: str):
        super().__init__()
        self.image_path = image_path
        self.sort_method = sort_method
    
    def run(self) -> None:
        """Process image in background thread."""
        self.progress.emit(25)
        processed_image = process_image(self.image_path, self.sort_method)
        self.progress.emit(100)
        self.finished.emit(processed_image)


class PixelMorphApp(QMainWindow):
    """Main application window for PixelMorph."""
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_widgets()
        self._setup_layout()
        self._setup_animations()
        self._initialize_state()

    def _setup_window(self) -> None:
        """Configure main window properties."""
        self.setWindowTitle("PixelMorph - Advanced Image Pixel Sorter")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)

    def _create_widgets(self) -> None:
        """Create all UI widgets."""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Title
        self.title_label = QLabel("PixelMorph", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #2c3e50;
            margin: 20px;
            padding: 10px;
        """)

        # Subtitle
        self.subtitle_label = QLabel("Advanced Image Pixel Sorting", self)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setFont(QFont("Arial", 14))
        self.subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")

        # Image display
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(400)
        self.image_label.setMinimumWidth(600)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #bdc3c7;
                border-radius: 10px;
                background-color: white;
                margin: 10px;
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        self.image_label.setText("No image loaded")

        # Sorting method selection
        self.sort_method_label = QLabel("Sorting Method:", self)
        self.sort_method_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.sort_method_combo = QComboBox(self)
        self.sort_method_combo.addItems([
            "Vertical (Column-wise)",
            "Horizontal (Row-wise)", 
            "Global Brightness"
        ])
        self.sort_method_combo.setStyleSheet(self._get_combo_style())

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(self._get_progress_style())

        # Buttons
        self.load_button = self._create_button(
            "📁 Load Image", "#27ae60", "#229954", self.load_image
        )
        
        self.sort_button = self._create_button(
            "🎨 Sort Pixels", "#3498db", "#2980b9", self.sort_pixels
        )
        self.sort_button.setEnabled(False)
        
        self.save_button = self._create_button(
            "💾 Save Image", "#e67e22", "#d35400", self.save_image
        )
        self.save_button.setEnabled(False)

    def _setup_layout(self) -> None:
        """Setup widget layout."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 20, 30, 20)

        # Header
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        # Image area
        main_layout.addWidget(self.image_label, 1)

        # Sorting options
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(self.sort_method_label)
        sort_layout.addWidget(self.sort_method_combo)
        sort_layout.addStretch()
        main_layout.addLayout(sort_layout)

        # Progress bar
        main_layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)

    def _setup_animations(self) -> None:
        """Initialize animations and effects."""
        self.opacity_effect = QGraphicsOpacityEffect(self.image_label)
        self.opacity_effect.setOpacity(1.0)
        self.image_label.setGraphicsEffect(self.opacity_effect)

    def _initialize_state(self) -> None:
        """Initialize application state."""
        self.image_path: Optional[str] = None
        self.current_image: Optional[QPixmap] = None
        self.processing_thread: Optional[ImageProcessingThread] = None
        self._fade_in_anim: Optional[QPropertyAnimation] = None

    def load_image(self) -> None:
        """Load image from file dialog."""
        self.image_path, loaded_image = load_image(self)
        
        if loaded_image and not loaded_image.isNull():
            self.current_image = loaded_image
            self.image_label.setText("")  # Clear the "No image loaded" text first
            self._display_image(loaded_image)
            self.sort_button.setEnabled(True)
            
            # Animate image appearance (persist reference to avoid GC)
            if self._fade_in_anim:
                self._fade_in_anim.stop()
            self._fade_in_anim = create_fade_in_animation(self.image_label, 800)
            self._fade_in_anim.finished.connect(lambda: self.opacity_effect.setOpacity(1.0))
            self._fade_in_anim.start()
        else:
            self._show_message("Error", "Failed to load image. Please try another file.", QMessageBox.Warning)

    def sort_pixels(self) -> None:
        """Sort pixels using selected method."""
        if not self.image_path:
            return

        # Get selected sorting method
        method_map = {
            0: "vertical",
            1: "horizontal", 
            2: "brightness"
        }
        sort_method = method_map.get(self.sort_method_combo.currentIndex(), "vertical")

        # Show progress and disable buttons
        self._set_processing_state(True)

        # Start background processing
        self.processing_thread = ImageProcessingThread(self.image_path, sort_method)
        self.processing_thread.progress.connect(self.progress_bar.setValue)
        self.processing_thread.finished.connect(self._on_processing_finished)
        self.processing_thread.start()

    def _on_processing_finished(self, processed_image: object) -> None:
        """Handle completion of image processing."""
        self._set_processing_state(False)
        
        if processed_image:
            self.current_image = QPixmap.fromImage(processed_image)
            self._display_image(self.current_image)
            self.save_button.setEnabled(True)
            self._show_message("Success", "Image processing completed!", QMessageBox.Information)
        else:
            self._show_message("Error", "Failed to process image. Please try again.", QMessageBox.Critical)

    def save_image(self) -> None:
        """Save current image to file."""
        if self.current_image:
            success = save_image_func(self.current_image, self)
            if not success:
                self._show_message("Error", "Failed to save image.", QMessageBox.Warning)

    def _display_image(self, image: QPixmap) -> None:
        """Display image in the label with proper scaling."""
        if image and not image.isNull():
            # Clear any existing text
            self.image_label.clear()
            
            # Get the current size of the image label
            label_size = self.image_label.size()
            
            # If the label hasn't been properly sized yet, use minimum dimensions
            if label_size.width() <= 100 or label_size.height() <= 100:
                label_size.setWidth(600)
                label_size.setHeight(400)
            
            # Scale the image to fit within the label while maintaining aspect ratio
            scaled_image = image.scaled(
                label_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # Set the pixmap and ensure it's displayed
            self.image_label.setPixmap(scaled_image)
            self.image_label.setScaledContents(False)
            
            # Update the widget to ensure it redraws
            self.image_label.update()

    def _set_processing_state(self, processing: bool) -> None:
        """Update UI state during processing."""
        self.progress_bar.setVisible(processing)
        self.load_button.setEnabled(not processing)
        self.sort_button.setEnabled(not processing and self.image_path is not None)
        self.save_button.setEnabled(not processing and self.current_image is not None)
        
        if processing:
            self.progress_bar.setValue(0)

    def resizeEvent(self, event) -> None:
        """Ensure image preview scales with window resize."""
        super().resizeEvent(event)
        if self.current_image and not self.current_image.isNull():
            self._display_image(self.current_image)

    def _create_button(self, text: str, base_color: str, hover_color: str,
                       callback: Callable[[], None]) -> QPushButton:
        """Create styled button with hover effects."""
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setFont(QFont("Arial", 12, QFont.Bold))
        button.setMinimumHeight(45)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                color: #7f8c8d;
            }}
        """)
        return button

    def _get_combo_style(self) -> str:
        """Get ComboBox stylesheet."""
        return """
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
            }
        """

    def _get_progress_style(self) -> str:
        """Get ProgressBar stylesheet."""
        return """
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """

    def _show_message(self, title: str, message: str, icon_type) -> None:
        """Show message dialog to user."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        msg_box.exec_()
