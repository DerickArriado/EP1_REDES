import socket

PORT = 5050
# é necessário colocar o IP da máquina em que o servidor está
SERVER = "192.168.15.24"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# o servidor precisa estar ligado
client.connect(ADDR)

def send(msg):
    # codifica a mensagem para poder ser enviada em bytes
    msg = msg.encode(FORMAT)
    tamanho_msg = len(msg)
    send_lenght = str(tamanho_msg).encode(FORMAT)

    # faz com que o tamanho da mensagem seja igual ao tamanho de HEADER em bytes
    send_lenght += b' ' * (HEADER - len(send_lenght))

    # envia o tamanho da mensagem
    client.send(send_lenght)
    # envia a mensagem
    client.send(msg)

send("AAAAAAAAAAAAAA")
send("OOOOOOOOOOOOOOOOO")
send("EEEEEEEEEEEEEE")
send(DISCONNECT_MESSAGE)