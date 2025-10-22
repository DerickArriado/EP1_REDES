import socket
import time
import mensagens
import sys
import os 
import threading
import tkinter as tk
import queue
import drawing_app

# define a porta, o IP e a tupla com o endereço do servidor
PORT = 5050
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

# define a categoria do socket como IPv4 e o métdo dele
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conecta ao servidor
client.connect(ADDR)

client_connected = True

mensagens_handler = mensagens.Mensagens()

RECEIVED_IMG_PATH = "received_drawing.png"

# fila para comunicação entre threads
gui_queue = queue.Queue()

def keep_alive():
    global client_connected
    tempo = time.time()

    while client_connected:
        tempoAtual = time.time()
        if tempoAtual - tempo > 2:
            try:
                mensagens_handler.enviar(client, mensagens_handler.ALIVE_MESSAGE)
                tempo = tempoAtual
            except (socket.error, ConnectionResetError, OSError):
                # se envio falhar significa q a outra thread ainda não atualizou, e sai
                client_connected = False
                print("Keep-alive falhou, encerrando thread.")
                break
            

def receber_e_salvar_imagem(client_socket):
    print("Recebendo imagem do servidor...")
    try:
        image_bytes = mensagens_handler.receber_bytes(client_socket)
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

def listen_for_server(client_socket):
    """Loop principal para escutar o servidor."""
    global client_connected
    receiving_image = False
    
    while True:
        if receiving_image:
            # MODO BINÁRIO: Receber a imagem e salvar.
            if receber_e_salvar_imagem(client_socket):
                # Se o recebimento binário for bem-sucedido, espere pelo !IMAGE_END (texto)
                pass # A próxima iteração lerá o !IMAGE_END
            receiving_image = False # Volta para modo de texto
            
        else:
            # MODO TEXTO: Receber comandos ou mensagens
            msg = mensagens_handler.receber(client_socket)
            
            if msg == mensagens_handler.IMAGE_START_MESSAGE:
                print("Servidor sinalizou início de imagem. Preparando para receber binário.")
                receiving_image = True
                continue
                
            elif msg == mensagens_handler.IMAGE_END_MESSAGE:
                print("Fim da transmissão de imagem.")
                # A imagem já foi salva na etapa anterior.
                continue

            elif msg == mensagens_handler.ALIVE_MESSAGE:
                # Mensagem de keep-alive do servidor
                continue
            
            elif msg == mensagens_handler.DISCONNECT_MESSAGE:
                print("Servidor desconectou.")
                break
                
            elif msg:
                print(f"Mensagem do servidor: {msg}")

            else:
                # Conexão perdida
                print("Conexão com servidor perdida.")
                break
    
    client_socket.close()
    client_connected = False

IS_GUESSER = False
# para alternação entre o modo desengista e adivinhador
if len(sys.argv) > 1 and sys.argv[1].lower == '--guesser':
    IS_GUESSER = True
    print("Modo: ADIVINHADOR (Guesser)")
else:
    print("Modo: DESENHISTA (Drawer)")

root = tk.Tk()
app = drawing_app.DrawingApp(root, client, mensagens_handler, gui_queue)

if IS_GUESSER:
    app.set_guesser_mode()

# iniciar mecanismo de polling da GUI
app.check_gui_queue()


threading.Thread(target=listen_for_server, args=(client,)).start()

threading.Thread(target=keep_alive).start()

# iniciar o loop principal da GUI
root.mainloop()


