import tkinter as tk
from tkinter import filedialog, messagebox
from save_png import save_canvas_as_png  # importar a função de salvamento
import os
import time

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.mode = "draw" #por padrão
        
        # Frame para os botões
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        self.eraser_btn = tk.Button(self.button_frame, text="Borracha", command=self.set_eraser_mode, bg="#A8EEFF")
        self.eraser_btn.pack(side=tk.LEFT, padx=5)

        self.draw_button = tk.Button(self.button_frame, text="Desenhar", command=self.set_draw_mode, bg="#b5e7a9", relief=tk.SUNKEN)
        self.draw_button.pack(side=tk.LEFT, padx=5)
        
        # Controle de cor
        tk.Label(self.button_frame, text="Color:").pack(side=tk.LEFT, padx=5)
        self.color_var = tk.StringVar(value="black")
        tk.Entry(self.button_frame, textvariable=self.color_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Controle de espessura
        tk.Label(self.button_frame, text="Thickness:").pack(side=tk.LEFT, padx=5)
        self.thickness_var = tk.IntVar(value=2)
        tk.Entry(self.button_frame, textvariable=self.thickness_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Botão para limpar
        tk.Button(self.button_frame, text="Clear Canvas", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        
        # Botão para salvar como PNG
        tk.Button(self.button_frame, text="Save as PNG", command=self.save_as_png).pack(side=tk.LEFT, padx=5)
        
        # Botão para enviar para outra pessoa
        tk.Button(self.button_frame, text="Enviar Imagem", command=self.send_image).pack(side=tk.LEFT, padx=5)
        
        # Bind events para desenho
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def set_eraser_mode(self):
        self.mode = "erase"

    def set_draw_mode(self):
        self.mode = "draw"

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            if self.mode == "erase":
                color = "white"
                thickness = 15
            else:
                try:
                    color = self.color_var.get()
                    thickness = self.thickness_var.get()
                except Exception:
                    color = "black"
                    thickness = 2
            
            x, y = event.x, event.y
            if self.last_x is not None and self.last_y is not None:
                self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    fill=color, width=thickness, capstyle=tk.ROUND
                )
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")
    
    def save_as_png(self):
        """Salva o canvas como PNG usando o módulo save_png."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if not file_path:
            return  # Usuário cancelou
        
        try:
            save_canvas_as_png(self.canvas, file_path)
            messagebox.showinfo("Success", f"Drawing saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def send_image(self):
        try:
            # Obtém o diretório atual onde o código está rodando
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Gera nomes de arquivo com timestamp para evitar sobrescrever
            timestamp = str(int(time.time()))
            png_filename = f"drawing_{timestamp}.png"
            bytes_filename = f"drawing_bytes_{timestamp}.bin"
            
            png_filepath = os.path.join(current_dir, png_filename)
            bytes_filepath = os.path.join(current_dir, bytes_filename)
            
            # Salva a imagem PNG localmente
            try:
                save_canvas_as_png(self.canvas, png_filepath)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PNG file: {e}")
                return
            
            # Lê a imagem salva e converte para bytes
            with open(png_filepath, "rb") as file:
                image_bytes = file.read()
            
            # Salva os bytes em um arquivo separado
            with open(bytes_filepath, "wb") as bytes_file:
                bytes_file.write(image_bytes)
            
            # Mostra informações sobre os arquivos salvos
            messagebox.showinfo("Success", 
                            f"PNG saved as: {png_filename}\n"
                            f"Bytes saved as: {bytes_filename}\n"
                            f"Size: {len(image_bytes)} bytes\n"
                            f"Location: {current_dir}")
            
            print(f"Image saved as PNG: {png_filepath}")
            print(f"Image bytes saved as: {bytes_filepath}")
            print(f"Image size: {len(image_bytes)} bytes")
            
            # ------------- CONVERTE BIN PARA .PNG ----------
            try:
                # Lê o arquivo .bin
                with open(bytes_filepath, "rb") as bin_file:
                    recovered_bytes = bin_file.read()
                
                # Salva como uma nova imagem para testar
                test_filename = f"test_recovered_{timestamp}.png"
                test_filepath = os.path.join(current_dir, test_filename)
                
                with open(test_filepath, "wb") as test_file:
                    test_file.write(recovered_bytes)
                
                # Mostra resultado do teste
                messagebox.showinfo("Conversion Test", 
                                f"Bytes successfully converted back to image!\n"
                                f"Test file: {test_filename}\n"
                                f"File size: {len(recovered_bytes)} bytes")
                
                print(f"Test recovery successful: {test_filepath}")
                print(f"Recovered file size: {len(recovered_bytes)} bytes")
                
            except Exception as e:
                messagebox.showerror("Conversion Test Error", 
                                    f"Failed to convert bytes back to image: {e}")
                print(f"Conversion test failed: {e}")
        
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
