# Technical Methodology & Algorithm Details

## 1. Image Preprocessing Pipeline

### 1.1 Grayscale Conversion
**Purpose**: Reduce computational complexity and noise sensitivity

**Implementation**:
```
Grayscale = 0.299·R + 0.587·G + 0.114·B
```

**Advantages**:
- Reduces data dimensionality (3 channels → 1)
- Edge detection works better on single channel
- Faster processing
- Maintains structural information

### 1.2 Gaussian Blur
**Purpose**: Reduce high-frequency noise before edge detection

**Parameters**:
- Kernel Size: 5×5
- Sigma (σ): 1.0

**Mathematical Formulation**:
$$G(x,y) = \frac{1}{2\pi\sigma^2}\exp\left(-\frac{x^2+y^2}{2\sigma^2}\right)$$

**Benefits**:
- Eliminates noise that would cause false edge detection
- Smooths while preserving major features
- Reduces computational load

---

## 2. Canny Edge Detection Algorithm

### 2.1 Algorithm Steps

#### Step 1: Gradient Computation
Compute intensity gradients using Sobel operators:

$$G_x = \begin{bmatrix} -1 & 0 & 1 \\\\ -2 & 0 & 2 \\\\ -1 & 0 & 1 \end{bmatrix}$$

$$G_y = \begin{bmatrix} -1 & -2 & -1 \\\\ 0 & 0 & 0 \\\\ 1 & 2 & 1 \end{bmatrix}$$

Magnitude:
$$M(x,y) = \sqrt{G_x^2 + G_y^2}$$

Direction:
$$\theta(x,y) = \arctan(G_y / G_x)$$

#### Step 2: Non-Maximum Suppression
Suppress gradients not aligned with edge direction:
- For each pixel, compare gradient with neighbors along gradient direction
- Keep only local maxima

#### Step 3: Double Threshold
Classify pixels into three categories:
- **Strong edges**: Gradient > T_high (150)
- **Weak edges**: T_low < Gradient ≤ T_high (50-150)
- **Non-edges**: Gradient ≤ T_low (50)

#### Step 4: Edge Tracking by Hysteresis
- Include strong edges in final edge map
- Include weak edges only if connected to strong edges
- Eliminates isolated weak edges (noise)

### 2.2 Our Parameters

```python
Lower Threshold (T_low):  50
Upper Threshold (T_high): 150
Kernel Size:             5×5
```

**Rationale**:
- Lower threshold captures more edge details
- Upper threshold eliminates noise
- Ratio 1:3 provides good noise-edge balance

---

## 3. Adaptive Embedding Mask Generation

### 3.1 Mask Creation Process

```
Edge Map (binary) → Morphological Dilation → Embedding Mask
```

**Dilation Operation**:
$$\text{Dilation}(A, B) = \{z \mid B_z \cap A \neq \emptyset\}$$

**Structuring Element**:
```
Elliptical kernel (3×3):
    0 1 0
    1 1 1
    0 1 0
```

**Iterations**: 1 dilation pass

**Purpose**:
- Expand edge regions slightly
- Create thicker embedding zones
- Improve connectivity of edge pixels

### 3.2 Embedding Capacity Calculation

```python
Edge_Pixels = Count of pixels with mask value > 0
Total_Bits = Edge_Pixels × 3          # 3 channels, 1 bit each
Total_Bytes = (Total_Bits - 32) / 8   # Subtract 4-byte header
Capacity = Total_Bytes
```

**Capacity Formula**:
$$C = \left\lfloor \frac{E \times 3 - 32}{8} \right\rfloor$$

Where:
- C = Capacity (bytes)
- E = Number of edge pixels

---

## 4. AES-256-GCM Encryption

### 4.1 Key Derivation (PBKDF2)

**Algorithm**: PBKDF2-SHA256

**Formula**:
$$DK = \text{PBKDF2}(\text{password}, \text{salt}, \text{iterations}, \text{dkLen})$$

**Parameters**:
- Hash Function: SHA-256
- Salt Length: 128 bits (16 bytes)
- Iterations: 100,000
- Key Length: 256 bits (32 bytes)

**Security Analysis**:
- 100,000 iterations provides ~0.1s computation time
- Resistant to brute-force attacks
- Unique salt prevents pre-computation attacks
- High iteration count increases attacker computational cost

### 4.2 AES-256-GCM Mode

