# save_png.py
from PIL import ImageGrab

def save_canvas_as_png(canvas, file_path):
    """
    Captura a área do canvas como imagem e salva em PNG.
    Usa PIL.ImageGrab para fazer screenshot da região do canvas:contentReference[oaicite:3]{index=3}.
    """
    # Garantir que o canvas esteja atualizado (importante para pegar tamanho correto)
    canvas.update()
    # Coordenadas absolutas da janela do canvas
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    # Define a região para captura (x0, y0, x1, y1)
    bbox = (x, y, x + w, y + h)
    # Captura a tela nessa região
    image = ImageGrab.grab(bbox)
    # Salva como PNG
    image.save(file_path, "PNG")
