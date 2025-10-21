import socket
import threading
import time
import mensagens

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

mensagens = mensagens.Mensagens()

clientes = []

def handle_client(conn, addr):
    print(f"|Nova Conexão| {addr} conectado")
    vivo = 5
    tempo = time.time()
    connected = True
    while connected:
        tempoAtual = time.time()
        if tempoAtual - tempo > 1:
            tempo = tempoAtual
            vivo -= 1
        if vivo == 0:
            connected = False
            print(f"|Cliente Morreu| {addr} desconectado")

        msg = mensagens.receber(conn)
        if msg:
            if msg == mensagens.ALIVE_MESSAGE:
                vivo = 5

            if msg == mensagens.DISCONNECT_MESSAGE:
                connected = False

            print(f"|{addr}: {msg}|")

    # fecha a conexão
    conn.close()
    clientes.remove(conn)


def busca_clientes():
    while True:
        conn, addr = server.accept()
        conn.settimeout(5)
        clientes.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def server_is_alive():
    for cliente in clientes:
       mensagens.enviar(cliente, mensagens.ALIVE_MESSAGE)

def timer():
    tempo = time.time()
    while True:
        tempoAtual = time.time()
        if tempoAtual - tempo > 1:
            tempo = tempoAtual
            server_is_alive()
            print(f"|Conexões Ativas|: {threading.active_count() - 2}")

def criar_threads():
    threading.Thread(target=timer).start()
    threading.Thread(target=busca_clientes).start()

def start():
    server.listen()
    criar_threads()
    tempo = time.time()
    print(f"|Servidor esperando Mensagens em: {SERVER}|")

print("---Iniciando o servidor---")
start()




