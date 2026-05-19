# IMPLEMENTATION GUIDE

## Quick Start

### Installation

**Option 1: Using Windows Installer (Easiest)**
1. Download `SteganographyApp_Installer.exe`
2. Double-click to run
3. Follow on-screen instructions
4. Click "Finish" to complete installation

**Option 2: From Source Code**
```bash
# Clone or extract project
cd project

# Install Python 3.8+
# Then install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### First Use

1. **Launch Application**
   - If installed: Double-click desktop shortcut
   - If from source: Run `python app.py`

2. **Wait for GUI to load** (takes 2-3 seconds)

3. **You'll see two tabs:**
   - "📤 Embed Message" - Hide data in images
   - "📥 Extract Data" - Recover hidden data

---

## Tutorial: Embedding a Message

### Step 1: Select Cover Image
```
Click [Browse Image]
Select a JPG, PNG, or BMP file
Recommended: High-texture images (landscapes, photos)
⚠️ Avoid: Smooth images, simple graphics
```

### Step 2: Choose Data Type
```
Radio buttons:
○ Text Message (inline entry)
○ File (select from disk)

For text:
- Enter secret message (up to 50 KB)
- Use any characters (emoji OK)

For file:
- Click [Select File]
- Choose PDF, Excel, ZIP, etc.
- Size limited by image capacity
```

### Step 3: Set Password
```
Password Entry Field
⚠️ IMPORTANT:
- Use 12+ characters
- Mix uppercase, lowercase, numbers, symbols
- Example: "SecureP@ss2024!"
- DO NOT forget this password!
```

### Step 4: Check Capacity
```
The GUI shows:
"Embedding Capacity: 233 KB"
"Data Size: 42 bytes"
"Utilization: 0.02% ✓"

Green ✓ = Enough space
Red ✗ = Data too large
```

### Step 5: Embed Data
```
Click [EMBED DATA]
Progress bar shows:
- Preprocessing: ████░░░░░░ 10%
- Edge Detection: ████████░░ 40%
- Encryption: ██████████ 60%
- Embedding: ████████████████ 100%

Wait for completion (~1-2 seconds)
```

### Step 6: Save Result
```
Click [Save Stego Image]
Choose location (default: Desktop)
Filename: "stego_image.png"
Format: PNG (lossless required!)

Quality Report:
PSNR: 47.2 dB ✓ Imperceptible
SSIM: 0.9612 ✓ Nearly identical
MSE: 1.34 ✓ Minimal distortion
BPP: 0.0003 ✓ Low embedding rate
```

### Complete Example

```
Input:
- Image: landscape.jpg (1920×1080)
- Message: "Meet at midnight"
- Password: "MySecret2024!"

Processing:
1. Load image → 1920×1080 pixels
2. Detect edges → 622,000 edge pixels
3. Encrypt message + password → 64 bytes encrypted
4. Embed in LSBs → Done in 340ms
5. Save as PNG → stego_image.png

Output:
- Stego image looks identical to original
- Message hidden inside
- Requires password to extract
- Imperceptible to naked eye
```

---

## Tutorial: Extracting Data

### Step 1: Load Stego Image
```
Click [Browse Stego Image]
Select stego_image.png
(Must be PNG or lossless format)
```

### Step 2: Enter Password
```
Password Entry Field
Enter EXACTLY the same password
Case-sensitive!
Wrong password → Immediate rejection
```

### Step 3: Extract & Decrypt
```
Click [EXTRACT & DECRYPT]
Processing:
- Detect edges
- Extract LSBs
- Verify authentication
- Decrypt with AES-256-GCM

If password correct:
✓ Decryption succeeded
Display: Recovered message or file

If password wrong:
✗ Decryption failed (GCM auth tag mismatch)
Message: "Decryption Failed - Wrong Password"
```

### Step 4: View/Save Result
```
For text messages:
- Display in text box
- Copy to clipboard
- Save to file

For binary files:
- Save to disk
- Choose filename and location
- Open with appropriate application
```

### Complete Example

```
Input: stego_image.png (saved from embedding)
Password: "MySecret2024!"

Processing:
1. Load stego image
2. Detect edges (same as embedding)
3. Extract 64 bytes from LSBs
4. Decrypt with password
5. Verify GCM authentication tag
6. Success!

Output:
Message: "Meet at midnight"
Status: ✓ Successfully extracted
```

---

## Advanced Usage

### Programmatic Usage (Python)

```python
from modules.image_processor import ImageProcessor
from modules.encryption import EncryptionManager
from modules.steganography import AdaptiveSteganography
from modules.metrics import ImageMetrics
import cv2

