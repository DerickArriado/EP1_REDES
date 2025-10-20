import os
import time
from tkinter import filedialog, messagebox
from save_png import save_canvas_as_png

class ImageHandler:
    def __init__(self, canvas):
        self.canvas = canvas

    def save_as_png(self):
        """Salva o canvas como PNG"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if not file_path:
            return
        
        try:
            save_canvas_as_png(self.canvas, file_path)
            messagebox.showinfo("Success", f"Drawing saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def send_image(self):
        """Salva a imagem localmente e converte para bytes"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            timestamp = str(int(time.time()))
            
            png_filename = f"drawing_{timestamp}.png"
            bytes_filename = f"drawing_bytes_{timestamp}.bin"
            
            png_filepath = os.path.join(current_dir, png_filename)
            bytes_filepath = os.path.join(current_dir, bytes_filename)
            
            # Salva PNG
            try:
                save_canvas_as_png(self.canvas, png_filepath)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PNG: {e}")
                return
            
            # Converte para bytes
            with open(png_filepath, "rb") as file:
                image_bytes = file.read()
            
            # Salva bytes
            with open(bytes_filepath, "wb") as bytes_file:
                bytes_file.write(image_bytes)
            
            # Mostra informações
            messagebox.showinfo("Success", 
                               f"PNG: {png_filename}\n"
                               f"Bytes: {bytes_filename}\n"
                               f"Size: {len(image_bytes)} bytes")
            
            print(f"PNG saved: {png_filepath}")
            print(f"Bytes saved: {bytes_filepath}")
            
            # Testa conversão de volta
            self.test_bytes_conversion(bytes_filepath, timestamp, current_dir)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

    def test_bytes_conversion(self, bytes_filepath, timestamp, current_dir):
        """Testa converter bytes de volta para imagem"""
        try:
            with open(bytes_filepath, "rb") as bin_file:
                recovered_bytes = bin_file.read()
            
            test_filename = f"test_recovered_{timestamp}.png"
            test_filepath = os.path.join(current_dir, test_filename)
            
            with open(test_filepath, "wb") as test_file:
                test_file.write(recovered_bytes)
            
            messagebox.showinfo("Conversion Test", 
                               f"Bytes converted back to image!\n"
                               f"Test file: {test_filename}")
            
            print(f"Test successful: {test_filepath}")
            
        except Exception as e:
            messagebox.showerror("Conversion Error", 
                                f"Failed to convert bytes: {e}")
            print(f"Conversion failed: {e}")