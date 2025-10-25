class DrawingTools:
    def __init__(self, canvas):
        self.canvas = canvas
        self.mode = "draw"
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def set_mode(self, mode):
        self.mode = mode

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event, color, thickness):
        if self.drawing:
            if self.mode == "erase":
                draw_color = "white"
                draw_thickness = 15
            else:
                try:
                    draw_color = color
                    draw_thickness = thickness
                except Exception:
                    draw_color = "black"
                    draw_thickness = 2
            
            x, y = event.x, event.y
            if self.last_x is not None and self.last_y is not None:
                self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    fill=draw_color, width=draw_thickness, capstyle="round"
                )
            self.last_x = x
            self.last_y = y

    def stop_drawing(self):
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")