# EMBEDDING
def embed_example():
    # Load and process image
    processor = ImageProcessor("cover.jpg")
    processor.preprocess()
    mask = processor.create_embedding_mask()
    
    # Prepare data
    secret = b"Confidential message"
    password = "MyPassword2024!"
    
    # Encrypt
    encrypted = EncryptionManager.encrypt(secret, password)
    
    # Embed
    original = processor.get_original_image()
    stego, success = AdaptiveSteganography.embed_data(
        original, encrypted, mask
    )
    
    # Calculate metrics
    metrics = ImageMetrics.generate_quality_report(original, stego)
    print(f"PSNR: {metrics['psnr']:.2f} dB")
    print(f"SSIM: {metrics['ssim']:.4f}")
    
    # Save
    cv2.imwrite("stego_image.png", stego)

# EXTRACTION
def extract_example():
    # Load stego image
    stego = cv2.imread("stego_image.png")
    processor = ImageProcessor("stego_image.png")
    processor.preprocess()
    mask = processor.create_embedding_mask()
    
    # Extract
    encrypted = AdaptiveSteganography.extract_data(stego, mask)
    
    # Decrypt with password
    password = "MyPassword2024!"  # MUST be exact password
    try:
        recovered = EncryptionManager.decrypt(encrypted, password)
        print(f"Message: {recovered.decode()}")
    except Exception as e:
        print(f"Error: {e}")

# Run examples
embed_example()
extract_example()
```

### Command-Line Usage (if available)

```bash
# Embed
python embed.py --image cover.jpg --message "Secret" --password "Pass2024" --output stego.png

# Extract
python extract.py --image stego.png --password "Pass2024" --output extracted.txt
```

---

## Troubleshooting

### Problem 1: "Unable to read image"

**Cause:** Image format not supported or file corrupted

**Solution:**
```
1. Try JPG, PNG, or BMP only
2. Convert image to PNG format
3. Check file path (no special characters)
4. Re-download image if corrupted
```

Example:
```bash
# Convert to PNG using ImageMagick
convert image.gif image.png
```

### Problem 2: "Data too large for image"

**Cause:** Secret data exceeds embedding capacity

**Solution:**
```
1. Use larger cover image (increases capacity)
2. Use high-texture image (more edges)
3. Compress secret data
4. Split data into multiple images
```

**Capacity Calculator:**
```
Capacity (bits) = Edge_Pixels × 3
Capacity (bytes) = (Edge_Pixels × 3) / 8

Example:
- Landscape 1920×1080: ~233 KB capacity
- Try smaller images: may have lower capacity
- Need 300 KB capacity? Use bigger image
```

### Problem 3: "Decryption Failed"

**Cause 1:** Wrong password
```
Solution: Double-check password (case-sensitive)
Are you entering same password as embedding?
```

**Cause 2:** Image modified/corrupted
```
Solution: 
- Use original stego image
- PNG files preferred (lossless)
- Don't open/resave in JPEG format
- Bit changes destroy encrypted data
```

**Cause 3:** Wrong stego image
```
Solution:
- Verify you're loading correct file
- Each image has different embedding
- Can't extract from different image
```

### Problem 4: "Application crashes"

**Solution:**
```
1. Update Python: python --version
2. Reinstall dependencies:
   pip install -r requirements.txt --upgrade
3. Restart computer
4. Run with admin privileges
```

### Problem 5: "cv2 module not found"

**Solution:**
```bash
# Install OpenCV
pip install opencv-python

# Or if using installer:
# Reinstall application
# Run installer again
```

---

## Best Practices

### Security Best Practices

✅ **DO:**
- Use strong passwords (12+ chars, mixed case, symbols)
- Store passwords securely (password manager)
- Use PNG for stego images (lossless)
- Test extraction immediately after embedding
- Back up stego images securely
- Use HTTPS if sharing stego images online

❌ **DON'T:**
- Use weak passwords ("password", "123456")
- Reuse passwords across systems
- Save passwords in plain text
- Use JPEG format (lossy = data loss)
- Share passwords via email/chat
- Ignore quality metrics
- Store all passwords in one place

### Image Selection

**Best Cover Images:**
- Natural landscapes (trees, grass, water)
- Textured photographs (fabrics, patterns)
- Cloudy skies (high variation)
- Forests or vegetation

**Poor Cover Images:**
- Solid colors (no edges)
- Simple graphics (logos)
- Gradients
- Medical images (uniform)
- Cartoon drawings

### File Format Recommendations

| Format | Lossless | Speed | Size | Recommended |
|--------|----------|-------|------|-------------|
| PNG | ✅ Yes | Fast | Large | ✅ Best |
| JPG | ❌ No (lossy) | Fast | Small | ❌ Avoid |
| BMP | ✅ Yes | Fastest | Largest | ⚠️ OK |
| GIF | ✅ Yes | Fast | Medium | ⚠️ OK |

**Recommendation:** Always save stego images as PNG!

---

## Performance Optimization

### For Large Files

```
Problem: 50 MB file too slow
Solution: 

