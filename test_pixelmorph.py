"""
Basic tests for PixelMorph application.
Tests core functionality and image processing algorithms.
"""
import unittest
import tempfile
import os
from PIL import Image
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

from image_processor import process_image, _sort_pixels_vertically, _sort_pixels_horizontally
from image_loader import load_image
from image_saver import save_image


class TestImageProcessor(unittest.TestCase):
    """Test image processing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test image
        self.test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        
        # Save test image
        pil_image = Image.fromarray(self.test_image)
        pil_image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        os.rmdir(self.temp_dir)
    
    def test_vertical_sorting(self):
        """Test vertical pixel sorting."""
        sorted_pixels = _sort_pixels_vertically(self.test_image.copy())
        
        # Check that dimensions are preserved
        self.assertEqual(sorted_pixels.shape, self.test_image.shape)
        
        # Check that sorting actually occurred (brightness should be sorted in each column)
        for x in range(sorted_pixels.shape[1]):
            column = sorted_pixels[:, x, :]
            brightness = np.sum(column, axis=1)
            self.assertTrue(np.all(brightness[:-1] <= brightness[1:]))
    
    def test_horizontal_sorting(self):
        """Test horizontal pixel sorting."""
        sorted_pixels = _sort_pixels_horizontally(self.test_image.copy())
        
        # Check that dimensions are preserved
        self.assertEqual(sorted_pixels.shape, self.test_image.shape)
        
        # Check that sorting actually occurred (brightness should be sorted in each row)
        for y in range(sorted_pixels.shape[0]):
            row = sorted_pixels[y, :, :]
            brightness = np.sum(row, axis=1)
            self.assertTrue(np.all(brightness[:-1] <= brightness[1:]))
    
    def test_process_image_vertical(self):
        """Test image processing with vertical sorting."""
        result = process_image(self.test_image_path, "vertical")
        self.assertIsNotNone(result)
    
    def test_process_image_horizontal(self):
        """Test image processing with horizontal sorting."""
        result = process_image(self.test_image_path, "horizontal")
        self.assertIsNotNone(result)
    
    def test_process_image_brightness(self):
        """Test image processing with brightness sorting."""
        result = process_image(self.test_image_path, "brightness")
        self.assertIsNotNone(result)
    
    def test_process_invalid_image(self):
        """Test processing with invalid image path."""
        result = process_image("nonexistent_file.png", "vertical")
        self.assertIsNone(result)


class TestImageOperations(unittest.TestCase):
    """Test image loading and saving operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])
        
        # Create test image
        self.test_image = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        
        pil_image = Image.fromarray(self.test_image)
        pil_image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        os.rmdir(self.temp_dir)
    
    def test_pixmap_creation(self):
        """Test QPixmap creation from file."""
        pixmap = QPixmap(self.test_image_path)
        self.assertFalse(pixmap.isNull())
        self.assertEqual(pixmap.width(), 50)
        self.assertEqual(pixmap.height(), 50)


class TestApplicationIntegration(unittest.TestCase):
    """Test application integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])
    
    def test_import_modules(self):
        """Test that all modules can be imported successfully."""
        try:
            import main
            import ui_elements
            import image_loader
            import image_processor
            import image_saver
            import animations
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")
    
    def test_application_creation(self):
        """Test that the main application can be created."""
        try:
            from ui_elements import PixelMorphApp
            app = PixelMorphApp()
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"Failed to create application: {e}")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)