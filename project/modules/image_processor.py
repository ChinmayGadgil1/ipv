"""
Image Processing Module
Handles image preprocessing, edge detection, and histogram analysis
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class ImageProcessor:
    """
    Handles all image preprocessing and edge detection operations
    """
    
    def __init__(self, image_path: str):
        """
        Initialize ImageProcessor with an image
        
        Args:
            image_path (str): Path to the image file
            
        Raises:
            FileNotFoundError: If image file not found
            ValueError: If image cannot be read
        """
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError(f"Cannot read image from {image_path}")
        
        self.image_height, self.image_width = self.original_image.shape[:2]
        self.grayscale = None
        self.edges = None
        self.blurred = None
        
    def preprocess(self) -> np.ndarray:
        """
        Preprocess image: convert to grayscale and apply Gaussian blur
        
        Returns:
            np.ndarray: Preprocessed grayscale blurred image
        """
        # Convert to grayscale
        self.grayscale = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur
        self.blurred = cv2.GaussianBlur(self.grayscale, (5, 5), 1.0)
        
        return self.blurred
    
    def detect_edges(self, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
        """
        Apply Canny edge detection on preprocessed image
        
        Args:
            threshold1 (int): Lower threshold for Canny edge detection
            threshold2 (int): Upper threshold for Canny edge detection
            
        Returns:
            np.ndarray: Edge map (binary image)
        """
        if self.blurred is None:
            self.preprocess()
        
        # Apply Canny edge detection
        self.edges = cv2.Canny(self.blurred, threshold1, threshold2)
        
        # Dilate edges to create embedding regions
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.edges = cv2.dilate(self.edges, kernel, iterations=1)
        
        return self.edges
    
    def create_embedding_mask(self) -> np.ndarray:
        """
        Create adaptive embedding mask from edge detection results
        
        Returns:
            np.ndarray: Binary mask for embedding (1 for embedding regions, 0 otherwise)
        """
        if self.edges is None:
            self.detect_edges()
        
        # Normalize edges to 0-1 range
        mask = (self.edges > 0).astype(np.uint8)
        
        return mask
    
    def get_embedding_capacity(self, mask: np.ndarray) -> int:
        """
        Calculate how many bytes can be embedded in the edge regions
        
        Args:
            mask (np.ndarray): Embedding mask
            
        Returns:
            int: Maximum bytes that can be embedded (each edge pixel can hold 3 bytes in RGB)
        """
        # Count edge pixels
        edge_pixels = np.sum(mask > 0)
        
        # Each pixel has 3 channels (RGB), each channel can hold 1 byte
        # Total capacity = edge_pixels * 3
        capacity = edge_pixels * 3
        
        return capacity
    
    def calculate_histogram(self, image: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate histogram for an image
        
        Args:
            image (np.ndarray, optional): Image to compute histogram for. If None, uses original image.
            
        Returns:
            Tuple: (hist_b, hist_g, hist_r) - Histograms for each channel
        """
        if image is None:
            image = self.original_image
        
        # Calculate histogram for each channel
        hist_b = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([image], [2], None, [256], [0, 256])
        
        return hist_b, hist_g, hist_r
    
    def get_image_dimensions(self) -> Tuple[int, int]:
        """
        Get image dimensions
        
        Returns:
            Tuple: (height, width)
        """
        return self.image_height, self.image_width
    
    def get_original_image(self) -> np.ndarray:
        """
        Get original image
        
        Returns:
            np.ndarray: Original image
        """
        return self.original_image.copy()
    
    def get_grayscale_image(self) -> np.ndarray:
        """
        Get grayscale image
        
        Returns:
            np.ndarray: Grayscale image
        """
        if self.grayscale is None:
            self.preprocess()
        return self.grayscale.copy()
    
    def get_edge_map(self) -> np.ndarray:
        """
        Get edge map
        
        Returns:
            np.ndarray: Edge map
        """
        if self.edges is None:
            self.detect_edges()
        return self.edges.copy()
