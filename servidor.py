import socket
import threading
import time
import sys
import cliente_servidor
import mensagens

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#listas de clientes
clientes_conectados = []
clientes_prontos = []
clientes_jogando = []

def desconectar_cliente(cliente):
    if cliente in clientes_conectados:
        clientes_conectados.remove(cliente)
    if cliente in clientes_prontos:
        clientes_prontos.remove(cliente)
    if cliente in clientes_jogando:
        clientes_jogando.remove(cliente)
    cliente.fechar_conexao()

def buscar_partida():
    # verifica se há pelo menos 2 clientes prontos
    if len(clientes_prontos) > 1:
        primeiro_cliente = clientes_prontos[0]
        segundo_cliente = clientes_prontos[1]
        # remove eles da lista de clientes prontos
        clientes_prontos.remove(primeiro_cliente)
        clientes_prontos.remove(segundo_cliente)
        # adiciona eles na lista de clientes em partida
        clientes_jogando.append(primeiro_cliente)
        clientes_jogando.append(segundo_cliente)
        # inicia uma partida com os dois clientes
        iniciar_partida(primeiro_cliente, segundo_cliente)

def encerrar_partida(primeiro_cliente, segundo_cliente):
    # remove os clientes da lista de clientes jogando
    clientes_jogando.remove(primeiro_cliente)
    clientes_jogando.remove(segundo_cliente)
    # adiciona eles na lista de clientes conectados
    clientes_conectados.append(primeiro_cliente)
    clientes_conectados.append(segundo_cliente)
    # avisa os clientes que a partida foi encerrada
    primeiro_cliente.partida_encerrada()
    segundo_cliente.partida_encerrada()

def iniciar_partida(primeiro_cliente, segundo_cliente):
    pontos_primeiro = 0
    pontos_segundo = 0
    partida_em_progresso = True
    while partida_em_progresso:
        # verifica se os dois clientes estão conectados
        if primeiro_cliente not in clientes_jogando or segundo_cliente not in clientes_jogando:
            partida_em_progresso = False
            print(f"|Partida encerrada| {primeiro_cliente.get_addr()} ou {segundo_cliente.get_addr()} se desconectou")

        else:
            # primeiro jogador desenha e o segundo adivinha
            img = desenhar_imagem(primeiro_cliente)
            pontos_primeiro += adivinhar(primeiro_cliente, img)

            print(f"Pontos de {primeiro_cliente.get_addr()}: {pontos_primeiro}")

            # segundo jogador desenha e o primeiro adivinha
            img = desenhar_imagem(segundo_cliente)
            pontos_segundo += adivinhar(segundo_cliente, img)

            print(f"Pontos de {segundo_cliente.get_addr()}: {pontos_segundo}")

            if pontos_primeiro > pontos_segundo:
                print(f"{primeiro_cliente.get_addr()} ganhou!")
                partida_em_progresso = False
            elif pontos_segundo > pontos_primeiro:
                print(f"{segundo_cliente.get_addr()} ganhou!")
                partida_em_progresso = False
            else:
                print("Indo para próxima rodada")

    encerrar_partida(segundo_cliente, primeiro_cliente)

def desenhar_imagem(cliente):
    img = cliente.receber_imagem()
    while img is None:
        img = cliente.receber_imagem()
    return img

def adivinhar(liente, img):
    pass

def handle_client(cliente):
    conectado = True
    while conectado:
        if not cliente.cliente_vivo():
            desconectar_cliente(cliente)
            conectado = False
        else:
            msg = cliente.receber_texto()
            match msg:
                case None:
                    pass

                case mensagens.ALIVE_MESSAGE:
                    cliente.set_vivo(5)

                case mensagens.DISCONNECT_MESSAGE:
                    desconectar_cliente(cliente)
                    conectado = False

                case mensagens.PRONTO_PARA_JOGAR:
                    clientes_prontos.append(cliente)

# busca continuamente por possíveis tentativas de conexões de clientes
def busca_clientes():
    while True:
        # aceita pedidos de conexão com o servidor
        conn, addr = server.accept()
        # coloca o tempo máximo de timeout do socket como 5 segundos
        conn.settimeout(5)
        # cria um cliente
        cliente = cliente_servidor.ClienteServidor(conn, addr)
        # adiciona o cliente na lista de clientes
        clientes_conectados.append(cliente)
        # inicia uma thread para executar as funções relacionadas a cada cliente
        threading.Thread(target=handle_client, args=cliente).start()

# envia uma confirmação de que o servidor está ligado para todos os clientes
def server_is_alive():
    for cliente in clientes_conectados[:]:  # cópia da lista para evitar problemas ao remover
        cliente.servidor_vivo()

# imprime informações relevantes do servidor
def imprime_status():
    # escreve o número de conexões ativas e o horário em que a verificação foi feita
    status_msg = f"|Conexões Ativas|: {threading.active_count() - 3} | Última verificação: {time.strftime('%H:%M:%S')}"
    # sobrescreve o texto antigo com os valores atuais
    sys.stdout.write('\r' + status_msg + ' ' * 10)
    sys.stdout.flush()

# executa funções a cada segundo
def timer():
    tempo = time.time()
    while True:
        # verifica se um segundo decorreu ou não
        tempo_atual = time.time()
        if tempo_atual - tempo > 1:
            tempo = tempo_atual
            server_is_alive()
            imprime_status()
            # faz a thread dormir para não sobrecarregar o processador
            time.sleep(0.1)

# cria as threads do servidor
def criar_threads():
    threading.Thread(target=timer).start()
    threading.Thread(target=busca_clientes).start()

#inicia o servidor
def start():
    # chama funções para que o servidor funcione corretamente
    server.listen()
    criar_threads()
    # imprime o IP do servidor
    print(f"|Servidor esperando Mensagens em: {SERVER}|")

print("---Iniciando o servidor---")
start()




