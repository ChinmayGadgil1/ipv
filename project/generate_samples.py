"""
Sample Image Generator
Creates test images for the steganography project
"""

import cv2
import numpy as np
import os


def create_geometric_image(filename, width=512, height=512):
    """
    Create an image with geometric patterns and textures
    Good for edge detection testing
    """
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Draw geometric shapes
    cv2.rectangle(image, (50, 50), (200, 200), (255, 100, 50), -1)
    cv2.circle(image, (400, 100), 80, (50, 200, 255), -1)
    cv2.rectangle(image, (100, 350), (350, 450), (150, 255, 100), -1)
    
    # Draw lines
    cv2.line(image, (0, 0), (width, height), (0, 0, 0), 3)
    cv2.line(image, (0, height), (width, 0), (0, 0, 0), 3)
    
    # Add texture
    for i in range(0, height, 50):
        cv2.line(image, (0, i), (width, i), (200, 200, 200), 1)
    for i in range(0, width, 50):
        cv2.line(image, (i, 0), (i, height), (200, 200, 200), 1)
    
    # Add text
    cv2.putText(image, "Test Image", (height//2 - 100, width//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    
    cv2.imwrite(filename, image)
    print(f"✓ Created: {filename}")


def create_gradient_image(filename, width=512, height=512):
    """
    Create a gradient image for quality metric testing
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create gradient
    for i in range(height):
        for j in range(width):
            image[i, j, 0] = int((j / width) * 255)  # Blue gradient
            image[i, j, 1] = int((i / height) * 255)  # Green gradient
            image[i, j, 2] = 128  # Red constant
    
    # Add some random noise
    noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
    image = cv2.addWeighted(image, 0.8, noise.astype(np.uint8), 0.2, 0)
    
    cv2.imwrite(filename, image)
    print(f"✓ Created: {filename}")


def create_textured_image(filename, width=512, height=512):
    """
    Create a highly textured image (good for embedding)
    """
    image = np.random.randint(100, 200, (height, width, 3), dtype=np.uint8)
    
    # Apply Gaussian blur to make it smoother but keep texture
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Add some patterns
    for i in range(0, height, 30):
        cv2.line(image, (0, i), (width, i), (50, 100, 200), 2)
    for j in range(0, width, 30):
        cv2.line(image, (j, 0), (j, height), (50, 100, 200), 2)
    
    cv2.imwrite(filename, image)
    print(f"✓ Created: {filename}")


def create_sample_text_file(filename):
    """
    Create a sample text file for embedding
    """
    content = """
    SAMPLE SECRET TEXT FILE
    =======================
    
    This is a sample secret text file that can be embedded
    into images using the steganography system.
    
    Key Features:
    - Supports any text content
    - Works with special characters
    - Unicode support
    - Multiple languages
    
    Example:
    This system can hide messages in images securely.
    
    You can also hide longer documents or files.
    The encryption ensures confidentiality.
    
    Happy Steganography!
    """.strip()
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✓ Created: {filename}")


def main():
    """
    Generate all sample images and files
    """
    print("\\nGenerating Sample Images for Testing")
    print("=" * 50)
    
    os.makedirs("sample_images", exist_ok=True)
    
    # Create different types of images
    print("\\nCreating test images...")
    create_geometric_image("sample_images/cover_image.jpg")
    create_gradient_image("sample_images/gradient_image.jpg")
    create_textured_image("sample_images/textured_image.jpg")
    
    # Create sample files
    print("\\nCreating sample files...")
    create_sample_text_file("sample_images/sample_text.txt")
    
    print("\\n" + "=" * 50)
    print("✓ All sample images created successfully!")
    print("\\nGenerated files:")
    print("  - sample_images/cover_image.jpg (Geometric patterns)")
    print("  - sample_images/gradient_image.jpg (Gradient + noise)")
    print("  - sample_images/textured_image.jpg (Texture + patterns)")
    print("  - sample_images/sample_text.txt (Sample text file)")


if __name__ == "__main__":
    main()
