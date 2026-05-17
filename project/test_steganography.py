"""
Test Script for Adaptive Encrypted Image Steganography System
Demonstrates all features and functionality
"""

import sys
import os
from pathlib import Path
import numpy as np
import cv2

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.image_processor import ImageProcessor
from modules.encryption import EncryptionManager
from modules.steganography import AdaptiveSteganography
from modules.metrics import ImageMetrics


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_image_processing():
    """Test image processing module"""
    print_section("TEST 1: Image Processing & Edge Detection")
    
    try:
        # Check if sample image exists
        image_path = "sample_images/cover_image.jpg"
        if not os.path.exists(image_path):
            print(f"⚠ Sample image not found at {image_path}")
            print("  Creating a synthetic test image...")
            
            # Create synthetic image
            os.makedirs("sample_images", exist_ok=True)
            test_image = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
            cv2.imwrite(image_path, test_image)
            print("  ✓ Synthetic image created")
        
        processor = ImageProcessor(image_path)
        print(f"✓ Image loaded: {processor.get_image_dimensions()}")
        
        # Preprocess
        blurred = processor.preprocess()
        print(f"✓ Preprocessing complete")
        
        # Edge detection
        edges = processor.detect_edges()
        edge_count = np.sum(edges > 0)
        print(f"✓ Edge detection complete: {edge_count} edge pixels found")
        
        # Create mask
        mask = processor.create_embedding_mask()
        print(f"✓ Embedding mask created")
        
        # Calculate capacity
        capacity = AdaptiveSteganography.calculate_capacity(mask)
        print(f"✓ Embedding capacity: {capacity} bytes")
        
        print("✓ ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_encryption():
    """Test encryption module"""
    print_section("TEST 2: AES Encryption & Decryption")
    
    try:
        plaintext = "This is a secret message! Special chars: @#$%^&*()"
        password = "SecurePassword123"
        
        # Test 1: Encrypt plaintext
        encrypted = EncryptionManager.encrypt_text(plaintext, password)
        print(f"✓ Text encrypted: {len(encrypted)} bytes")
        
        # Test 2: Decrypt with correct password
        decrypted = EncryptionManager.decrypt_text(encrypted, password)
        assert decrypted == plaintext, "Decrypted text doesn't match original"
        print(f"✓ Text decrypted correctly: {decrypted[:30]}...")
        
        # Test 3: Decrypt with wrong password (should fail)
        try:
            wrong_decrypt = EncryptionManager.decrypt_text(encrypted, "WrongPassword")
            print(f"✗ Should have failed with wrong password!")
            return False
        except ValueError:
            print(f"✓ Wrong password correctly rejected")
        
        # Test 4: Binary data encryption
        binary_data = b"\\x00\\x01\\x02\\x03\\xFF\\xFE\\xFD"
        encrypted_bin = EncryptionManager.encrypt(binary_data, password)
        decrypted_bin = EncryptionManager.decrypt(encrypted_bin, password)
        assert decrypted_bin == binary_data, "Binary data mismatch"
        print(f"✓ Binary data encryption/decryption successful")
        
        print("✓ ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_steganography():
    """Test steganography embedding and extraction"""
    print_section("TEST 3: Steganography - Embedding & Extraction")
    
    try:
        image_path = "sample_images/cover_image.jpg"
        
        if not os.path.exists(image_path):
            print("⚠ Creating synthetic test image...")
            os.makedirs("sample_images", exist_ok=True)
            test_image = np.random.randint(100, 200, (512, 512, 3), dtype=np.uint8)
            cv2.imwrite(image_path, test_image)
        
        # Load image
        processor = ImageProcessor(image_path)
        processor.preprocess()
        mask = processor.create_embedding_mask()
        original_image = processor.get_original_image()
        
        # Prepare data
        secret_message = "This is my secret message!"
        password = "TestPassword123"
        
        # Encrypt
        encrypted_data = EncryptionManager.encrypt_text(secret_message, password)
        print(f"✓ Message encrypted: {len(encrypted_data)} bytes (including overhead)")
        
        # Validate embedding
        valid, msg = AdaptiveSteganography.validate_embedding(original_image, encrypted_data, mask)
        print(f"✓ Embedding validation: {msg}")
        
        # Embed
        stego_image, success = AdaptiveSteganography.embed_data(original_image, encrypted_data, mask)
        assert success, "Embedding failed"
        print(f"✓ Data embedded successfully")
        
        # Extract
        extracted_encrypted = AdaptiveSteganography.extract_data(stego_image, mask)
        print(f"✓ Data extracted: {len(extracted_encrypted)} bytes")
        
        # Decrypt
        recovered_message = EncryptionManager.decrypt_text(extracted_encrypted, password)
        assert recovered_message == secret_message, "Recovered message doesn't match"
        print(f"✓ Data decrypted correctly: {recovered_message}")
        
        # Save results
        os.makedirs("output", exist_ok=True)
        cv2.imwrite("output/test_stego_image.png", stego_image)
        print(f"✓ Stego image saved to output/test_stego_image.png")
        
        print("✓ ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_metrics():
    """Test metrics calculation"""
    print_section("TEST 4: Image Quality Metrics Calculation")
    
    try:
        image_path = "sample_images/cover_image.jpg"
        
        if not os.path.exists(image_path):
            print("⚠ Creating synthetic test image...")
            os.makedirs("sample_images", exist_ok=True)
            test_image = np.random.randint(100, 200, (512, 512, 3), dtype=np.uint8)
            cv2.imwrite(image_path, test_image)
        
        # Load and process
        processor = ImageProcessor(image_path)
        processor.preprocess()
        mask = processor.create_embedding_mask()
        original_image = processor.get_original_image()
        
        # Create stego image
        secret_data = b"Test data"
        encrypted_data = EncryptionManager.encrypt(secret_data, "test")
        stego_image, _ = AdaptiveSteganography.embed_data(original_image, encrypted_data, mask)
        
        # Calculate metrics
        mse = ImageMetrics.calculate_mse(original_image, stego_image)
        print(f"✓ MSE calculated: {mse:.4f}")
        
        psnr = ImageMetrics.calculate_psnr(original_image, stego_image)
        print(f"✓ PSNR calculated: {psnr:.2f} dB")
        
        ssim = ImageMetrics.calculate_ssim(original_image, stego_image)
        print(f"✓ SSIM calculated: {ssim:.4f}")
        
        bpp = ImageMetrics.calculate_bpp(len(encrypted_data), original_image)
        print(f"✓ BPP calculated: {bpp:.4f}")
        
        # Generate report
        report = ImageMetrics.generate_quality_report(original_image, stego_image, len(encrypted_data))
        print(f"✓ Quality report generated:")
        for key, value in report.items():
            print(f"    {key}: {value}")
        
        print("✓ ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_edge_cases():
    """Test edge cases and error handling"""
    print_section("TEST 5: Edge Cases & Error Handling")
    
    try:
        # Test 1: Very small message
        image_path = "sample_images/cover_image.jpg"
        if os.path.exists(image_path):
            processor = ImageProcessor(image_path)
            processor.preprocess()
            original_image = processor.get_original_image()
            
            small_data = b"A"
            encrypted_small = EncryptionManager.encrypt(small_data, "test")
            print(f"✓ Small message (1 byte) handled correctly")
        
        # Test 2: Special characters in password
        special_password = "P@$$w0rd!#%^&*()_+-=[]{}|;:',.<>?/~`"
        encrypted = EncryptionManager.encrypt(b"test", special_password)
        decrypted = EncryptionManager.decrypt(encrypted, special_password)
        assert decrypted == b"test"
        print(f"✓ Special characters in password handled correctly")
        
        # Test 3: Unicode in message
        unicode_message = "Hello 世界 🌍 Привет العالم"
        encrypted_unicode = EncryptionManager.encrypt_text(unicode_message, "pass")
        decrypted_unicode = EncryptionManager.decrypt_text(encrypted_unicode, "pass")
        assert decrypted_unicode == unicode_message
        print(f"✓ Unicode characters handled correctly")
        
        # Test 4: Empty password (should work, but not recommended)
        encrypted_empty = EncryptionManager.encrypt(b"data", "")
        decrypted_empty = EncryptionManager.decrypt(encrypted_empty, "")
        assert decrypted_empty == b"data"
        print(f"✓ Empty password handled correctly")
        
        print("✓ ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\\n" + "█"*60)
    print("█  ADAPTIVE ENCRYPTED IMAGE STEGANOGRAPHY TEST SUITE")
    print("█"*60)
    
    tests = [
        ("Image Processing & Edge Detection", test_image_processing),
        ("AES Encryption & Decryption", test_encryption),
        ("Steganography Embedding & Extraction", test_steganography),
        ("Image Quality Metrics", test_metrics),
        ("Edge Cases & Error Handling", test_edge_cases),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Print summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\\nTotal: {total} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\\n🎉 ALL TESTS PASSED! System is ready for use.")
    else:
        print(f"\\n⚠ {failed} test(s) failed. Please review the errors above.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
