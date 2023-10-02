import socket
import random

# Crie um socket TCP para o servidor
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
Porta localhost para teste 
"""
tcp_server_socket.bind(('0.0.0.0', 12345))
# tcp_server_socket.bind(('ip do host', 12345))
tcp_server_socket.listen(5)

# Crie um socket UDP para receber o nome do jogador
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
"""
Porta localhost para teste 
"""
udp_server_socket.bind(('0.0.0.0', 12346))
# udp_server_socket.bind(('ip do host', 12346))

# Função para gerar o tabuleiro do jogo
def generate_board(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    for _ in range(size):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        board[row][col] = 1
    return board

# Função para verificar o palpite do cliente
def guess_ship_position(board, row, col):
    if board[row][col] == 1:
        board[row][col] = "X"  # Navio atingido
        return "Acertou!"
    else:
        return "Errou!"

# Receba o nome do jogador por meio do socket UDP
player_name, player_addr = udp_server_socket.recvfrom(1024)
print(f"Nome do jogador: {player_name.decode()}")


# Defina o tamanho do tabuleiro aqui
board_size = 5
tcp_clients = []

# Gere o tabuleiro do jogo
board = generate_board(board_size)
print("Tabuleiro do jogo:")
for row in board:
    print(" ".join(map(str, row)))

while True:
    # Espere por uma conexão TCP
    conn, addr = tcp_server_socket.accept()
    print(f"Conexão TCP de {addr}")
    tcp_clients.append(conn)

    # Envie o tamanho do tabuleiro para o cliente
    conn.send(str(board_size).encode())

    # Inicie o jogo
    while True:
        # Receba os palpites do cliente
        guess = conn.recv(1024).decode()
        if not guess:
            print(f"{player_name} desconectado")
            break  # O cliente desconectou
        row, col = map(int, guess.split())
        
        # Verifique o palpite e envie uma resposta ao cliente
        result = guess_ship_position(board, row, col)
        print(f"Palpite de {addr}: ({row}, {col}) -> {result}")
        conn.send(result.encode())

        # Verifique se todos os navios foram afundados
        if all(all(cell != 1 for cell in row) for row in board):
            result = "Todos os navios foram afundados!"
            print(result)
            conn.send(result.encode())
            break

# Feche os sockets quando o jogo terminar
for conn in tcp_clients:
    conn.close()

tcp_server_socket.close()
udp_server_socket.close()

