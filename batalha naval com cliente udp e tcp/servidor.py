import socket
import random

# Configuração do servidor TCP
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(('0.0.0.0', 12345))
tcp_server_socket.listen(5)

# Configuração do servidor UDP
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(('0.0.0.0', 12346))

# Gera um tabuleiro com navios aleatórios
def generate_board(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    for _ in range(size):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        board[row][col] = 1
    return board

board_size = 10
tcp_clients = []

board = generate_board(board_size)

while True:
    # Aguarda a conexão de um cliente TCP
    client, addr = tcp_server_socket.accept()
    tcp_clients.append(client)
    print(f'Conexão TCP estabelecida com {addr}')

    # Envia o tabuleiro para o cliente TCP
    client.send(str(board).encode())

    # Aguarda dados do cliente UDP
    data, addr = udp_server_socket.recvfrom(1024)
    row, col = map(int, data.decode().split())

    # Verifica se houve acerto ou erro e envia a resposta para o cliente TCP
    response = "Acertou!" if board[row][col] == 1 else "Errou!"
    for tcp_client in tcp_clients:
        tcp_client.send(response.encode())

    # Reinicia o jogo
    board = generate_board(board_size)
