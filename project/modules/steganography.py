"""
Steganography Module
Handles adaptive LSB embedding and extraction of encrypted data
Robust approach: Uses deterministic grid-based embedding independent of edge detection
"""

import numpy as np
import struct
from typing import Tuple, List


class AdaptiveSteganography:
    """
    Implements robust LSB steganography using grid-based pixel selection
    """
    
    GRID_STEP = 2  # Embed in every nth pixel for better imperceptibility
    
    @staticmethod
    def _get_embedding_pixels(image: np.ndarray, mask: np.ndarray = None) -> List[Tuple[int, int]]:
        """
        Get deterministic list of pixels for embedding using pure grid-based selection
        NO edge prioritization during extraction - completely reproducible
        
        Args:
            image (np.ndarray): Original image
            mask (np.ndarray): Ignored - kept for API compatibility
            
        Returns:
            List of (y, x) coordinates in deterministic order
        """
        height, width = image.shape[:2]
        pixels = []
        
        # Pure grid-based selection - deterministic and independent of edge detection
        for y in range(0, height, AdaptiveSteganography.GRID_STEP):
            for x in range(0, width, AdaptiveSteganography.GRID_STEP):
                pixels.append((y, x))
        
        return pixels
    
    @staticmethod
    def embed_data(image: np.ndarray, encrypted_data: bytes, mask: np.ndarray) -> Tuple[np.ndarray, bool]:
        """
        Embed encrypted data into image using robust grid-based LSB
        Deterministic pixel selection ensures extraction works reliably
        
        Args:
            image (np.ndarray): Original image (BGR format)
            encrypted_data (bytes): Encrypted data to embed
            mask (np.ndarray): Binary mask indicating edge regions (for prioritization)
            
        Returns:
            Tuple: (stego_image, success) - Modified image and success flag
        """
        stego_image = image.copy()
        
        # Get deterministic pixel list
        pixels = AdaptiveSteganography._get_embedding_pixels(image, mask)
        
        if len(pixels) == 0:
            return stego_image, False
        
        # Calculate maximum capacity (3 bits per pixel: R, G, B LSBs)
        max_bits = len(pixels) * 3
        max_capacity = max_bits // 8
        
        # Create data with length header
        # Store: data_length (4 bytes) + encrypted_data
        full_data = struct.pack('>I', len(encrypted_data)) + encrypted_data
        
        if len(full_data) > max_capacity:
            return stego_image, False
        
        # Convert to bit stream
        bit_stream = ''.join(format(byte, '08b') for byte in full_data)
        
        # Embed bits in grid pixels using LSB
        bit_index = 0
        for y, x in pixels:
            if bit_index >= len(bit_stream):
                break
            
            # Embed in all 3 channels (BGR)
            for channel in range(3):
                if bit_index >= len(bit_stream):
                    break
                
                pixel_value = stego_image[y, x, channel]
                bit = int(bit_stream[bit_index])
                stego_image[y, x, channel] = (pixel_value & 0xFE) | bit
                bit_index += 1
        
        return stego_image, True
    
    @staticmethod
    def extract_data(stego_image: np.ndarray, mask: np.ndarray) -> bytes:
        """
        Extract encrypted data from stego image using same deterministic grid
        
        Args:
            stego_image (np.ndarray): Image containing hidden data
            mask (np.ndarray): Binary mask (only used for reference, not required for extraction)
            
        Returns:
            bytes: Extracted encrypted data
        """
        # Get deterministic pixel list (same as embedding)
        pixels = AdaptiveSteganography._get_embedding_pixels(stego_image, mask)
        
        if len(pixels) == 0:
            return b''
        
        # Extract bits from grid pixels
        bit_stream = ''
        for y, x in pixels:
            for channel in range(3):
                pixel_value = stego_image[y, x, channel]
                bit = pixel_value & 1
                bit_stream += str(bit)
        
        # Extract header
        if len(bit_stream) < 32:  # 4 bytes (data_length) = 32 bits
            return b''
        
        try:
            # Extract data length
            data_length_bits = bit_stream[:32]
            data_length = int(data_length_bits, 2)
            
            # Sanity check on data length
            if data_length == 0 or data_length > 10*1024*1024:  # Max 10MB
                return b''
            
        except (ValueError, IndexError):
            return b''
        
        # Data starts immediately after the 4-byte header
        header_bits = 32
        data_bits_start = header_bits
        data_bits_end = data_bits_start + (data_length * 8)
        
        if len(bit_stream) < data_bits_end:
            # Not enough bits
            return b''
        
        try:
            data_bits = bit_stream[data_bits_start:data_bits_end]
            
            # Convert bits back to bytes
            extracted_data = b''
            for i in range(data_length):
                byte_bits = data_bits[i*8:(i+1)*8]
                if len(byte_bits) != 8:
                    return b''
                byte_value = int(byte_bits, 2)
                extracted_data += bytes([byte_value])
            
            return extracted_data
            
        except (ValueError, IndexError):
            return b''
    
    @staticmethod
    def calculate_capacity(mask: np.ndarray) -> int:
        """
        Calculate embedding capacity in bytes
        Grid-based approach: capacity depends on image dimensions, not edge detection
        
        Args:
            mask (np.ndarray): Binary mask (used to get image dimensions)
            
        Returns:
            int: Maximum bytes that can be embedded
        """
        height, width = mask.shape[:2]
        
        # Count grid pixels
        grid_pixels = 0
        for y in range(0, height, AdaptiveSteganography.GRID_STEP):
            for x in range(0, width, AdaptiveSteganography.GRID_STEP):
                grid_pixels += 1
        
        # Header: 4 bytes (data length) = 32 bits
        header_bits = 32
        
        # Each pixel has 3 channels, each can hold 1 bit (3 bits per pixel)
        available_bits = grid_pixels * 3 - header_bits
        
        # Convert bits to bytes
        capacity = int(available_bits / 8)
        
        return max(0, capacity)
    
    @staticmethod
    def validate_embedding(image: np.ndarray, encrypted_data: bytes, mask: np.ndarray) -> Tuple[bool, str]:
        """
        Validate if data can be embedded
        
        Args:
            image (np.ndarray): Original image
            encrypted_data (bytes): Encrypted data to embed
            mask (np.ndarray): Binary mask
            
        Returns:
            Tuple: (valid, message) - Validity and message
        """
        if image is None:
            return False, "Image not loaded"
        
        if len(encrypted_data) == 0:
            return False, "No data to embed"
        
        capacity = AdaptiveSteganography.calculate_capacity(mask)
        
        # Account for 4-byte header (data length only)
        required_capacity = len(encrypted_data) + 4
        
        if required_capacity > capacity:
            return False, f"Data too large. Required: {required_capacity} bytes, Available: {capacity} bytes"
        
        return True, "Ready to embed"
