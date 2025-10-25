# tamanho máximo de uma mensagem
HEADER = 64
# formato em que a mensagem do tipo TEXTO deve ser decifrada e codificada
FORMAT = 'utf-8'

# mensagens padrão
DISCONNECT_MESSAGE = "!DISCONNECT"
ALIVE_MESSAGE = "!ALIVE"
PRONTO_PARA_JOGAR = "!PRONTO_PARA_JOGAR"
PARTIDA_INICIADA = "!PARTIDA_INICIADA"
PARTIDA_ENCERRADA = "!PARTIDA_ENCERRADA"
ESPERANDO_VEREDITO = "!ESPERANDO_VEREDITO"
ESPERANDO_IMAGEM = "!ESPERANDO_IMAGEM"
ESPERANDO_ADIVINHACAO = "!ESPERANDO_ADIVINHAÇÃO"
ENVIANDO_IMAGEM = "!ENVIANDO_IMAGEM"
ENVIANDO_ADIVINHACAO = "!ENVIANDO_ADIVINHAÇÃO"
ADIVINHACAO_CORRETA = "!ADIVINHAÇÃO_CORRETA"
ADIVINHACAO_ERRADA = "!ADIVINHAÇÃO_ERRADA"


def enviar(conn, msg):
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
    return msg

def enviar_texto(conn, msg):
    # envia a mensagem
    conn.send(enviar(conn, msg))

def enviar_imagem(conn, msg):
    # envia todos os bytes da imagem
    conn.sendall(enviar(conn, msg))

def receber(conn):
    try:
        # recebe e decifra a mensagem de tamanho no formato escolhido
        tamanho_msg = conn.recv(HEADER).decode(FORMAT)
        # converte o tamanho para int
        tamanho_msg = int(tamanho_msg)
        #verifica se a mensagem está vazia
        if not tamanho_msg:
            return None
        # recebe a mensagem
        msg = conn.recv(tamanho_msg).decode(FORMAT)
        # retorna a mensagem
        return msg

    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        return None

def receber_imagem(conn):
    try:
        # recebe e decifra a mensagem de tamanho no formato escolhido
        tamanho_msg = conn.recv(HEADER).decode(FORMAT)
        # converte o tamanho para int
        tamanho_dados = int(tamanho_msg)
        # verifica se a mensagem está vazia
        if not tamanho_msg:
            return None

        bytes_recebidos = b''
        bytes_pendentes = tamanho_dados

        # recebe os dados em blocos até ter o total
        while bytes_pendentes > 0:
            # recebe em blocos de 4096 ou menos
            chunk = conn.recv(min(4096, bytes_pendentes))
            # verifica se houve um erro na transmissão da imagem
            if not chunk:
                return None
            bytes_recebidos += chunk
            bytes_pendentes -= len(chunk)

        return bytes_recebidos

    except Exception as e:
        print(f"Erro ao receber imagem: {e}")
        return None
