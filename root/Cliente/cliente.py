import socket
import time
from root.Comunicação import mensagens
from root.Servidor import cliente_servidor
import sys
import threading
import tkinter as tk
import queue
from root.Imagens import drawing_app

# define a porta, o IP e a tupla com o endereço do servidor
PORT = 5050
SERVER = "192.168.15.24"
ADDR = (SERVER, PORT)

# define a categoria do socket como IPv4 e o métdo dele
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conecta ao servidor
socket_cliente.connect(ADDR)

# cria uma instância de cliente_servidor
cliente = cliente_servidor.ClienteServidor(socket_cliente, ADDR)

RECEIVED_IMG_PATH = "received_drawing.png"

# fila para comunicação entre threads
gui_queue = queue.Queue()

# avisa o servidor que o cliente está conectado
def estou_vivo():
    tempo = time.time()
    while cliente.get_conectado():
        # verifica se um segundo decorreu ou não
        tempo_atual = time.time()
        if tempo_atual - tempo > 1:
            tempo = tempo_atual
            cliente.enviar_texto(mensagens.ALIVE_MESSAGE)
            # faz a thread dormir para não sobrecarregar o processador
            time.sleep(0.1)

def input_usuario():
    resposta = input("Gostaria de entrar em uma partida? (S/N)\n")
    if resposta.upper() == "S":
        print("|Esperando partida começar|")
        cliente.set_esperando_partida(True)
        cliente.cliente_pronto()
    elif resposta.upper() == "N":
        if input("Gostaria de sair? (S/N)\n").upper() == "S":
            cliente.desconectar()

def mensagens_servidor():
    while cliente.get_conectado():
        if not cliente.get_conectado():
            pass
        elif not cliente.get_esperando_partida() and not cliente.get_em_partida():
            input_usuario()
        else:
            msg = mensagens.receber(socket_cliente)
            match msg:
                case mensagens.PARTIDA_INICIADA:
                    cliente.set_em_partida(True)
                    cliente.set_esperando_partida(False)

                case mensagens.PARTIDA_ENCERRADA:
                    cliente.set_em_partida(False)

                case mensagens.ESPERANDO_IMAGEM:
                    # Servidor está esperando que uma imagem seja enviada
                    ferramenta_desenho()

                case mensagens.ESPERANDO_ADIVINHACAO:
                    # O servidor está esperando que uma adivinhação seja enviada
                    cliente.enviar_adivinhacao(AAAAAAAAAAAAAAA)

                case mensagens.ENVIANDO_IMAGEM:
                    # O servidor está mandando uma imagem
                    cliente.salvar_imagem()

                case mensagens.ENVIANDO_ADIVINHACAO:
                    # O servidor está enviando uma adivinhação
                    cliente.salvar_adivinhacao()

def ferramenta_desenho():
    IS_GUESSER = False
    # para alternação entre o modo desenhista e adivinhador
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--guesser':
        IS_GUESSER = True
        print("Modo: ADIVINHADOR (Guesser)")
    else:
        print("Modo: DESENHISTA (Drawer)")

    root = tk.Tk()
    app = drawing_app.DrawingApp(root, socket_cliente, mensagens, gui_queue)

    if IS_GUESSER:
        app.set_guesser_mode()

    # iniciar mecanismo de polling da GUI
    app.check_gui_queue()

    # iniciar o loop principal da GUI
    root.mainloop()

def criar_threads():
    threading.Thread(target=mensagens_servidor).start()
    threading.Thread(target=estou_vivo).start()

criar_threads()


