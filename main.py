import tkinter as tk
from tkinter import filedialog, messagebox
from save_png import save_canvas_as_png  # importar a função de salvamento

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame para os botões
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)
        
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
        
        # Bind events para desenho
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
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

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
