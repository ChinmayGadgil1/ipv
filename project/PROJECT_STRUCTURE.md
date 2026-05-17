# Project Structure Documentation

## Complete Directory Tree

```
project/
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # Quick start guide (START HERE ⭐)
├── METHODOLOGY.md                     # Technical algorithms & mathematics
├── API_REFERENCE.md                   # API documentation for developers
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── app.py                             # Main GUI application (ENTRY POINT)
├── setup.py                           # Automated setup script
├── generate_samples.py                # Sample image generation
├── test_steganography.py              # Unit tests & examples
│
├── modules/
│   ├── __init__.py                    # Module initialization
│   ├── image_processor.py             # Image processing & edge detection
│   │   └── Class: ImageProcessor
│   │       - preprocess()
│   │       - detect_edges()
│   │       - create_embedding_mask()
│   │       - get_embedding_capacity()
│   │       - calculate_histogram()
│   │       - get_image_dimensions()
│   │
│   ├── encryption.py                  # AES-256-GCM encryption/decryption
│   │   └── Class: EncryptionManager
│   │       - generate_key_from_password()
│   │       - encrypt()
│   │       - decrypt()
│   │       - encrypt_text()
│   │       - decrypt_text()
│   │
│   ├── steganography.py               # Adaptive LSB embedding/extraction
│   │   └── Class: AdaptiveSteganography
│   │       - embed_data()
│   │       - extract_data()
│   │       - calculate_capacity()
│   │       - validate_embedding()
│   │
│   └── metrics.py                     # Quality metrics calculation
│       └── Class: ImageMetrics
│           - calculate_mse()
│           - calculate_psnr()
│           - calculate_ssim()
│           - calculate_bpp()
│           - generate_quality_report()
│
├── sample_images/                     # Sample test images
│   ├── cover_image.jpg                # Geometric patterns image
│   ├── gradient_image.jpg             # Gradient + noise image
│   ├── textured_image.jpg             # Textured image
│   └── sample_text.txt                # Sample text file
│
└── output/                            # Output directory
    └── (stego images saved here)
```

---

## File Descriptions

### Documentation Files

#### **README.md** (Main Documentation)
- Project overview
- Installation instructions
- Usage guide
- Feature list
- Technical methodology pipeline
- Performance metrics
- Troubleshooting
- References

**Size**: ~15 KB | **Read Time**: 15-20 minutes

#### **QUICKSTART.md** (Get Started Fast)
- 5-minute setup
- Basic workflow
- Understanding results
- Security tips
- Troubleshooting quick answers
- FAQs

**Size**: ~8 KB | **Read Time**: 5-10 minutes | **START HERE ⭐**

#### **METHODOLOGY.md** (Technical Deep Dive)
- Image preprocessing algorithms
- Canny edge detection mathematics
- AES-256-GCM cryptography
- LSB embedding techniques
- Quality metrics formulas
- Security analysis
- Computational complexity
- Algorithm comparisons

**Size**: ~25 KB | **Read Time**: 30-45 minutes | **For academics**

#### **API_REFERENCE.md** (Developer Guide)
- Detailed API documentation
- Method signatures
- Parameter descriptions
- Return values
- Example code for each method
- Complete workflow example
- Error handling
- Best practices

**Size**: ~20 KB | **Read Time**: 20-30 minutes | **For developers**

#### **LICENSE**
- MIT License terms
- Disclaimer
- Academic use guidelines
- Copyright information

---

### Main Application Files

#### **app.py** (GUI Application)
- Main entry point for users
- Tkinter-based user interface
- Image upload/preview
- Embedding workflow
- Extraction workflow
- Quality metrics display
- Save/load functionality

**Lines**: ~500 | **Type**: Application

#### **test_steganography.py** (Test Suite)
- Unit tests for all modules
- 5 test categories:
  1. Image processing & edge detection
  2. Encryption/decryption
  3. Steganography embedding/extraction
  4. Quality metrics
  5. Edge cases & error handling

**Lines**: ~400 | **Type**: Test | **Run**: `python test_steganography.py`

#### **generate_samples.py** (Data Generation)
- Creates sample images for testing
- Functions:
  - `create_geometric_image()` - Geometric patterns
  - `create_gradient_image()` - Gradient + noise
  - `create_textured_image()` - Highly textured
  - `create_sample_text_file()` - Sample text

**Lines**: ~150 | **Type**: Utility | **Run**: `python generate_samples.py`

#### **setup.py** (Automated Setup)
- Complete project setup automation
- Checks Python version
- Creates directories
- Installs dependencies
- Generates sample images
- Runs tests

**Lines**: ~100 | **Type**: Setup Script | **Run**: `python setup.py`

---

### Core Modules

#### **modules/image_processor.py**
- Class: `ImageProcessor`
- Purpose: Image processing & edge detection
- **Key Methods**:
  - `preprocess()` - Grayscale + Gaussian blur
  - `detect_edges()` - Canny edge detection
  - `create_embedding_mask()` - Generate adaptive mask
  - `get_embedding_capacity()` - Calculate capacity
  - `calculate_histogram()` - Generate histograms
  - `get_image_dimensions()` - Get dimensions
  - `get_original_image()` - Get copy of original
  - `get_grayscale_image()` - Get grayscale
  - `get_edge_map()` - Get edge map

