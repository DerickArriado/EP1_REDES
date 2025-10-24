import mensagens

# instância do sistema que controla o envio de mensagens
mensagens = mensagens.Mensagens()

class ClienteServidor:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.vivo = 5
        self.recebendo_imagem = False

    def fechar_conexao(self):
        self.conn.close()

    def cliente_vivo(self):
        self.vivo -= 1
        if self.vivo == 0:
            print(f"|Cliente Morreu| {self.addr} desconectado")
            return False
        return True

    def servidor_vivo(self):
        mensagens.enviar(self.conn, mensagens.ALIVE_MESSAGE)

    def partida_iniciada(self):
        mensagens.enviar(self.conn, mensagens.PARTIDA_INICIADA)

    def partida_encerrada(self):
        mensagens.enviar(self.conn, mensagens.PARTIDA_ENCERRADA)

    def receber_texto(self):
        msg = mensagens.receber(self.conn)
        if msg:
            print(f"|{self.addr()}: {msg}|")
            return msg
        print("|Erro ao receber mensagem|")
        return None

    def receber_imagem(self):
        mensagens.enviar(self.conn, mensagens.ESPERANDO_IMAGEM)
        img_bytes = mensagens.receber_bytes(self.conn)
        if img_bytes:
            print(f"|{self.addr}| Recebido {len(img_bytes)} bytes de imagem.")
            return img_bytes
        print("Erro ao receber imagem.")
        return None

    def set_vivo(self, vivo):
        self.vivo = vivo

    def get_addr(self):
        return self.addr
