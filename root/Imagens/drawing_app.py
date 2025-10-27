import tkinter as tk

from .image_handler import ImageHandler
from .drawing_tools import DrawingTools

from PIL import Image, ImageTk
import queue

class DrawingApp:
    def __init__(self, root, cliente, event_queue):
        self.root = root
        self.root.title("Drawing App")
        self.cliente = cliente
        self.event_queue = event_queue
        
        # Inicializa o canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Inicializa componentes
        self.setup_toolbar()
        self.drawing_tools = DrawingTools(self.canvas)
        self.image_handler = ImageHandler(self.canvas, self.cliente)

        # Configura bindings
        self.setup_bindings()

        # armazena imagem recebida
        self.photo_image = None
        self.image_item_id = None # ID do objeto no canvas para a imagem enviada

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
    
    def set_guesser_mode(self):
        """Prepara a GUI para o modo Adivinhador (Guesser)."""
        self.drawing_tools.set_mode("none") # Desabilita a drawing_tools
        
        # 🌟 Opcional: Desabilita botões de desenho/salvar
        self.draw_button.config(state=tk.DISABLED)
        self.eraser_btn.config(state=tk.DISABLED)
        # Limpa o canvas para a imagem recebida
        self.canvas.delete("all")
        
        print("GUI em modo Adivinhador. Esperando imagem...")
    
    def check_gui_queue(self):
        """Verifica a fila de eventos da thread de rede e processa-os."""
        try:
            while True:
                # Tenta pegar um item da fila (sem bloqueio)
                event = self.event_queue.get_nowait()
                
                if event['type'] == 'IMAGE_RECEIVED':
                    self.load_image_to_canvas(event['path'])
                
        except queue.Empty:
            pass # Nenhuma mensagem na fila, tudo bem.
        
        # Chama a si mesmo novamente após 100 milissegundos (Polling)
        self.root.after(100, self.check_gui_queue)
    
    def load_image_to_canvas(self, image_path):
        """Carrega e exibe a imagem no canvas do modo Adivinhador."""
        try:
            # Remove a imagem anterior, se houver
            if self.image_item_id:
                self.canvas.delete(self.image_item_id)
            
            # 1. Abre a imagem usando Pillow
            original_image = Image.open(image_path)
            
            # 2. Redimensiona a imagem para caber no canvas (opcional, mas recomendado)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Mantém a proporção (simples)
            original_image.thumbnail((canvas_width, canvas_height))
            
            # 3. Converte para um objeto que o Tkinter pode usar
            self.photo_image = ImageTk.PhotoImage(original_image)
            
            # 4. Exibe a imagem no centro do canvas
            x_center = canvas_width // 2
            y_center = canvas_height // 2
            
            self.image_item_id = self.canvas.create_image(
                x_center, y_center, 
                image=self.photo_image, 
                anchor=tk.CENTER
            )
            
            print(f"Imagem carregada no canvas a partir de {image_path}")
            
        except FileNotFoundError:
            print(f"ERRO: Arquivo de imagem não encontrado em {image_path}")
        except Exception as e:
            print(f"ERRO ao carregar imagem no canvas: {e}")