**Lines**: ~200 | **Type**: Core Module

#### **modules/encryption.py**
- Class: `EncryptionManager`
- Purpose: AES-256-GCM encryption
- **Key Methods**:
  - `generate_key_from_password()` - PBKDF2 key derivation
  - `encrypt()` - AES-256-GCM encryption
  - `decrypt()` - AES-256-GCM decryption
  - `encrypt_text()` - Text-specific encryption
  - `decrypt_text()` - Text-specific decryption

**Lines**: ~150 | **Type**: Core Module | **Security**: Military-grade

#### **modules/steganography.py**
- Class: `AdaptiveSteganography`
- Purpose: Adaptive LSB embedding/extraction
- **Key Methods**:
  - `embed_data()` - Embed encrypted data
  - `extract_data()` - Extract encrypted data
  - `calculate_capacity()` - Compute capacity
  - `validate_embedding()` - Pre-embedding validation

**Lines**: ~200 | **Type**: Core Module

#### **modules/metrics.py**
- Class: `ImageMetrics`
- Purpose: Quality metrics calculation
- **Key Methods**:
  - `calculate_mse()` - Mean Squared Error
  - `calculate_psnr()` - Peak Signal-to-Noise Ratio
  - `calculate_ssim()` - Structural Similarity
  - `calculate_bpp()` - Bits Per Pixel
  - `generate_quality_report()` - Comprehensive report

**Lines**: ~200 | **Type**: Core Module

---

### Data Directories

#### **sample_images/**
- **cover_image.jpg** (512×512)
  - Geometric shapes and patterns
  - Good for edge detection testing
  - Size: ~50 KB

- **gradient_image.jpg** (512×512)
  - Gradient background + noise
  - Tests quality metrics
  - Size: ~30 KB

- **textured_image.jpg** (512×512)
  - Highly textured background
  - High embedding capacity
  - Size: ~40 KB

- **sample_text.txt**
  - Sample secret text file
  - For file embedding tests
  - Size: ~0.5 KB

#### **output/**
- Directory for saving stego images
- Auto-created on first run
- Users can organize results here

---

## Statistics

### Code Statistics

| Component | Lines | File Count | Purpose |
|-----------|-------|-----------|---------|
| Core Modules | ~750 | 4 | Algorithms & logic |
| GUI Application | ~500 | 1 | User interface |
| Tests & Utils | ~650 | 3 | Testing & setup |
| Documentation | ~60K | 5 | Knowledge base |
| **Total** | **~1900** | **13** | Complete system |

### Module Statistics

| Module | Classes | Methods | LOC |
|--------|---------|---------|-----|
| image_processor.py | 1 | 9 | 200 |
| encryption.py | 1 | 5 | 150 |
| steganography.py | 1 | 4 | 200 |
| metrics.py | 1 | 5 | 200 |
| app.py | 1 | 18 | 500 |
| **Total** | **5** | **41** | **1250** |

---

## File Size Reference

### Documentation
| File | Size |
|------|------|
| README.md | ~15 KB |
| METHODOLOGY.md | ~25 KB |
| API_REFERENCE.md | ~20 KB |
| QUICKSTART.md | ~8 KB |
| **Total Docs** | **~70 KB** |

### Code
| File | Size |
|------|------|
| app.py | ~20 KB |
| test_steganography.py | ~15 KB |
| Modules (4 files) | ~30 KB |
| Other scripts | ~10 KB |
| **Total Code** | **~75 KB** |

### Data
| Directory | Size |
|-----------|------|
| sample_images/ | ~120 KB |
| **Total Data** | **~120 KB** |

### **Total Project Size**: ~265 KB

---

## Dependency Tree

```
app.py
├── tkinter (built-in)
├── PIL (Pillow) - Image display
├── cv2 (OpenCV)
│   └── numpy
│
└── modules/
    ├── image_processor.py
    │   ├── cv2 (OpenCV)
    │   └── numpy
    │
    ├── encryption.py
    │   └── PyCryptodome
    │
    ├── steganography.py
    │   └── numpy
    │
    └── metrics.py
        ├── numpy
        ├── cv2 (OpenCV)
        └── (optional) matplotlib
```

---

## Quick File Reference

| Task | File to Use |
|------|-------------|
| Run application | `python app.py` |
| Generate samples | `python generate_samples.py` |
| Run tests | `python test_steganography.py` |
| Automated setup | `python setup.py` |
| Read intro | `QUICKSTART.md` |
| Learn techniques | `METHODOLOGY.md` |
| Develop code | `API_REFERENCE.md` |
| Full docs | `README.md` |

---

## Getting Started Checklist

- [ ] Read QUICKSTART.md (5 min)
- [ ] Run `pip install -r requirements.txt` (2 min)
- [ ] Run `python generate_samples.py` (1 min)
- [ ] Run `python test_steganography.py` (1 min)
- [ ] Run `python app.py` (launches GUI)
- [ ] Try embedding a message
- [ ] Try extracting the message
- [ ] Read METHODOLOGY.md if interested in theory

---

**Project Structure Version**: 1.0  
**Status**: Complete & Documented  
**Last Updated**: 2024
