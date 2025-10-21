# tamanho máximo de uma mensagem
HEADER = 64
# formato em que a mensagem deve ser decifrada e codificada
FORMAT = 'utf-8'
# mensagens padrão

class Mensagens:
    DISCONNECT_MESSAGE = "!DISCONNECT"
    ALIVE_MESSAGE = "!ALIVE"

    def __init__(self):
        pass

    def enviar(self, conn, msg):
        # codifica a mensagem para poder ser enviada em bytes
        msg = msg.encode(FORMAT)
        # calcula o tamanho da mensagem em bytes
        tamanho_msg = len(msg)
        # codifica o tamanho da mensagem
        tamanho_msg = str(tamanho_msg).encode(FORMAT)
        # faz com que o tamanho da mensagem seja igual ao tamanho de HEADER em bytes
        tamanho_msg += b' ' * (HEADER - len(tamanho_msg))
        # envia o tamanho da mensagem
        conn.send(tamanho_msg)
        # envia a mensagem
        conn.send(msg)

    def receber(self, conn):
        # recebe e decifra a mensagem de tamanho no formato escolhido
        tamanho_msg = conn.recv(HEADER).decode(FORMAT)
        # verifica se o tamanho foi recebido
        if tamanho_msg:
            # converte o tamanho para bytes
            tamanho_msg = int(tamanho_msg)
            # recebe a mensagem
            msg = conn.recv(tamanho_msg).decode(FORMAT)
            # retorna a mensagem
            return msg
        # retorna None se o tamanho não foi recebido
        return None