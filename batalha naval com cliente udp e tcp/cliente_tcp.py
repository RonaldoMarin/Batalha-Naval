import socket

# Configuração do cliente TCP
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(('localhost', 12345))

# Recebe o tabuleiro do servidor
board = eval(tcp_client_socket.recv(1024).decode())
print("Tabuleiro recebido:")
print(board)

while True:
    # Pede ao jogador para fornecer coordenadas de ataque
    row = int(input("Digite a linha do seu ataque: "))
    col = int(input("Digite a coluna do seu ataque: "))

    # Envia os dados de ataque para o servidor via UDP
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.sendto(f"{row} {col}".encode(), ('localhost', 12346))
    udp_client_socket.close()

    # Recebe a resposta do servidor TCP
    response = tcp_client_socket.recv(1024).decode()
    print(response)
