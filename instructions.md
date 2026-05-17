Build a complete project called “Adaptive Encrypted Image Steganography Using Edge-Based Image Processing”.

Tech Stack:
- Python
- OpenCV
- NumPy
- PyCryptodome
- Tkinter or Flask for GUI
- Matplotlib for analysis graphs

Project Goal:
Create a secure image steganography system that hides encrypted secret messages/files inside images using adaptive edge-based embedding techniques instead of simple traditional LSB hiding.

Core Features:
1. Upload cover image
2. Enter secret text message or choose secret file
3. Encrypt message using AES encryption with password/key
4. Perform edge detection on image using Canny Edge Detection
5. Embed encrypted data only inside edge/high-texture regions
6. Generate stego image
7. Extract hidden data from stego image
8. Decrypt extracted data using correct key
9. Display recovered message/file

Image Processing Requirements:
- Use OpenCV for image preprocessing
- Use grayscale conversion
- Apply Gaussian blur before edge detection
- Use Canny edge detection
- Create adaptive embedding mask using detected edges
- Perform Least Significant Bit (LSB) embedding only on edge pixels

Security Features:
- AES encryption before embedding
- Password-based encryption/decryption
- Wrong password handling
- Capacity checking before embedding

Analysis & Evaluation Features:
- Calculate PSNR (Peak Signal-to-Noise Ratio)
- Calculate MSE (Mean Squared Error)
- Compare original image and stego image histograms
- Show side-by-side comparison images
- Generate graphs/charts using matplotlib

Project Modules:
1. image_processor.py
   - preprocessing
   - edge detection
   - histogram generation

2. encryption.py
   - AES encryption/decryption
   - key generation

3. steganography.py
   - adaptive LSB embedding
   - extraction logic

4. metrics.py
   - PSNR calculation
   - MSE calculation
   - quality analysis

5. app.py
   - GUI or Flask web app
   - upload/download functionality

GUI Requirements:
- Modern clean interface
- Upload image button
- Message input field
- Password input
- Encode button
- Decode button
- Preview original and stego images
- Display PSNR/MSE results
- Save output image

Additional Requirements:
- Use modular and well-commented code
- Explain every major function
- Include proper exception handling
- Add sample images for testing
- Create README.md with:
  - project explanation
  - installation steps
  - methodology
  - algorithms used
  - screenshots
  - future scope

Required Methodology Pipeline:
Input Image
↓
Preprocessing
↓
Edge Detection
↓
AES Encryption
↓
Adaptive LSB Embedding
↓
Stego Image
↓
Extraction
↓
AES Decryption
↓
Recovered Message

Advanced Features (Optional but Preferred):
- Support hiding text files/PDFs
- Multi-image embedding
- SSIM calculation
- Frequency-domain embedding (DCT)
- Steganalysis detection module
- Dark mode UI
- Drag-and-drop support

Output Expectations:
- Fully working project
- Professional folder structure
- Clean UI
- Detailed comments
- Ready for academic presentation/viva
- Include sample outputs and evaluation results