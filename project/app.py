"""
Adaptive Encrypted Image Steganography - GUI Application
Main application using Tkinter for user interface
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.image_processor import ImageProcessor
from modules.encryption import EncryptionManager
from modules.steganography import AdaptiveSteganography
from modules.metrics import ImageMetrics


class SteganographyApp:
    """
    Main GUI application for adaptive encrypted image steganography
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application
        """
        self.root = root
        self.root.title("Adaptive Encrypted Image Steganography System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.resizable(True, True)
        
        # Set style
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Initialize variables
        self.original_image = None
        self.stego_image = None
        self.image_processor = None
        self.edge_mask = None
        self.encrypted_data = None
        self.original_image_path = None
        self.selected_file_path = None  # Store full path to selected file
        self.selected_file_path = None  # Store full path to selected file
        
        # Create GUI
        self.create_widgets()
    
    def create_widgets(self):
        """
        Create and layout GUI widgets with tabbed interface
        """
        # Top title bar
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        title = ttk.Label(title_frame, text="🔐 Adaptive Encrypted Image Steganography System", font=("Arial", 14, "bold"))
        title.pack()
        
        # Create tabbed interface
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ============ TAB 1: EMBED MESSAGE ============
        embed_tab = ttk.Frame(notebook, padding=15)
        notebook.add(embed_tab, text="📤 Embed Message")
        
        # Left panel for embed controls
        embed_left = ttk.Frame(embed_tab)
        embed_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
        
        # Image upload section
        img_frame = ttk.LabelFrame(embed_left, text="1. Select Image", padding=10)
        img_frame.pack(fill=tk.X, pady=5)
        ttk.Button(img_frame, text="📁 Upload Image", command=self.load_image, width=20).pack(fill=tk.X, pady=5)
        self.image_label = ttk.Label(img_frame, text="No image selected", foreground="gray", wraplength=200)
        self.image_label.pack(fill=tk.X, pady=5)
        
        # Mode selection
        mode_frame = ttk.LabelFrame(embed_left, text="2. Data Type", padding=10)
        mode_frame.pack(fill=tk.X, pady=5)
        self.mode_var = tk.StringVar(value="text")
        ttk.Radiobutton(mode_frame, text="Text Message", variable=self.mode_var, value="text").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Hide File", variable=self.mode_var, value="file").pack(anchor=tk.W)
        
        # Message input
        msg_frame = ttk.LabelFrame(embed_left, text="3. Secret Data", padding=10)
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Label(msg_frame, text="Your message:").pack(anchor=tk.W)
        self.message_text = tk.Text(msg_frame, height=5, width=30)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Button(msg_frame, text="📄 Select File", command=self.select_file).pack(fill=tk.X, pady=3)
        self.file_label = ttk.Label(msg_frame, text="No file selected", foreground="gray", wraplength=200)
        self.file_label.pack(fill=tk.X)
        
        # Password input
        pwd_frame = ttk.LabelFrame(embed_left, text="4. Encryption Password", padding=10)
        pwd_frame.pack(fill=tk.X, pady=5)
        ttk.Label(pwd_frame, text="Password:").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(pwd_frame, show="•", width=25)
        self.password_entry.pack(fill=tk.X, pady=3)
        ttk.Label(pwd_frame, text="Confirm:").pack(anchor=tk.W)
        self.confirm_pwd_entry = ttk.Entry(pwd_frame, show="•", width=25)
        self.confirm_pwd_entry.pack(fill=tk.X, pady=3)
        
        # Embed button
        embed_btn_frame = ttk.Frame(embed_left)
        embed_btn_frame.pack(fill=tk.X, pady=10)
        self.embed_btn = ttk.Button(embed_btn_frame, text="✅ EMBED DATA", command=self.embed_data)
        self.embed_btn.pack(fill=tk.X, pady=5)
        ttk.Button(embed_btn_frame, text="💾 Save Stego Image", command=self.save_stego_image).pack(fill=tk.X, pady=3)
        
        # Right panel for preview
        embed_right = ttk.Frame(embed_tab)
        embed_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        preview_frame = ttk.LabelFrame(embed_right, text="Image Preview", padding=5)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        col1 = ttk.Frame(canvas_frame)
        col1.pack(side=tk.LEFT, padx=5)
        self.original_canvas = tk.Canvas(col1, width=200, height=200, bg='lightgray')
        self.original_canvas.pack()
        ttk.Label(col1, text="Original Image", font=("Arial", 10, "bold")).pack()
        
        col2 = ttk.Frame(canvas_frame)
        col2.pack(side=tk.RIGHT, padx=5)
        self.stego_canvas = tk.Canvas(col2, width=200, height=200, bg='lightgray')
        self.stego_canvas.pack()
        ttk.Label(col2, text="Stego Image", font=("Arial", 10, "bold")).pack()
        
        # Status for embed
        status_frame = ttk.LabelFrame(embed_right, text="Status & Metrics", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(status_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_text = tk.Text(status_frame, height=12, width=40, yscrollcommand=scrollbar.set)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.status_text.yview)
        
        self.status_text.insert(tk.END, "📢 Ready to embed...\n")
        self.status_text.config(state=tk.DISABLED)
        
        # ============ TAB 2: EXTRACT MESSAGE ============
        extract_tab = ttk.Frame(notebook, padding=15)
        notebook.add(extract_tab, text="📥 Extract Message")
        
        # Left panel for extract controls
        extract_left = ttk.Frame(extract_tab)
        extract_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
        
        # Stego image selection
        stego_frame = ttk.LabelFrame(extract_left, text="1. Select Stego Image", padding=10)
        stego_frame.pack(fill=tk.X, pady=5)
        ttk.Button(stego_frame, text="📁 Load Stego Image", command=self.load_stego_image, width=20).pack(fill=tk.X, pady=5)
        self.stego_label = ttk.Label(stego_frame, text="No image selected", foreground="gray", wraplength=200)
        self.stego_label.pack(fill=tk.X, pady=5)
        
        # Decryption password
        decrypt_pwd_frame = ttk.LabelFrame(extract_left, text="2. Enter Decryption Password", padding=10)
        decrypt_pwd_frame.pack(fill=tk.X, pady=5)
        ttk.Label(decrypt_pwd_frame, text="Password:").pack(anchor=tk.W)
        self.extract_pwd_entry = ttk.Entry(decrypt_pwd_frame, show="•", width=25)
        self.extract_pwd_entry.pack(fill=tk.X, pady=5)
        
        # Extract button
        extract_btn_frame = ttk.Frame(extract_left)
        extract_btn_frame.pack(fill=tk.X, pady=10)
        extract_btn = ttk.Button(extract_btn_frame, text="🔓 EXTRACT & DECRYPT", command=self.extract_data)
        extract_btn.pack(fill=tk.X, pady=5)
        
        # Recovered message display
        recovered_frame = ttk.LabelFrame(extract_left, text="3. Recovered Data", padding=10)
        recovered_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Label(recovered_frame, text="Extracted message:").pack(anchor=tk.W)
        self.recovered_text = tk.Text(recovered_frame, height=6, width=30)
        self.recovered_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Right panel for extract status
        extract_right = ttk.Frame(extract_tab)
        extract_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        extract_status_frame = ttk.LabelFrame(extract_right, text="Status & Information", padding=10)
        extract_status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar2 = ttk.Scrollbar(extract_status_frame)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.extract_status_text = tk.Text(extract_status_frame, height=15, width=40, yscrollcommand=scrollbar2.set)
        self.extract_status_text.pack(fill=tk.BOTH, expand=True)
        scrollbar2.config(command=self.extract_status_text.yview)
        
        self.extract_status_text.insert(tk.END, "📢 Ready to extract...\n")
        self.extract_status_text.config(state=tk.DISABLED)
        
        stego_preview = ttk.LabelFrame(extract_right, text="Stego Image Preview", padding=5)
        stego_preview.pack(fill=tk.BOTH, expand=True, pady=5)
        self.stego_preview_canvas = tk.Canvas(stego_preview, width=250, height=250, bg='lightgray')
        self.stego_preview_canvas.pack()
        
        # Bottom buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        
        ttk.Button(button_frame, text="🔄 Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def load_image(self):
        """
        Load original image
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.original_image_path = file_path
                self.original_image = cv2.imread(file_path)
                self.image_processor = ImageProcessor(file_path)
                
                # Preprocess and detect edges
                self.image_processor.preprocess()
                self.edge_mask = self.image_processor.create_embedding_mask()
                
                # Display image
                self.display_image(self.original_image, self.original_canvas)
                
                # Update status
                height, width = self.image_processor.get_image_dimensions()
                capacity = AdaptiveSteganography.calculate_capacity(self.edge_mask)
                
                self.image_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                self.update_status(f"Image loaded successfully\nDimensions: {width}x{height}\n"
                                 f"Embedding capacity: {capacity} bytes\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def select_file(self):
        """
        Select a file to hide
        """
        file_path = filedialog.askopenfilename(title="Select File to Hide")
        
        if file_path:
            self.selected_file_path = file_path  # Store full path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
    
    def load_stego_image(self):
        """
        Load stego image for extraction
        """
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.stego_image = cv2.imread(file_path)
                self.display_image(self.stego_image, self.stego_preview_canvas)
                self.stego_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                self.update_status("Stego image loaded successfully\n", is_extract=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load stego image: {str(e)}")
    
    def embed_data(self):
        """
        Embed data into image
        """
        try:
            # Validate inputs
            if self.original_image is None:
                messagebox.showwarning("Warning", "Please load an image first")
                return
            
            password = self.password_entry.get()
            confirm_pwd = self.confirm_pwd_entry.get()
            
            if not password:
                messagebox.showwarning("Warning", "Please enter a password")
                return
            
            if password != confirm_pwd:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Get data to embed
            if self.mode_var.get() == "text":
                message = self.message_text.get("1.0", tk.END).strip()
                if not message:
                    messagebox.showwarning("Warning", "Please enter a message")
                    return
                data = message.encode('utf-8')
            else:
                if self.selected_file_path is None:
                    messagebox.showwarning("Warning", "Please select a file")
                    return
                try:
                    with open(self.selected_file_path, 'rb') as f:
                        data = f.read()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"File not found: {self.selected_file_path}")
                    return
            
            # Update status
            self.update_status("Encrypting data...\n")
            self.root.update()
            
            # Encrypt data with metadata if file mode
            if self.mode_var.get() == "file":
                filename = os.path.basename(self.selected_file_path)
                encrypted_data = EncryptionManager.encrypt_file(data, filename, password)
            else:
                encrypted_data = EncryptionManager.encrypt(data, password)
            
            # Validate embedding
            valid, msg = AdaptiveSteganography.validate_embedding(
                self.original_image, encrypted_data, self.edge_mask
            )
            
            if not valid:
                messagebox.showerror("Error", msg)
                return
            
            self.update_status("Embedding data...\n")
            self.root.update()
            
            # Embed data
            self.stego_image, success = AdaptiveSteganography.embed_data(
                self.original_image, encrypted_data, self.edge_mask
            )
            
            if not success:
                messagebox.showerror("Error", "Embedding failed")
                return
            
            # Calculate metrics
            self.update_status("Calculating metrics...\n")
            self.root.update()
            
            metrics = ImageMetrics.generate_quality_report(
                self.original_image, self.stego_image, len(encrypted_data)
            )
            
            # Display results
            self.display_image(self.stego_image, self.stego_canvas)
            
            status_msg = ("Data embedded successfully!\n\n"
                         "=== METRICS ===\n"
                         f"MSE: {metrics['MSE']}\n"
                         f"PSNR: {metrics['PSNR']} dB\n"
                         f"SSIM: {metrics['SSIM']}\n"
                         f"BPP: {metrics['BPP']}\n"
                         f"Data Size: {metrics['Data_Size_Bytes']} bytes\n"
                         f"Image Pixels: {metrics['Image_Pixels']}\n")
            
            self.update_status(status_msg)
            messagebox.showinfo("Success", "Data embedded successfully!\n\n" + status_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Embedding failed: {str(e)}")
    
    def extract_data(self):
        """
        Extract and decrypt data from stego image
        """
        try:
            if self.stego_image is None:
                messagebox.showwarning("Warning", "Please load a stego image first")
                return
            
            password = self.extract_pwd_entry.get()
            
            if not password:
                messagebox.showwarning("Warning", "Please enter password")
                return
            
            # Process stego image to get edge mask
            temp_processor = ImageProcessor.__new__(ImageProcessor)
            temp_processor.original_image = self.stego_image
            temp_processor.image_height, temp_processor.image_width = self.stego_image.shape[:2]
            temp_processor.grayscale = None
            temp_processor.edges = None
            temp_processor.blurred = None
            
            temp_processor.preprocess()
            temp_mask = temp_processor.create_embedding_mask()
            
            self.update_status("Extracting data...\n", is_extract=True)
            self.root.update()
            
            # Extract encrypted data
            encrypted_data = AdaptiveSteganography.extract_data(self.stego_image, temp_mask)
            
            if len(encrypted_data) == 0:
                messagebox.showwarning("Warning", "No hidden data found")
                return
            
            self.update_status("Decrypting data...\n", is_extract=True)
            self.root.update()
            
            # Decrypt data
            try:
                decrypted_data = EncryptionManager.decrypt(encrypted_data, password)
                
                # Try to extract as file first
                file_extracted = False
                filename = None
                
                try:
                    file_data, filename = EncryptionManager.decrypt_file(encrypted_data, password)
                    # Successfully extracted file with metadata
                    result_msg = f"Decryption successful!\n\nExtracted file: {filename}\nSize: {len(file_data)} bytes"
                    self.update_status(result_msg + "\n", is_extract=True)
                    self.recovered_text.config(state=tk.NORMAL)
                    self.recovered_text.delete(1.0, tk.END)
                    self.recovered_text.insert(tk.END, f"File: {filename}\n{len(file_data)} bytes")
                    self.recovered_text.config(state=tk.NORMAL)
                    
                    # Offer to save
                    if messagebox.askyesno("Save File", f"Save extracted file '{filename}'?"):
                        # Default save path with original filename
                        initial_file = filename
                        save_path = filedialog.asksaveasfilename(
                            defaultextension=os.path.splitext(filename)[1],
                            initialfile=initial_file,
                            filetypes=[("All files", "*.*")]
                        )
                        if save_path:
                            with open(save_path, 'wb') as f:
                                f.write(file_data)
                            messagebox.showinfo("Success", f"File saved to {save_path}")
                    
                    file_extracted = True
                    
                except ValueError:
                    # No file metadata - treat as text
                    pass
                
                # If not a file, try as text
                if not file_extracted:
                    try:
                        message = decrypted_data.decode('utf-8')
                        result_msg = f"Decryption successful!\n\nExtracted message:\n{message}"
                        self.update_status(result_msg + "\n", is_extract=True)
                        self.recovered_text.config(state=tk.NORMAL)
                        self.recovered_text.delete(1.0, tk.END)
                        self.recovered_text.insert(tk.END, message)
                        self.recovered_text.config(state=tk.NORMAL)
                        messagebox.showinfo("Success", result_msg)
                    except UnicodeDecodeError:
                        # Binary data
                        result_msg = f"Decryption successful!\n\nExtracted binary data: {len(decrypted_data)} bytes"
                        self.update_status(result_msg + "\n", is_extract=True)
                        
                        # Offer to save
                        if messagebox.askyesno("Save File", "Save extracted data to file?"):
                            save_path = filedialog.asksaveasfilename(filetypes=[("All files", "*.*")])
                            if save_path:
                                with open(save_path, 'wb') as f:
                                    f.write(decrypted_data)
                                messagebox.showinfo("Success", f"File saved to {save_path}")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")
    
    def display_image(self, image, canvas):
        """
        Display image on canvas
        """
        try:
            # Resize for display
            display_size = (200, 200)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_pil.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image_pil)
            canvas.create_image(100, 100, image=photo)
            canvas.photo = photo
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def save_stego_image(self):
        """
        Save stego image to file
        """
        if self.stego_image is None:
            messagebox.showwarning("Warning", "No stego image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.stego_image)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
                self.update_status(f"Stego image saved to {file_path}\n")
                
                # Warn if saving as JPEG
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    messagebox.showwarning(
                        "Format Warning",
                        "⚠ WARNING: You saved as JPEG (lossy compression).\n\n"
                        "IMPORTANT: The data can still be extracted, but JPEG compression\n"
                        "can slightly alter pixel values, which may affect extraction accuracy.\n\n"
                        "For best results, use PNG format for lossless saving.\n"
                        "PNG is recommended for reliable extraction."
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def update_status(self, message, is_extract=False):
        """
        Update status text in appropriate tab
        """
        status_widget = self.extract_status_text if is_extract else self.status_text
        status_widget.config(state=tk.NORMAL)
        status_widget.insert(tk.END, message)
        status_widget.see(tk.END)
        status_widget.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_all(self):
        """
        Clear all data
        """
        if messagebox.askyesno("Clear", "Clear all data?"):
            self.original_image = None
            self.stego_image = None
            self.encrypted_data = None
            self.image_processor = None
            self.edge_mask = None
            self.selected_file_path = None  # Clear selected file path
            
            self.image_label.config(text="No image loaded")
            self.file_label.config(text="No file selected")
            self.stego_label.config(text="No stego image loaded")
            self.message_text.delete("1.0", tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_pwd_entry.delete(0, tk.END)
            self.extract_pwd_entry.delete(0, tk.END)
            self.recovered_text.config(state=tk.NORMAL)
            self.recovered_text.delete("1.0", tk.END)
            self.recovered_text.config(state=tk.NORMAL)
            
            self.original_canvas.create_rectangle(0, 0, 200, 200, fill='lightgray')
            self.stego_canvas.create_rectangle(0, 0, 200, 200, fill='lightgray')
            self.stego_preview_canvas.create_rectangle(0, 0, 250, 250, fill='lightgray')
            
            # Clear both status texts
            self.status_text.config(state=tk.NORMAL)
            self.status_text.delete("1.0", tk.END)
            self.status_text.insert(tk.END, "📢 Ready to embed...\n")
            self.status_text.config(state=tk.DISABLED)
            
            self.extract_status_text.config(state=tk.NORMAL)
            self.extract_status_text.delete("1.0", tk.END)
            self.extract_status_text.insert(tk.END, "📢 Ready to extract...\n")
            self.extract_status_text.config(state=tk.DISABLED)


def main():
    """
    Main entry point
    """
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
