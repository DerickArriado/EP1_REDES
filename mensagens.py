import socket

# tamanho máximo de uma mensagem
HEADER = 64
# formato em que a mensagem do tipo TEXTO deve ser decifrada e codificada
FORMAT = 'utf-8'

# mensagens padrão
DISCONNECT_MESSAGE = "!DISCONNECT"
ALIVE_MESSAGE = "!ALIVE"
SENDING_IMAGE = "!SENDING_IMAGE"
PRONTO_PARA_JOGAR = "!PRONTO_PARA_JOGAR"
PARTIDA_INICIADA = "!PARTIDA_INICIADA"
PARTIDA_ENCERRADA = "!PARTIDA_ENCERRADA"
ESPERANDO_IMAGEM = "!ESPERANDO_IMAGEM"
ESPERANDO_ADIVINHACAO = "!ESPERANDO_ADIVINHAÇÃO"

class Mensagens:

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
        try:
            # recebe e decifra a mensagem de tamanho no formato escolhido
            tamanho_msg_header = conn.recv(HEADER).decode(FORMAT)
            # verifica se há conteúdo relevante após remover espaços
            if not tamanho_msg_header.strip():
                return None
            # limpa os espaços (essencial!) e converte para inteiro
            tamanho_msg = int(tamanho_msg_header.strip())
            # recebe a mensagem
            msg = conn.recv(tamanho_msg).decode(FORMAT)
            # retorna a mensagem
            return msg
        except (socket.error, ConnectionResetError, OSError) as e: 
            # Erro de conexão (o servidor resetou ou fechou)
            # Imprime apenas o erro do socket para debug, mas retorna None
            print(f"Erro ao receber mensagem de texto: {e}") 
            return None
        except ValueError as e:
            # Erro de formatação do header (dados inválidos)
            print(f"Erro ao receber mensagem de texto: {e}") 
            return None
        except Exception as e:
            # Se houver um erro de conversão (ValueError) ou de socket, retorna None
            print(f"Erro ao receber mensagem de texto: {e}") 
            return None
    
    def enviar_bytes(self, conn, dados_bytes):
        # envia tamanho dos dados binários
        tamanho_dados = len(dados_bytes)
        tamanho_header = str(tamanho_dados).encode(FORMAT)
        tamanho_header += b' ' * (HEADER - len(tamanho_header))
        conn.send(tamanho_header)
        
        # Envia os dados binários brutos
        conn.sendall(dados_bytes)

    def receber_bytes(self, conn):
        # recebe dados binários (bytes) usando o tamanho do header
        try:
            # recebe o header
            tamanho_header = conn.recv(HEADER).decode(FORMAT)
            if not tamanho_header:
                return None

            tamanho_str = tamanho_header.strip()
            if not tamanho_str:
                return None
            
            tamanho_dados = int(tamanho_str)

            dados_recebidos = b''
            bytes_pendentes = tamanho_dados
            
            # recebe os dados em blocos até ter o total
            while bytes_pendentes > 0:
                # recebe em blocos de 4096 ou menos
                chunk = conn.recv(min(4096, bytes_pendentes)) 
                if not chunk:
                    # Conexão fechada inesperadamente
                    return None
                dados_recebidos += chunk
                bytes_pendentes -= len(chunk)
                
            return dados_recebidos

        except ValueError as e:
            print(f"Erro ao receber binário (ValueError): {e}")
            return None
        
        except Exception as e:
            print(f"Erro ao receber binário: {e}")
            return None