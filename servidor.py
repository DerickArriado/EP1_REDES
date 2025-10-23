import socket
import threading
import time
import mensagens
import sys

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# nova instância do sistema que controla o envio de mensagens
mensagens = mensagens.Mensagens()
# lista que contém todos os clientes
clientes = []

def handle_client(conn, addr):
    print(f"|Nova Conexão| {addr} conectado")
    vivo = 5
    tempo = time.time()
    connected = True

    receiving_image = False

    while connected:

        tempoAtual = time.time()
        if tempoAtual - tempo > 1:
            tempo = tempoAtual
            vivo -= 1
        if vivo == 0:
            connected = False
            print(f"|Cliente Morreu| {addr} desconectado")

        if receiving_image:
            # modo byte: tenta receber a imagem
            img_bytes = mensagens.receber_bytes(conn)
            if  img_bytes is not None:
                print(f"|{addr}| Recebido {len(img_bytes)} bytes de imagem.")
                retransmitir_img(conn, img_bytes)
                receiving_image = False #espera pelo !IMAGE_END
            else:
                receiving_image = False
        else:
            # modo texto: tenta receber mensagem de texto
            msg = mensagens.receber(conn)

            if msg is None:
                connected = False
                break

            if msg:
                if msg == mensagens.ALIVE_MESSAGE:
                    vivo = 5
                    continue

                if msg == mensagens.DISCONNECT_MESSAGE:
                    connected = False
                    break

                if msg == mensagens.IMAGE_START_MESSAGE:
                    print(f"|{addr}| Sinal de início de imagem recebido. Mudando para binário.")
                    receiving_image = True
                    continue
                
                if msg == mensagens.IMAGE_END_MESSAGE:
                    # Isso deve ser recebido logo após os bytes binários
                    print(f"|{addr}| Fim de transmissão de imagem.")
                    # A retransmissão já foi feita quando receiving_image era True
                    continue

                print(f"|{addr}: {msg}|")
                # Se não for imagem, retransmita o texto (se for um jogo multiplayer)
                # retransmitir_mensagem(conn, msg)

    # fecha a conexão
    conn.close()
    if conn in clientes:
        clientes.remove(conn)

# função que distribui a imagem para o cliente que deve adivinhar
def retransmitir_img(sender_conn, image_bytes):
    # retransmite para todos, menos ao remetente
    for cliente in clientes:
        if cliente != sender_conn:
            try:
                # avisa que uma imagem está chegando 
                mensagens.enviar(cliente, mensagens.IMAGE_START_MESSAGE) 
                # envia os bytes da imagem
                mensagens.enviar_bytes(cliente, image_bytes)
                # avisa o fi
                mensagens.enviar(cliente, mensagens.IMAGE_END_MESSAGE)
                print(f"Imagem retransmitida para {cliente.getpeername()}")
            except Exception as e:
                print(f"Erro ao retransmitir imagem: {e}")

# busca continuamente por possíveis tentativas de conexões de clientes
def busca_clientes():
    while True:
        # aceita pedidos de conexão com o servidor
        conn, addr = server.accept()
        # coloca o tempo máximo de timeout do socket como 5 segundos
        conn.settimeout(5)
        # adiciona o cliente na lista de clientes
        clientes.append(conn)
        # inicia uma thread para executar as funções relacionadas a cada cliente
        threading.Thread(target=handle_client, args=(conn, addr)).start()

# envia uma confirmação de que o servidor está a funcionar para todos os clientes
def server_is_alive():
    for cliente in clientes[:]:  # cópia da lista para evitar problemas ao remover
        try:
            mensagens.enviar(cliente, mensagens.ALIVE_MESSAGE)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

# imprime informações relevantes do servidor
def status():
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
        tempoAtual = time.time()
        if tempoAtual - tempo > 1:
            tempo = tempoAtual
            server_is_alive()
            status()
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