**Components**:
- **Cipher**: AES (Rijndael)
- **Block Size**: 128 bits
- **Key Size**: 256 bits
- **Mode**: GCM (Galois/Counter Mode)
- **Nonce**: 96 bits (12 bytes)
- **Authentication Tag**: 128 bits (16 bytes)

**Encryption Process**:
```
1. Generate random nonce
2. Counter mode for encryption
3. Parallel GF(2^128) polynomial evaluation
4. Generate authentication tag
```

**Authentication**:
$$\text{Tag} = \text{GHASH}(\text{H}, \text{ciphertext})$$

**Format of Encrypted Data**:
```
[Salt (16B)] + [Nonce (12B)] + [Ciphertext] + [Tag (16B)]
```

**Total Overhead**: 44 bytes per message

---

## 5. Adaptive LSB Embedding

### 5.1 LSB Embedding Technique

**Least Significant Bit (LSB)**:
For a pixel channel value P (0-255):
- MSB (Most Significant): High bits determine primary color
- LSB (Least Significant): Low bit has minimal visual impact

**Embedding Process**:
```
For each edge pixel (x, y) with channels B, G, R:
    For each channel C:
        bit = next bit from encrypted data
        P_new = (P_old & 0xFE) | bit
        Replace P_old with P_new
```

**Visual Impact Analysis**:
- Changing LSB changes pixel value by ≤1
- Imperceptible to human vision
- PSNR typically > 40 dB

### 5.2 Data Header

**Purpose**: Enable extraction of correct data length

**Format**:
```
Bits 0-31: Data Length (32-bit unsigned integer, big-endian)
Bits 32+: Encrypted Data
```

**Example**:
```
Message: "Hello" (5 bytes)
Encrypted: 50 bytes
Header: 0x00000032 (50 in hex)
Embedded bits: [header bits] + [data bits]
```

### 5.3 Embedding Order

**Sequential Scanning**:
1. Scan image top-to-bottom, left-to-right
2. For each edge pixel: embed in B channel, then G, then R
3. Continue until all data embedded

**Algorithm**:
```python
edge_coords = find_all_edge_coordinates(mask)
for y, x in edge_coords:
    for channel in [B, G, R]:
        if bit_index >= len(bit_stream):
            break
        image[y, x, channel] = embed_bit(...)
        bit_index += 1
```

---

## 6. Extraction Process

### 6.1 Reverse LSB Extraction

**Process**:
```
For each edge pixel (x, y):
    For each channel C:
        bit = image[y, x, C] & 0x01  # Extract LSB
        bit_stream += bit
```

**Data Recovery**:
1. Extract first 32 bits → data length L
2. Extract next L×8 bits → encrypted data
3. Terminate extraction

### 6.2 Validation

**Checks Performed**:
1. Minimum bits available (≥ 32 for header)
2. Data length ≤ available bits
3. Successful GCM authentication upon decryption

---

## 7. Quality Metrics

### 7.1 Mean Squared Error (MSE)

**Formula**:
$$\text{MSE} = \frac{1}{N} \sum_{i=0}^{N-1} (I_{\text{orig}}[i] - I_{\text{stego}}[i])^2$$

**Interpretation**:
- Lower values → better imperceptibility
- Typical range for LSB: 0.5-2.0
- Imperceptible changes: MSE < 5

### 7.2 Peak Signal-to-Noise Ratio (PSNR)

**Formula**:
$$\text{PSNR} = 20 \log_{10}\left(\frac{255}{\sqrt{\text{MSE}}}\right)$$

**Units**: Decibels (dB)

**Quality Scale**:
- \> 50 dB: Imperceptible changes
- 40-50 dB: Imperceptible/difficult to detect
- 30-40 dB: Visible distortion
- \< 30 dB: Significant distortion

**Our Typical Results**: 45-50 dB

### 7.3 Structural Similarity Index (SSIM)