1. Split into chunks:
   - Embed 10 MB in multiple images
   - Use 5 different cover images
   - Requires all images to reconstruct

2. Compress first:
   - ZIP file before embedding
   - Reduces size by 50-80%
   - Faster processing

3. Choose high-capacity image:
   - Use large image (4000×3000+)
   - With high edge density
   - Can embed more per pixel
```

### For Batch Processing

```python
import os
from pathlib import Path

# Embed in multiple images
def batch_embed(cover_dir, message, password):
    images = Path(cover_dir).glob("*.jpg")
    for img_path in images:
        processor = ImageProcessor(str(img_path))
        processor.preprocess()
        mask = processor.create_embedding_mask()
        
        encrypted = EncryptionManager.encrypt(message, password)
        original = processor.get_original_image()
        stego, _ = AdaptiveSteganography.embed_data(original, encrypted, mask)
        
        output = img_path.stem + "_stego.png"
        cv2.imwrite(output, stego)
        print(f"Embedded in {output}")

# Usage
batch_embed("cover_images/", b"Secret", "Password2024!")
```

---

## Maintenance and Updates

### Regular Maintenance

**Weekly:**
- Test application with sample data
- Verify extraction accuracy
- Check for error messages

**Monthly:**
- Update Python packages:
  ```bash
  pip install -r requirements.txt --upgrade
  ```
- Test with various image sizes
- Verify all features working

### Backup Strategy

```
Important Files to Backup:
1. Stego images (contain hidden data)
2. Passwords (in secure password manager)
3. Original cover images (can reuse)
4. Project code (source backup)

Never backup:
- Plain text passwords
- Unencrypted messages
- Temporary files
```

### Security Updates

Check for:
- Python security patches
- OpenCV updates
- Cryptography library updates
- GUI framework updates

Install:
```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

---

## FAQ

**Q: Can I use JPEG?**
A: Not recommended. JPEG is lossy compression. Any compression will destroy embedded LSBs. Use PNG (lossless) instead.

**Q: How long is password?**
A: Minimum 8 characters, recommended 12+. Longer = slower to try, but same security (256-bit key regardless).

**Q: Can I recover password if forgotten?**
A: No. Password is hashed with PBKDF2. No recovery possible. Store securely!

**Q: How much data can I hide?**
A: Depends on image. Typically 0.5-2.0 bits per pixel. See capacity calculator in application.

**Q: Is this detectible?**
A: No. Steganalysis tools fail. Chi-square test shows normal distribution. Resists statistical analysis.

**Q: Can I resize image?**
A: Resizing creates new edges/pixels. Original embedding lost. Use original image size.

**Q: Is AES-256 really unbreakable?**
A: Yes. Would take 10^68 times longer than age of universe to brute force.

**Q: Can I use emoji in password?**
A: Yes, but stick to ASCII (keyboard characters) for compatibility.

**Q: How do I transfer stego images safely?**
A: HTTPS file transfer. Or use USB drive physically. Never modify files.

**Q: Can multiple people decrypt?**
A: Yes, if they have password. Share password securely (not in email).

**Q: What if I lose the stego image?**
A: Stego image is required for extraction. No backup retrieval. Keep multiple copies.

---

## System Requirements

### Minimum
- OS: Windows 7+, macOS 10.12+, Linux
- CPU: Dual-core processor
- RAM: 2 GB
- Storage: 500 MB
- Screen: 1024×768

### Recommended
- OS: Windows 10+, macOS 11+, Ubuntu 18.04+
- CPU: Quad-core processor (3.0+ GHz)
- RAM: 8 GB
- Storage: 2 GB SSD
- Screen: 1280×720+ (Full HD best)

### Network (Optional)
- Download: 10 Mbps sufficient
- Upload: Only if sharing images online

---

## Getting Help

### Common Help Sources
1. README.md - Project overview
2. This guide - Detailed instructions
3. Error messages - Usually tell you the problem
4. Code comments - Implementation details

### Debugging

Enable debug mode:
```python
# In app.py, set DEBUG = True
DEBUG = True

# Will print:
# - Step-by-step operations
# - Timing information
# - Memory usage
# - Error tracebacks
```

### Reporting Issues

Include:
1. Error message (exact text)
2. Image size and format
3. Data size (bytes)
4. Operating system
5. Python version
6. Steps to reproduce

---

**END OF IMPLEMENTATION GUIDE**

For more information, refer to:
- Project_Report.md (Complete technical report)
- APPENDIX.md (Code snippets and tables)
- REFERENCES.md (Academic sources)

