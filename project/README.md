# 🔐 Adaptive Encrypted Image Steganography

Hide encrypted messages in images using military-grade security and intelligent edge-based embedding.

**Version**: 1.0.0 | **License**: MIT | **Python**: 3.8+

---

## ⚡ Quick Start

### Run GUI Application
```bash
pip install -r requirements.txt
python app.py
```

### Build Windows Installer
```bash
.\build.bat
```
Creates `SteganographyApp_Installer.exe` for sharing.

See [BUILD.md](BUILD.md) for complete build & distribution guide.

---

## ✨ What It Does

1. **Embed**: Hide text or files in images with AES-256 encryption
2. **Detect**: Uses Canny edge detection for optimal embedding regions  
3. **Extract**: Recover data with authentication verification
4. **Analyze**: Measures quality with PSNR, MSE, SSIM, BPP metrics

---

## 🎯 Key Features

- 🔒 **AES-256-GCM** encryption with PBKDF2 key derivation
- 🎨 **Adaptive LSB** embedding in high-texture regions (edges)
- 📊 **Quality Metrics**: PSNR, MSE, SSIM, BPP analysis
- 💻 **Tkinter GUI**: User-friendly interface
- 📁 **Flexible Data**: Hide text messages or files
- 🔍 **Lossless Recovery**: Complete data extraction
- 📈 **Capacity Planning**: Real-time embedding limits

---

## 🚀 Usage

### Embed a Message
1. Launch `python app.py`
2. Click "Upload Image"
3. Enter secret message or select file
4. Set password
5. Click "EMBED DATA"
6. Save stego image

### Extract a Message
1. Load stego image
2. Enter password
3. Click "EXTRACT & DECRYPT"
4. View or save recovered data

---

## 📁 Project Structure

```
├── app.py                      # GUI application
├── requirements.txt            # Dependencies
├── modules/
│   ├── image_processor.py     # Edge detection & preprocessing
│   ├── encryption.py          # AES-256-GCM encryption
│   ├── steganography.py       # Adaptive LSB embedding
│   └── metrics.py             # Quality measurement
├── test_steganography.py      # Unit tests
├── BUILD.md                   # Build & distribution guide
└── README.md                  # This file
```

---

## 🔐 Security

| Component | Details |
|-----------|---------|
| **Encryption** | AES-256-GCM (NIST-approved) |
| **Key Derivation** | PBKDF2 with 100,000 iterations |
| **Authorization** | GCM authentication tag |
| **Embedding** | Adaptive LSB in edges only |
| **Detection Resistance** | Blends with natural image variation |

---

## 📊 Performance

| Metric | Typical Value |
|--------|---------------|
| PSNR | 45-50 dB (imperceptible) |
| MSE | 0.5-2.0 (minimal distortion) |
| SSIM | 0.95-0.99 (nearly identical) |
| Embedding Rate | 0.5-2.0 BPP |
| Encryption Time | <100 ms |

---

## 🔧 Command-Line Usage

```python
from modules.image_processor import ImageProcessor
from modules.encryption import EncryptionManager
from modules.steganography import AdaptiveSteganography
import cv2

# Load and process image
processor = ImageProcessor("image.jpg")
processor.preprocess()
mask = processor.create_embedding_mask()

# Encrypt data
message = "Secret"
password = "StrongPassword123"
encrypted = EncryptionManager.encrypt(message.encode(), password)

# Embed
original = processor.get_original_image()
stego, success = AdaptiveSteganography.embed_data(original, encrypted, mask)

# Save
cv2.imwrite("stego.png", stego)
```

---

## 🧪 Testing

```bash
python test_steganography.py
```

---

## 📦 Build Installer

See [BUILD.md](BUILD.md) for detailed instructions on:
- Creating Windows installer
- Distributing on GitHub/web
- User installation steps

---

## 📝 License

MIT License - See LICENSE file

---

## 🎓 How It Works

1. **Image Analysis**: Detect edges using Canny algorithm
2. **Encryption**: AES-256-GCM with PBKDF2 key derivation
3. **Embedding**: Adaptive LSB in high-texture regions only
4. **Quality Check**: PSNR/SSIM verify imperceptibility

---

## 🧪 Testing

```bash
python test_steganography.py
```

---

## 📝 License

MIT License - See LICENSE file
