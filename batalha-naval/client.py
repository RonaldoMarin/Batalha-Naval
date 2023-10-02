import socket

# Crie um socket TCP para o cliente
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
Porta localhost para teste 
"""
tcp_client_socket.connect(('localhost', 12345))
# tcp_client_socket.connect(('ip do host', 12345))

# Crie um socket UDP para enviar o nome do jogador
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Nome do jogador
player_name = input("Digite o nome do jogador: ")

# Envie o nome do jogador por meio do socket UDP
"""
Porta localhost para teste 
"""
udp_client_socket.sendto(player_name.encode(), ('localhost', 12346))
# udp_client_socket.sendto(player_name.encode(), ('ip do host', 12346))

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
            print("Você venceu!")
            break

play_game()

# Feche os sockets quando o jogo terminar
tcp_client_socket.close()
udp_client_socket.close()
