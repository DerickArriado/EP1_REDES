import socket
import threading
import time
import sys
import cliente_servidor
from root.Comunicação import mensagens


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# listas de clientes conectados no servidor
clientes_conectados = []
# lista de clientes prontos para começar uma partida
clientes_prontos = []
# lista de clientes numa partida em andamento
clientes_em_partida = []

# retira o cliente de todas as listas e fecha a conexão
def desconectar_cliente(cliente):
    if cliente in clientes_conectados:
        clientes_conectados.remove(cliente)
    if cliente in clientes_prontos:
        clientes_prontos.remove(cliente)
    if cliente in clientes_em_partida:
        clientes_em_partida.remove(cliente)
    cliente.fechar_conexao()

def buscar_partida():
    # verifica se há pelo menos 2 clientes prontos
    if len(clientes_prontos) > 1:
        # seleciona os jogadores
        primeiro_cliente = clientes_prontos[0]
        segundo_cliente = clientes_prontos[1]
        # avisa que a partida será iniciada
        primeiro_cliente.partida_iniciada()
        segundo_cliente.partida_iniciada()
        # remove eles da lista de clientes prontos
        clientes_prontos.remove(primeiro_cliente)
        clientes_prontos.remove(segundo_cliente)
        # adiciona eles na lista de clientes em partida
        clientes_em_partida.append(primeiro_cliente)
        clientes_em_partida.append(segundo_cliente)
        # inicia uma thread para organizar a partida entre os dois clientes
        threading.Thread(target=iniciar_partida, args=(primeiro_cliente, segundo_cliente)).start()

def encerrar_partida(primeiro_cliente, segundo_cliente):
    # remove os clientes da lista de clientes que estão em uma partida
    if primeiro_cliente in clientes_conectados:
        clientes_em_partida.remove(primeiro_cliente)
        primeiro_cliente.partida_encerrada()
    if segundo_cliente in clientes_conectados:
        clientes_em_partida.remove(segundo_cliente)
        segundo_cliente.partida_encerrada()

def iniciar_partida(primeiro_cliente, segundo_cliente):
    pontos_primeiro = 0
    pontos_segundo = 0
    etapa = 0
    partida_em_progresso = True
    while partida_em_progresso:
        # verifica se os dois clientes estão conectados
        if primeiro_cliente not in clientes_em_partida or segundo_cliente not in clientes_em_partida:
            partida_em_progresso = False
            print(f"\nPartida encerrada| {primeiro_cliente.get_addr()} ou {segundo_cliente.get_addr()} se desconectou")
        else:
            match etapa:
                # as etapas a seguir estão suscetíveis à race condition
                case 4:
                    if pontos_primeiro > pontos_segundo:
                        print(f"\n{primeiro_cliente.get_addr()} ganhou!")
                    elif pontos_segundo > pontos_primeiro:
                        print(f"\n{segundo_cliente.get_addr()} ganhou!")
                    else:
                        print("\nEmpate")
                    partida_em_progresso = False
                case 0:
                    if primeiro_cliente.get_imagem():
                        etapa = 1
                        segundo_cliente.enviar_texto(mensagens.ENVIANDO_IMAGEM)
                        segundo_cliente.enviar_imagem(primeiro_cliente.get_imagem())
                    elif not primeiro_cliente.get_esperando_imagem():
                        primeiro_cliente.pedir_imagem()
                case 1:
                    if segundo_cliente.get_adivinhacao():
                        pontos_segundo += adivinhar(primeiro_cliente, segundo_cliente.get_adivinhacao())
                        etapa = 2
                        primeiro_cliente.deletar_imagem()
                        segundo_cliente.deletar_adivinhacao()
                        print(f"\nPontos de {segundo_cliente.get_addr()}: {pontos_segundo}")
                    elif not segundo_cliente.get_esperando_adivinhacao():
                        segundo_cliente.pedir_adivinhacao()
                case 2:
                    if segundo_cliente.get_imagem():
                        etapa = 3
                    elif not segundo_cliente.get_esperando_imagem():
                        segundo_cliente.pedir_imagem()
                case 3:
                    if primeiro_cliente.get_adivinhacao():
                        pontos_primeiro += adivinhar(segundo_cliente, primeiro_cliente.get_adivinhacao())
                        etapa = 4
                        segundo_cliente.deletar_imagem()
                        primeiro_cliente.deletar_adivinhacao()
                        print(f"\nPontos de {primeiro_cliente.get_addr()}: {pontos_primeiro}")
                    elif not primeiro_cliente.get_esperando_adivinhacao():
                        primeiro_cliente.pedir_adivinhacao()
    # avisa os clientes que a partida foi encerrada
    encerrar_partida(primeiro_cliente, segundo_cliente)

