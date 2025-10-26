import socket
import time
from root.Comunicação import mensagens
import sys
import threading
import tkinter as tk
import queue

from root.Imagens import drawing_app
from root.Imagens import drawing_tools
from root.Imagens import chat_widget

# define a porta, o IP e a tupla com o endereço do servidor
PORT = 5050
SERVER = "192.168.15.55"
ADDR = (SERVER, PORT)

# define a categoria do socket como IPv4 e o métdo dele
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conecta ao servidor
cliente.connect(ADDR)

#variável global que indica se o cliente está conectado ou não
cliente_conectado = True
recebendo_imagem = False
recebendo_adivinhacao = False
RECEIVED_IMG_PATH = "received_drawing.png"

# fila para comunicação entre threads
gui_queue = queue.Queue()

# avisa o servidor que o cliente está conectado
def cliente_vivo():
    mensagens.enviar(cliente, mensagens.ALIVE_MESSAGE)

# executa funções a cada segundo
def timer():
    tempo = time.time()
    while True:
        # verifica se um segundo decorreu ou não
        tempo_atual = time.time()
        if tempo_atual - tempo > 1:
            tempo = tempo_atual
            cliente_vivo()
            # faz a thread dormir para não sobrecarregar o processador
            time.sleep(0.1)

def receber_e_salvar_imagem():
    print("Recebendo imagem do servidor...")
    try:
        image_bytes = mensagens.receber_imagem(cliente)
        if image_bytes:
            with open(RECEIVED_IMG_PATH, "wb") as f:
                f.write(image_bytes)
            gui_queue.put({"type": "IMAGE_RECEIVED", "path": RECEIVED_IMG_PATH})
            print(f"Imagem recebida e salva em {RECEIVED_IMG_PATH}")
            # adicionar a lógica para exibir a imagem na GUI
            # ou notificar o cliente que a imagem está pronta para ser adivinhada.
            return True
        else:
            print("Falha ao receber bytes da imagem.")
            return False
    except Exception as e:
        print(f"Erro ao salvar a imagem recebida: {e}")
        return False

def listen_for_server():
    """Loop principal para escutar o servidor."""
    global cliente_conectado
    receiving_image = False

    while True:
        if receiving_image:
            receber_e_salvar_imagem(cliente)
        else:
            msg = mensagens.receber(cliente)
            match msg:
                case mensagens.PARTIDA_INICIADA:
                    print("Partida iniciada")

                case mensagens.PARTIDA_ENCERRADA:
                    print("A partida foi encerrada")

                case mensagens.ESPERANDO_IMAGEM:
                    print("Servidor está pedindo que uma imagem seja enviada")
                    continue

                case mensagens.ESPERANDO_ADIVINHACAO:
                    print("Servidor está pedindo que uma adivinhação seja enviada")

                case mensagens.ENVIANDO_IMAGEM:
                    print("Servidor está mandando uma mensagem")

                case mensagens.ENVIANDO_ADIVINHACAO:
                    print("Servidor está enviando uma adivinhação")


    cliente.close()
    cliente_conectado = False

IS_GUESSER = False
# para alternação entre o modo desengista e adivinhador
if len(sys.argv) > 1 and sys.argv[1].lower == '--guesser':
    IS_GUESSER = True
    print("Modo: ADIVINHADOR (Guesser)")
else:
    print("Modo: DESENHISTA (Drawer)")

root = tk.Tk()
app = drawing_app.DrawingApp(root, cliente, mensagens, gui_queue)

if IS_GUESSER:
    app.set_guesser_mode()

# iniciar mecanismo de polling da GUI
app.check_gui_queue()

threading.Thread(target=listen_for_server, args=(cliente,)).start()

threading.Thread(target=cliente_vivo()).start()

# iniciar o loop principal da GUI
root.mainloop()


