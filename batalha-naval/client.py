import socket

# Crie um socket TCP para o cliente
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(('localhost', 12345))

# Função para receber dados do servidor e enviar palpites
def play_game():
    board_size = int(tcp_client_socket.recv(1024).decode())
    print(f"Tabuleiro do jogo: {board_size}x{board_size}")

    while True:
        guess = input("Faça um palpite (linha coluna): ")
        tcp_client_socket.send(guess.encode())
        response = tcp_client_socket.recv(1024).decode()
        print(response)
        if "Todos os navios foram afundados!" in response:
            break

play_game()

# Feche o socket do cliente quando o jogo terminar
tcp_client_socket.close()