def adivinhar(verificador, adivinhacao):
    etapa = 0
    partida_em_progresso = True
    while partida_em_progresso:
        match etapa:
            case 0:
                if verificador.esperando_adivinhacao():
                    verificador.enviar_adivinhacao(adivinhacao)
                    verificador.set_esperando_veredito(True)
                    etapa = 1
                if not verificador.esperando_adivinhacao():
                    verificador.enviar_texto(mensagens.ENVIANDO_ADIVINHACAO)
            case 1:
                if not verificador.get_esperando_veredito():
                    if verificador.get_veredito():
                        return 1
                    return 0
    return None


def cliente_vivo(cliente, tempo):
    tempo_atual = time.time()
    if tempo_atual - tempo > 1:
        cliente.cliente_vivo()
        return tempo_atual
    return tempo

def handle_client(cliente):
    conectado = True
    tempo = time.time()
    while conectado:
        if not cliente.get_esperando_adivinhacao() and not cliente.get_esperando_imagem():
            tempo = cliente_vivo(cliente, tempo)
        if not cliente.get_conectado():
            desconectar_cliente(cliente)
            conectado = False
        else:
            msg = cliente.receber_texto()
            match msg:
                case mensagens.ALIVE_MESSAGE:
                    cliente.set_vivo(5)

                case mensagens.DISCONNECT_MESSAGE:
                    desconectar_cliente(cliente)
                    cliente.set_conectado(False)
                    conectado = False

                case mensagens.PRONTO_PARA_JOGAR:
                    clientes_prontos.append(cliente)

                case mensagens.ENVIANDO_IMAGEM:
                    img_bytes = mensagens.receber_imagem(cliente.conn)
                    if img_bytes:
                        cliente.salvar_imagem(img_bytes)

                case mensagens.ENVIANDO_ADIVINHACAO:
                    adv = mensagens.receber(cliente.conn)
                    if adv:
                        cliente.salvar_adivinhacao(adv)

                case mensagens.ESPERANDO_IMAGEM:
                    cliente.set_esperando_imagem(True)

                case mensagens.ESPERANDO_ADIVINHACAO:
                    cliente.set_esperando_adivinhacao(True)

                case mensagens.ADIVINHACAO_CORRETA:
                    cliente.set_veredito(True)
                    cliente.set_esperando_veredito(False)

                case mensagens.ADIVINHACAO_ERRADA:
                    cliente.set_veredito(False)
                    cliente.set_esperando_veredito(False)

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
        threading.Thread(target=handle_client, args=(cliente,)).start()

# imprime informações relevantes do servidor
def imprime_status():
    # escreve o número de conexões ativas e o horário em que a verificação foi feita
    status_msg = (f"|Conexões Ativas|: {len(clientes_conectados)} "
                  f"|Partidas em andamento|: {len(clientes_em_partida)/2} "
                  f"|Última verificação|: {time.strftime('%H:%M:%S')}")
    # sobrescreve o texto antigo com os valores atuais
    sys.stdout.write('\r' + status_msg + '' * 10)
    sys.stdout.flush()

# executa funções a cada segundo
def timer():
    tempo = time.time()
    while True:
        # verifica se um segundo decorreu ou não
        tempo_atual = time.time()
        if tempo_atual - tempo > 1:
            tempo = tempo_atual
            imprime_status()
            buscar_partida()
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




