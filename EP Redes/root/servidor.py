import socket
import threading

# define a porta, o IP e o endereço do servidor
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) # tupla que contém a porta e o IP do servidor

# define o tamanho do cabeçalho de cada mensagem em bytes
# antes de cada mensagem ser enviada, enviamos outra mensagem que descreve
# o tamanho dela em bytes, e essa mensagem tem o tamanho máximo HEADER
HEADER = 64

#define o formato em que as mensagens serão decifrada
FORMAT = 'utf-8'

# Mensagem que simboliza um pedido de desconexão
DISCONNECT_MESSAGE = "!DISCONNECT"

# define a categoria do socket como IPv4 e o métdo dele
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conecta o socket com a tupla de Porta e IP do servidor
# faz com que todas as máquinas tentando conectar nesse tupla sejam encaminhadas para esse socket
server.bind(ADDR)

# address é uma tupla que contém o endereço IP e a porta de um cliente
# conn é um objeto que permite a comunicação com aquele endereço em específico
# lida com cada conexão individual entre cliente e servidor
# cada cliente tem uma thread separada onde a função handle_client() ocorre
def handle_client(conn, addr):
    print(f"|Nova Conexão|: {addr} conectado")
    connected = True
    while connected:
        # não fazemos nada até receber o tamanho da mensagem do cliente
        # deciframos a mensagem no formato escolhido
        tamanho_msg = conn.recv(HEADER).decode(FORMAT)
        #verifica se uma mensagem foi recebida
        if tamanho_msg:
            tamanho_msg = int(tamanho_msg)

            # recebemos a mensagem do cliente
            msg = conn.recv(tamanho_msg).decode(FORMAT)

            # paramos o loop se a mensagem for um pedido de desconexão
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"|{addr}: {msg}|")

    # fecha a conexão
    conn.close()

# inicializa o socket do servidor

# passa as conexões para handle_client()
def start():
    # permite que ele comece a buscar conexões
    server.listen()
    print(f"|Servidor esperando Mensagens em|: {SERVER}")
    while True:
        conn, addr = server.accept()
        # quando uma nova conexão ocorre,
        # criamos uma nova thread onde passamos a conexão para handle_client()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"|Conexões Ativas|: {threading.active_count() - 1}")

print("---Iniciando o servidor---")
start()




