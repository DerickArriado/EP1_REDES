import os
from tkinter import filedialog, messagebox
from .save_png import save_canvas_as_png

class ImageHandler:
    def __init__(self, canvas, cliente):
        self.canvas = canvas
        self.cliente = cliente
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
        """Salva a imagem localmente e a envia pelo socket"""
        try:
            # salvar PNG para obter os bytes (simplificado para o essencial)
            temp_filepath = "temp_drawing_to_send.png" # Salva temporariamente
            save_canvas_as_png(self.canvas, temp_filepath)
            
            with open(temp_filepath, "rb") as file:
                image_bytes = file.read()

            # enviar o tamanho da imagem (já tratado pelo enviar_binario)
            # enviar a imagem em bytes (BINÁRIO)
            self.cliente.enviar_imagem(image_bytes)
            
            messagebox.showinfo("Success", f"Image sent! Size: {len(image_bytes)} bytes")
            
            # opcional: remover arquivo temporário
            os.remove(temp_filepath)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send image: {e}")

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