**Complex Formula**:
$$\text{SSIM}(x,y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$

Where:
- μ_x, μ_y: Local means
- σ_x², σ_y²: Local variances
- σ_xy: Covariance
- C_1, C_2: Stabilization constants

**Interpretation**:
- Range: -1 to 1
- 1 = Identical images
- \> 0.95: Imperceptible differences
- \< 0.5: Noticeable differences

### 7.4 Bits Per Pixel (BPP)

**Formula**:
$$\text{BPP} = \frac{\text{Total Data Bits}}{\text{Total Image Pixels}}$$

**Significance**:
- Measures embedding capacity vs. image size
- Our adaptive LSB: typically 0.5-2 BPP
- Traditional LSB: 0-3 BPP
- DCT-based: 0.1-0.5 BPP

---

## 8. Security Analysis

### 8.1 Encryption Security

**Threat Model**: Ciphertext-only attack

**AES-256 Security**:
- Key space: 2^256 ≈ 1.16 × 10^77 possibilities
- No known practical attacks on AES-256
- NIST approved (FIPS 197)

**GCM Authentication**:
- Prevents tampering detection
- Tag forgery probability: 2^-128
- Detects bit-level modifications

### 8.2 Steganography Security

**Steganalysis Resistance**:
- Edge-based embedding harder to detect than random LSB
- PSNR > 40 dB defeats basic statistical analysis
- Local entropy preservation

**Vulnerabilities**:
- Does not survive lossy compression
- Detectable with steganalysis tools (SVM-based)
- Vulnerable to targeted attacks (histogram analysis)

### 8.3 Overall Security Level

**Classification**: Secure for civilian applications

**Recommended Uses**:
- Protecting sensitive personal documents
- Covert communication in trusted networks
- Academic/research applications

**Not Recommended For**:
- Classified government communications
- High-stakes espionage scenarios
- Protection against sophisticated adversaries

---

## 9. Robustness Analysis

### 9.1 Robustness to Image Modifications

| Modification | Robustness | Comments |
|---|---|---|
| Slight brightness change | Low | LSB changes easily with tone adjustment |
| Small rotation | Low | Pixel positions change |
| JPEG compression (90%) | Low | Block rounding destroys LSB |
| Gaussian blur | Medium | Spatial information preserved |
| Edge detection-based | High | By design |

### 9.2 Capacity-Security Tradeoff

```
Higher Capacity
    ↓
More edge pixels used
    ↓
Easier detection
    ↓
Lower Security

Lower Capacity
    ↓
Fewer edge pixels used
    ↓
Harder detection
    ↓
Higher Security
```

**Recommended Balance**: 50% of capacity utilization

---

## 10. Computational Complexity

### 10.1 Time Complexity

| Operation | Complexity | Typical Time |
|---|---|---|
| Image preprocessing | O(W×H) | 10-20 ms |
| Edge detection (Canny) | O(W×H) | 30-50 ms |
| AES encryption | O(n) | 5-10 ms |
| LSB embedding | O(E×3) | 20-40 ms |
| **Total** | **O(W×H + n)** | **~100 ms** |

### 10.2 Space Complexity

| Component | Space Required |
|---|---|
| Original image | W×H×3 bytes |
| Grayscale | W×H bytes |
| Edge map | W×H bytes |
| Stego image | W×H×3 bytes |
| **Total** | **~3.5 W×H** |

For 512×512 image: ~950 KB total

---

## 11. Comparison with Other Methods

| Method | Capacity | Security | Imperceptibility | PSNR |
|---|---|---|---|---|
| Simple LSB | High (3 BPP) | Low | Good | 50-60 dB |
| DCT | Low (0.1-0.5 BPP) | Medium | Excellent | 55-65 dB |
| **Our Method** | **Medium (0.5-2 BPP)** | **High** | **Excellent** | **45-50 dB** |
| Wavelet | Medium | Medium | Good | 45-55 dB |

**Advantages of Our Approach**:
1. Adaptive embedding in edges (harder to detect)
2. Military-grade encryption (AES-256-GCM)
3. Good capacity-security balance
4. Imperceptible visual changes

---

## 12. Future Enhancements

### 12.1 DCT-based Embedding
- Replace LSB with DCT coefficient modification
- Better robustness to compression
- Lower capacity but better security

### 12.2 Multi-image Schemes
- Distribute data across multiple images
- Require all images for extraction
- Enhanced security through redundancy

### 12.3 Steganalysis Detection
- Train ML model to detect steganography
- Implement counter-measures
- Adaptive embedding adjustment

### 12.4 Quaternion Transform
- Use color channel relationships
- Better camouflage in color images
- Advanced mathematical framework

---

## References

1. Canny, J. (1986). "A computational approach to edge detection." IEEE TPAMI.
2. NIST FIPS 197. "Advanced Encryption Standard (AES)."
3. Bellare, M., Desai, A., Jokipii, E., & Rogaway, P. (2000). "A concrete security treatment of symmetric encryption."
4. Kutter, M., & Petitcolas, F. P. (1999). "A fair benchmark for image watermarking systems."
5. Petitcolas, F. A., Anderson, R. J., & Kuhn, M. G. (1998). "Information hiding—a survey."

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Status**: Complete
