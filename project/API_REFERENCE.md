# API Reference Documentation

## Overview

This document provides comprehensive API documentation for all modules in the Adaptive Encrypted Image Steganography system.

---

## Table of Contents

1. [image_processor.py](#image_processorpy)
2. [encryption.py](#encryptionpy)
3. [steganography.py](#steganographypy)
4. [metrics.py](#metricspy)

---

## image_processor.py

### ImageProcessor Class

Core class for image processing and edge detection operations.

#### Constructor

```python
ImageProcessor(image_path: str)
```

**Parameters**:
- `image_path` (str): Path to the image file

**Raises**:
- `FileNotFoundError`: If image file not found
- `ValueError`: If image cannot be read

**Example**:
```python
from modules.image_processor import ImageProcessor

processor = ImageProcessor("sample.jpg")
print(processor.get_image_dimensions())
```

---

#### Method: preprocess()

```python
def preprocess(self) -> np.ndarray
```

Preprocess image: convert to grayscale and apply Gaussian blur.

**Returns**:
- `np.ndarray`: Preprocessed grayscale blurred image

**Notes**:
- Gaussian kernel: 5×5
- Sigma: 1.0
- Modifies internal state

**Example**:
```python
blurred_image = processor.preprocess()
print(f"Image shape: {blurred_image.shape}")
```

---

#### Method: detect_edges()

```python
def detect_edges(self, threshold1: int = 50, threshold2: int = 150) -> np.ndarray
```

Apply Canny edge detection on preprocessed image.

**Parameters**:
- `threshold1` (int): Lower threshold (default: 50)
- `threshold2` (int): Upper threshold (default: 150)

**Returns**:
- `np.ndarray`: Binary edge map

**Raises**:
- Auto-calls `preprocess()` if not already called

**Example**:
```python
edges = processor.detect_edges(threshold1=40, threshold2=120)
edge_count = np.sum(edges > 0)
print(f"Edge pixels: {edge_count}")
```

---

#### Method: create_embedding_mask()

```python
def create_embedding_mask(self) -> np.ndarray
```

Create adaptive embedding mask from edge detection results.

**Returns**:
- `np.ndarray`: Binary mask (1 for embedding regions, 0 otherwise)

**Dependencies**:
- Requires `detect_edges()` to be called first

**Example**:
```python
mask = processor.create_embedding_mask()
print(f"Mask shape: {mask.shape}")
print(f"Mask dtype: {mask.dtype}")
```

---

#### Method: get_embedding_capacity()

```python
def get_embedding_capacity(mask: np.ndarray) -> int
```

Calculate maximum bytes that can be embedded.

**Parameters**:
- `mask` (np.ndarray): Binary embedding mask

**Returns**:
- `int`: Maximum bytes (each edge pixel = 3 bytes in RGB)

**Formula**:
```
capacity = (edge_pixels * 3 - 32) / 8
```

**Example**:
```python
capacity = processor.get_embedding_capacity(mask)
print(f"Can embed: {capacity} bytes")
```

---

#### Method: calculate_histogram()

```python
def calculate_histogram(self, image: Optional[np.ndarray] = None) 
    -> Tuple[np.ndarray, np.ndarray, np.ndarray]
```

Calculate histogram for an image.

**Parameters**:
- `image` (np.ndarray, optional): Image to analyze. Default: original image

**Returns**:
- `Tuple[np.ndarray, np.ndarray, np.ndarray]`: (hist_b, hist_g, hist_r)

**Example**:
```python
hist_b, hist_g, hist_r = processor.calculate_histogram()
print(f"Blue channel: {hist_b.shape}")
```

---

#### Method: get_image_dimensions()

```python
def get_image_dimensions(self) -> Tuple[int, int]
```

Get image dimensions.

**Returns**:
- `Tuple[int, int]`: (height, width)

**Example**:
```python
height, width = processor.get_image_dimensions()
print(f"Image: {width}x{height}")
```

---

#### Method: get_original_image()

```python
def get_original_image(self) -> np.ndarray
```

Get a copy of original image.

**Returns**:
- `np.ndarray`: Original image (BGR format)

**Example**:
```python
original = processor.get_original_image()
```

---

#### Method: get_grayscale_image()

```python
def get_grayscale_image(self) -> np.ndarray
```

Get grayscale image (calls preprocess if needed).

**Returns**:
- `np.ndarray`: Grayscale image

**Example**:
```python
gray = processor.get_grayscale_image()
```

---

#### Method: get_edge_map()

```python
def get_edge_map(self) -> np.ndarray
```

Get edge map (calls detect_edges if needed).

**Returns**:
- `np.ndarray`: Binary edge map

**Example**:
```python
edges = processor.get_edge_map()
```

---

## encryption.py

### EncryptionManager Class

Static class managing AES-256-GCM encryption operations.

#### Method: generate_key_from_password()

```python
@staticmethod
def generate_key_from_password(password: str, salt: bytes = None) 
    -> Tuple[bytes, bytes]
```

Generate AES encryption key from password using PBKDF2.

**Parameters**:
- `password` (str): User password
- `salt` (bytes, optional): Salt for key derivation. Auto-generated if None

**Returns**:
- `Tuple[bytes, bytes]`: (key, salt)

**Parameters**:
- Key size: 256 bits (32 bytes)
- Salt size: 128 bits (16 bytes) if generated
- Iterations: 100,000

**Example**:
```python
from modules.encryption import EncryptionManager

key, salt = EncryptionManager.generate_key_from_password("MyPassword")
print(f"Key: {key.hex()}")
print(f"Salt: {salt.hex()}")
```

---

#### Method: encrypt()

```python
@staticmethod
def encrypt(data: bytes, password: str) -> bytes
```

Encrypt data using AES-256-GCM.

**Parameters**:
- `data` (bytes): Data to encrypt
- `password` (str): Encryption password

**Returns**:
- `bytes`: Encrypted data (salt + nonce + ciphertext + tag)

**Format**:
```
[Salt (16B)] + [Nonce (12B)] + [Ciphertext] + [Tag (16B)]
```

**Total Overhead**: 44 bytes

**Example**:
```python
plaintext = b"Secret message"
encrypted = EncryptionManager.encrypt(plaintext, "password123")
print(f"Encrypted size: {len(encrypted)} bytes")
```

---

#### Method: decrypt()

```python
@staticmethod
def decrypt(encrypted_data: bytes, password: str) -> bytes
```

Decrypt AES-256-GCM encrypted data.

**Parameters**:
- `encrypted_data` (bytes): Encrypted data
- `password` (str): Decryption password

**Returns**:
- `bytes`: Decrypted data

**Raises**:
- `ValueError`: If decryption fails (wrong password or corrupted data)

**Example**:
```python
try:
    decrypted = EncryptionManager.decrypt(encrypted, "password123")
except ValueError as e:
    print(f"Decryption failed: {e}")
```

---

#### Method: encrypt_text()

```python
@staticmethod
def encrypt_text(text: str, password: str) -> bytes
```

Encrypt text message (wrapper for text-specific use).

**Parameters**:
- `text` (str): Text to encrypt
- `password` (str): Encryption password

**Returns**:
- `bytes`: Encrypted text

**Example**:
```python
encrypted = EncryptionManager.encrypt_text("Hello World", "pass")
```

---

#### Method: decrypt_text()

```python
@staticmethod
def decrypt_text(encrypted_data: bytes, password: str) -> str
```

Decrypt encrypted text.

**Parameters**:
- `encrypted_data` (bytes): Encrypted data
- `password` (str): Decryption password

**Returns**:
- `str`: Decrypted text

**Example**:
```python
decrypted = EncryptionManager.decrypt_text(encrypted, "pass")
print(decrypted)
```

---

## steganography.py

### AdaptiveSteganography Class

Static class implementing adaptive LSB steganography.

#### Method: embed_data()

```python
@staticmethod
def embed_data(image: np.ndarray, encrypted_data: bytes, mask: np.ndarray) 
    -> Tuple[np.ndarray, bool]
```

Embed encrypted data into image using adaptive LSB.

**Parameters**:
- `image` (np.ndarray): Original image (BGR format)
- `encrypted_data` (bytes): Encrypted data to embed
- `mask` (np.ndarray): Binary embedding mask

**Returns**:
- `Tuple[np.ndarray, bool]`: (stego_image, success)

**Raises**:
- No exceptions; returns (image, False) if embedding fails

**Embedding Process**:
1. Check capacity
2. Add 4-byte length header
3. Convert to bit stream
4. Embed in edge pixels (LSB)

**Example**:
```python
from modules.steganography import AdaptiveSteganography

stego_image, success = AdaptiveSteganography.embed_data(
    original_image, encrypted_data, mask
)

if success:
    print("Embedding successful")
else:
    print("Embedding failed - data too large")
```

---

#### Method: extract_data()

```python
@staticmethod
def extract_data(stego_image: np.ndarray, mask: np.ndarray) -> bytes
```

Extract encrypted data from stego image.

**Parameters**:
- `stego_image` (np.ndarray): Image containing hidden data
- `mask` (np.ndarray): Binary embedding mask

**Returns**:
- `bytes`: Extracted encrypted data (empty if extraction fails)

**Extraction Process**:
1. Extract bits from edge pixels (LSB)
2. Parse 4-byte length header
3. Extract data bits
4. Reconstruct bytes

**Example**:
```python
extracted = AdaptiveSteganography.extract_data(stego_image, mask)
if extracted:
    print(f"Extracted {len(extracted)} bytes")
else:
    print("No data found or extraction failed")
```

---

#### Method: calculate_capacity()

```python
@staticmethod
def calculate_capacity(mask: np.ndarray) -> int
```

Calculate maximum embedding capacity.

**Parameters**:
- `mask` (np.ndarray): Binary embedding mask

**Returns**:
- `int`: Maximum bytes that can be embedded

**Formula**:
```python
capacity = (edge_pixels * 3 - 32) / 8
```

**Example**:
```python
capacity = AdaptiveSteganography.calculate_capacity(mask)
print(f"Maximum capacity: {capacity} bytes")
```

---

#### Method: validate_embedding()

```python
@staticmethod
def validate_embedding(image: np.ndarray, encrypted_data: bytes, mask: np.ndarray) 
    -> Tuple[bool, str]
```

Validate if data can be embedded.

**Parameters**:
- `image` (np.ndarray): Original image
- `encrypted_data` (bytes): Data to embed
- `mask` (np.ndarray): Embedding mask

**Returns**:
- `Tuple[bool, str]`: (is_valid, message)

**Validation Checks**:
- Image exists
- Data not empty
- Data fits in capacity
- Mask available

**Example**:
```python
valid, message = AdaptiveSteganography.validate_embedding(
    image, encrypted_data, mask
)

if valid:
    print("OK: " + message)
else:
    print("ERROR: " + message)
```

---

## metrics.py

### ImageMetrics Class

Static class for image quality metric calculations.

#### Method: calculate_mse()

```python
@staticmethod
def calculate_mse(image1: np.ndarray, image2: np.ndarray) -> float
```

Calculate Mean Squared Error.

**Parameters**:
- `image1` (np.ndarray): First image
- `image2` (np.ndarray): Second image

**Returns**:
- `float`: MSE value

**Formula**:
$$MSE = \frac{1}{N} \sum (I1 - I2)^2$$

**Note**: Auto-resizes image2 if dimensions don't match

**Example**:
```python
from modules.metrics import ImageMetrics

mse = ImageMetrics.calculate_mse(original, stego)
print(f"MSE: {mse:.4f}")
```

---

#### Method: calculate_psnr()

```python
@staticmethod
def calculate_psnr(image1: np.ndarray, image2: np.ndarray) -> float
```

Calculate Peak Signal-to-Noise Ratio.

**Parameters**:
- `image1` (np.ndarray): First image (original)
- `image2` (np.ndarray): Second image (stego)

**Returns**:
- `float`: PSNR value in dB

**Formula**:
$$PSNR = 20 \log_{10}(255 / \sqrt{MSE})$$

**Quality Scale**:
- \> 50 dB: Imperceptible
- 40-50 dB: imperceptible/hard to detect
- 30-40 dB: Noticeable
- \< 30 dB: Significant

**Example**:
```python
psnr = ImageMetrics.calculate_psnr(original, stego)
print(f"PSNR: {psnr:.2f} dB")
```

---

#### Method: calculate_ssim()

```python
@staticmethod
def calculate_ssim(image1: np.ndarray, image2: np.ndarray) -> float
```

Calculate Structural Similarity Index.

**Parameters**:
- `image1` (np.ndarray): First image
- `image2` (np.ndarray): Second image

**Returns**:
- `float`: SSIM value (-1 to 1)

**Interpretation**:
- 1.0: Identical images
- 0.95-1.0: Imperceptible differences
- 0.8-0.95: Very similar
- 0.5-0.8: Similar
- \< 0.5: Noticeably different

**Example**:
```python
ssim = ImageMetrics.calculate_ssim(original, stego)
print(f"SSIM: {ssim:.4f}")
```

---

#### Method: calculate_bpp()

```python
@staticmethod
def calculate_bpp(encrypted_data_size: int, image: np.ndarray) -> float
```

Calculate Bits Per Pixel embedding rate.

**Parameters**:
- `encrypted_data_size` (int): Size of encrypted data in bytes
- `image` (np.ndarray): Image

**Returns**:
- `float`: BPP value

**Formula**:
$$BPP = \frac{\text{Total Data Bits}}{\text{Total Pixels}}$$

**Example**:
```python
bpp = ImageMetrics.calculate_bpp(len(encrypted_data), image)
print(f"BPP: {bpp:.4f}")
```

---

#### Method: generate_quality_report()

```python
@staticmethod
def generate_quality_report(original_image: np.ndarray, stego_image: np.ndarray, 
                           encrypted_data_size: int) -> dict
```

Generate comprehensive quality analysis report.

**Parameters**:
- `original_image` (np.ndarray): Original image
- `stego_image` (np.ndarray): Stego image
- `encrypted_data_size` (int): Size of encrypted data

**Returns**:
- `dict`: Dictionary with keys:
  - `MSE`: Mean squared error
  - `PSNR`: Peak signal-to-noise ratio (dB)
  - `SSIM`: Structural similarity index
  - `BPP`: Bits per pixel
  - `Data_Size_Bytes`: Data size in bytes
  - `Data_Size_KB`: Data size in KB
  - `Image_Pixels`: Total image pixels

**Example**:
```python
report = ImageMetrics.generate_quality_report(original, stego, data_size)
print(f"PSNR: {report['PSNR']} dB")
print(f"BPP: {report['BPP']}")
print(f"SSIM: {report['SSIM']}")
```

---

## Complete Example Workflow

```python
#!/usr/bin/env python3
"""
Complete example: Embed and extract secret message
"""

from modules.image_processor import ImageProcessor
from modules.encryption import EncryptionManager
from modules.steganography import AdaptiveSteganography
from modules.metrics import ImageMetrics
import cv2

# 1. Load and process image
processor = ImageProcessor("image.jpg")
processor.preprocess()
mask = processor.create_embedding_mask()
original_image = processor.get_original_image()

# 2. Prepare secret data
secret_message = "This is secret!"
password = "MySecurePassword"

# 3. Encrypt
encrypted_data = EncryptionManager.encrypt_text(secret_message, password)
print(f"Encrypted: {len(encrypted_data)} bytes")

# 4. Validate and embed
valid, msg = AdaptiveSteganography.validate_embedding(original_image, encrypted_data, mask)
if not valid:
    print(f"Error: {msg}")
    exit(1)

stego_image, success = AdaptiveSteganography.embed_data(original_image, encrypted_data, mask)

# 5. Calculate metrics
report = ImageMetrics.generate_quality_report(original_image, stego_image, len(encrypted_data))
print(f"Quality Report: {report}")

# 6. Save stego image
cv2.imwrite("stego.jpg", stego_image)

# 7. Extract (on another machine/time)
processor2 = ImageProcessor("stego.jpg")
processor2.preprocess()
mask2 = processor2.create_embedding_mask()
stego_image2 = processor2.get_original_image()

extracted_encrypted = AdaptiveSteganography.extract_data(stego_image2, mask2)
recovered_message = EncryptionManager.decrypt_text(extracted_encrypted, password)

print(f"Recovered: {recovered_message}")
assert recovered_message == secret_message
```

---

## Error Handling

### Common Exceptions

```python
# File not found
try:
    processor = ImageProcessor("nonexistent.jpg")
except FileNotFoundError as e:
    print(f"Image not found: {e}")

# Decryption failure
try:
    plaintext = EncryptionManager.decrypt(encrypted, "wrong_password")
except ValueError as e:
    print(f"Decryption failed: {e}")

# Data too large
valid, msg = AdaptiveSteganography.validate_embedding(image, large_data, mask)
if not valid:
    print(f"Embedding failed: {msg}")
```

---

## Best Practices

1. **Always validate before embedding**
   ```python
   valid, msg = AdaptiveSteganography.validate_embedding(...)
   if valid:
       # proceed
   ```

2. **Handle decryption errors**
   ```python
   try:
       plaintext = EncryptionManager.decrypt(encrypted, password)
   except ValueError:
       # wrong password
   ```

3. **Check extraction results**
   ```python
   extracted = AdaptiveSteganography.extract_data(...)
   if extracted:
       # process
   else:
       # no data found
   ```

4. **Use strong passwords** (> 12 characters, mixed case, numbers, symbols)

5. **Keep original images safe** as reference for quality metrics

---

**API Reference Version**: 1.0  
**Last Updated**: 2024  
**Status**: Complete
