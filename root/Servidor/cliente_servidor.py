from root.Comunicação import mensagens

class ClienteServidor:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.vivo = 5
        self.esperando_veredito = False
        self.esperando_imagem = False
        self.esperando_adivinhacao = False
        self.veredito = False
        self.imagem = b""
        self.adivinhacao = ""
        self.conectado = True


    def fechar_conexao(self):
        self.conn.close()

    def cliente_vivo(self):
        self.vivo -= 1
        if self.vivo == 0:
            print(f"\n|Cliente Morreu| {self.addr} desconectado")
            self.conectado = False

    # avisa o cliente que a partida foi iniciada
    def partida_iniciada(self):
        mensagens.enviar_texto(self.conn, mensagens.PARTIDA_INICIADA)

    # avisa o cliente que a partida foi encerrada
    def partida_encerrada(self):
        mensagens.enviar_texto(self.conn, mensagens.PARTIDA_ENCERRADA)

    # avisa o cliente que o servidor precisa que ele envie uma imagem
    def pedir_imagem(self):
        mensagens.enviar_texto(self.conn, mensagens.ESPERANDO_IMAGEM)
        self.esperando_imagem = True

    # avisa o cliente que o servidor precisa que ele envie uma adivinhação
    def pedir_adivinhacao(self):
        mensagens.enviar_texto(self.conn, mensagens.ESPERANDO_ADIVINHACAO)
        self.esperando_adivinhacao = True

    # retorna uma mensagem do cliente
    def receber_texto(self):
        msg = mensagens.receber(self.conn)
        if msg:
            print(f"\n|{self.addr}: {msg}|")
            return msg
        return None

    # recebe uma imagem do cliente e salva na variável img
    def salvar_imagem(self):
        self.imagem = mensagens.receber_imagem(self.conn)
        self.esperando_imagem = False
        if self.imagem:
            print(f"\n|{self.addr}| Recebido {len(self.imagem)} bytes de imagem.")

    # recebe uma adivinhação do cliente e salva na variável adivinhação
    def salvar_adivinhacao(self):
        adivinhacao = self.receber_texto()
        self.esperando_adivinhacao = False
        if self.adivinhacao is not None:
            self.adivinhacao = adivinhacao
            print(f"\n|Adivinhacao recebida| de {self.addr}")
        else:
            print(f"\n|Erro ao receber adivinhação| de {self.addr}")

    def enviar_texto(self, msg):
        mensagens.enviar_texto(self.conn, msg)

    # envia uma imagem para o cliente
    def enviar_imagem(self, img):
        mensagens.enviar_imagem(self.conn, img)

    # envia uma adivinhação para o cliente
    def enviar_adivinhacao(self, adivinhacao):
        mensagens.enviar_texto(self.conn, adivinhacao)

    def deletar_imagem(self):
        self.imagem = None

    def deletar_adivinhacao(self):
        self.adivinhacao = ""

    def set_vivo(self, vivo):
        self.vivo = vivo

    def set_veredito(self, veredito):
        self.veredito = veredito

    def set_esperando_veredito(self, esperando_veredito):
        self.esperando_veredito = esperando_veredito

    def set_esperando_imagem(self, esperando_imagem):
        self.esperando_imagem = esperando_imagem

    def set_esperando_adivinhacao(self, esperando_adivinhacao):
        self.esperando_adivinhacao = esperando_adivinhacao

    def set_conectado(self,conectado):
        self.conectado = conectado

    def get_addr(self):
        return self.addr

    def get_imagem(self):
        return self.imagem

    def get_adivinhacao(self):
        return self.adivinhacao

    def get_veredito(self):
        return self.veredito

    def get_esperando_veredito(self):
        return self.esperando_veredito

    def get_esperando_imagem(self):
        return self.esperando_imagem

    def get_esperando_adivinhacao(self):
        return self.esperando_adivinhacao

    def get_conectado(self):
        return self.conectado
