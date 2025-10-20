import tkinter as tk
from chat_widget import ChatWidget
from image_handler import ImageHandler
from drawing_tools import DrawingTools

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        # Inicializa o canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Inicializa componentes
        self.setup_toolbar()
        self.drawing_tools = DrawingTools(self.canvas)
        self.image_handler = ImageHandler(self.canvas)
        self.chat_widget = ChatWidget(root)
        
        # Configura bindings
        self.setup_bindings()

    def setup_toolbar(self):
        """Configura a barra de ferramentas"""
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        # Botões de modo
        self.eraser_btn = tk.Button(self.button_frame, text="Eraser", command=self.set_eraser_mode, bg="#A8EEFF")
        self.eraser_btn.pack(side=tk.LEFT, padx=5)

        self.draw_button = tk.Button(self.button_frame, text="Draw", command=self.set_draw_mode, bg="#b5e7a9", relief=tk.SUNKEN)
        self.draw_button.pack(side=tk.LEFT, padx=5)
        
        # Controles de cor e espessura
        tk.Label(self.button_frame, text="Color:").pack(side=tk.LEFT, padx=5)
        self.color_var = tk.StringVar(value="black")
        tk.Entry(self.button_frame, textvariable=self.color_var, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.button_frame, text="Thickness:").pack(side=tk.LEFT, padx=5)
        self.thickness_var = tk.IntVar(value=2)
        tk.Entry(self.button_frame, textvariable=self.thickness_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Botões de ação
        tk.Button(self.button_frame, text="Clear Canvas", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Save as PNG", command=self.save_as_png).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Send Image", command=self.send_image).pack(side=tk.LEFT, padx=5)

    def setup_bindings(self):
        """Configura os eventos do mouse"""
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def set_eraser_mode(self):
        self.drawing_tools.set_mode("erase")

    def set_draw_mode(self):
        self.drawing_tools.set_mode("draw")

    def start_drawing(self, event):
        self.drawing_tools.start_drawing(event)

    def draw(self, event):
        color = self.color_var.get()
        thickness = self.thickness_var.get()
        self.drawing_tools.draw(event, color, thickness)

    def stop_drawing(self, event):
        self.drawing_tools.stop_drawing()

    def clear_canvas(self):
        self.drawing_tools.clear_canvas()
    
    def save_as_png(self):
        self.image_handler.save_as_png()

    def send_image(self):
        self.image_handler.send_image()