"""
Metrics Module
Calculates image quality metrics for analysis
"""

import numpy as np
import cv2
from typing import Tuple


class ImageMetrics:
    """
    Calculates various image quality metrics
    """
    
    @staticmethod
    def calculate_mse(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Calculate Mean Squared Error between two images
        
        Args:
            image1 (np.ndarray): First image
            image2 (np.ndarray): Second image
            
        Returns:
            float: Mean Squared Error value
        """
        if image1.shape != image2.shape:
            # Resize image2 to match image1
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        
        # Convert to float
        img1 = image1.astype(np.float32)
        img2 = image2.astype(np.float32)
        
        mse = np.mean((img1 - img2) ** 2)
        
        return float(mse)
    
    @staticmethod
    def calculate_psnr(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Calculate Peak Signal-to-Noise Ratio between two images
        
        Args:
            image1 (np.ndarray): First image
            image2 (np.ndarray): Second image
            
        Returns:
            float: PSNR value in dB
        """
        mse = ImageMetrics.calculate_mse(image1, image2)
        
        if mse == 0:
            return float('inf')
        
        # Maximum pixel value
        max_pixel = 255.0
        
        # Calculate PSNR
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
        return float(psnr)
    
    @staticmethod
    def calculate_ssim(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Calculate Structural Similarity Index (SSIM) between two images
        
        Args:
            image1 (np.ndarray): First image
            image2 (np.ndarray): Second image
            
        Returns:
            float: SSIM value (-1 to 1, where 1 is identical)
        """
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) if len(image1.shape) == 3 else image1
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) if len(image2.shape) == 3 else image2
        
        # Constants
        C1 = 6.5025
        C2 = 58.5225
        
        # Convert to float
        img1 = gray1.astype(np.float32)
        img2 = gray2.astype(np.float32)
        
        # Calculate mean
        mean1 = cv2.blur(img1, (11, 11))
        mean2 = cv2.blur(img2, (11, 11))
        
        # Calculate variance and covariance
        sqr1 = cv2.blur(img1 ** 2, (11, 11))
        sqr2 = cv2.blur(img2 ** 2, (11, 11))
        cross = cv2.blur(img1 * img2, (11, 11))
        
        var1 = sqr1 - mean1 ** 2
        var2 = sqr2 - mean2 ** 2
        cov = cross - mean1 * mean2
        
        # Calculate SSIM
        numerator1 = 2 * mean1 * mean2 + C1
        denominator1 = mean1 ** 2 + mean2 ** 2 + C1
        numerator2 = 2 * cov + C2
        denominator2 = var1 + var2 + C2
        
        ssim_map = (numerator1 * numerator2) / (denominator1 * denominator2)
        
        return float(np.mean(ssim_map))
    
    @staticmethod
    def calculate_bpp(encrypted_data_size: int, image: np.ndarray) -> float:
        """
        Calculate Bits Per Pixel (embedding rate)
        
        Args:
            encrypted_data_size (int): Size of encrypted data in bytes
            image (np.ndarray): Image
            
        Returns:
            float: BPP value
        """
        total_pixels = image.shape[0] * image.shape[1]
        total_bits = encrypted_data_size * 8
        
        if total_pixels == 0:
            return 0.0
        
        bpp = total_bits / total_pixels
        
        return float(bpp)
    
    @staticmethod
    def generate_quality_report(original_image: np.ndarray, stego_image: np.ndarray, 
                                encrypted_data_size: int) -> dict:
        """
        Generate a comprehensive quality analysis report
        
        Args:
            original_image (np.ndarray): Original image
            stego_image (np.ndarray): Stego image with embedded data
            encrypted_data_size (int): Size of embedded encrypted data
            
        Returns:
            dict: Dictionary containing all metrics
        """
        mse = ImageMetrics.calculate_mse(original_image, stego_image)
        psnr = ImageMetrics.calculate_psnr(original_image, stego_image)
        ssim = ImageMetrics.calculate_ssim(original_image, stego_image)
        bpp = ImageMetrics.calculate_bpp(encrypted_data_size, original_image)
        
        report = {
            'MSE': round(mse, 4),
            'PSNR': round(psnr, 2),
            'SSIM': round(ssim, 4),
            'BPP': round(bpp, 4),
            'Data_Size_Bytes': encrypted_data_size,
            'Data_Size_KB': round(encrypted_data_size / 1024, 2),
            'Image_Pixels': original_image.shape[0] * original_image.shape[1]
        }
        
        return report
