import mensagens

class ClienteServidor:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.vivo = 5
        self.esperando_imagem = False
        self.img = b""
        self.adivinhacao = ""
        self.pontos = 0

    def fechar_conexao(self):
        self.conn.close()

    def cliente_vivo(self):
        self.vivo -= 1
        if self.vivo == 0:
            print(f"|Cliente Morreu| {self.addr} desconectado")
            return False
        return True

    def servidor_vivo(self):
        mensagens.enviar_texto(self.conn, mensagens.ALIVE_MESSAGE)

    def partida_iniciada(self):
        mensagens.enviar_texto(self.conn, mensagens.PARTIDA_INICIADA)

    def partida_em_andamento(self):
        mensagens.enviar_texto(self.conn, mensagens.PARTIDA_EM_ANDAMENTO)

    def partida_encerrada(self):
        mensagens.enviar_texto(self.conn, mensagens.PARTIDA_ENCERRADA)

    def pedir_imagem(self):
        mensagens.enviar_texto(self.conn, mensagens.ESPERANDO_IMAGEM)
        self.esperando_imagem = True

    def receber_texto(self):
        msg = mensagens.receber(self.conn)
        if msg:
            print(f"|{self.addr()}: {msg}|")
            return msg
        print("|Erro ao receber mensagem|")
        return None

    def receber_imagem(self):
        self.img = mensagens.receber_imagem(self.conn)
        self.esperando_imagem = False
        if self.img:
            print(f"|{self.addr}| Recebido {len(self.img)} bytes de imagem.")

    def esperando_imagem(self):
        return self.esperando_imagem

    def possui_imagem(self):
        if self.img:
            return True
        return False

    def deletar_imagem(self):
        self.img = None

    def set_vivo(self, vivo):
        self.vivo = vivo

    def get_addr(self):
        return self.addr

    def get_img(self):
        return self.img
