import socket
import time
import mensagens

# define a porta, o IP e a tupla com o endereço do servidor
PORT = 5050
SERVER = " "
ADDR = (SERVER, PORT)

# define a categoria do socket como IPv4 e o métdo dele
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conecta ao servidor
client.connect(ADDR)

mensagens = mensagens.Mensagens()

def keep_alive():
    tempo = time.time()
    connected = True
    while connected:
        tempoAtual = time.time()
        if tempoAtual - tempo > 2:
            mensagens.enviar(client, mensagens.ALIVE_MESSAGE)


mensagens.enviar(client, "AAAAAAAAAAAAAA")
mensagens.enviar(client, "IIIIIIIIIIIIII")
mensagens.enviar(client, "OOOOOOOOOOOOOO")

