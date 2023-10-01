import socket

while True:
    # Configuração do cliente UDP
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Pede ao jogador para fornecer coordenadas de ataque
    row = int(input("Digite a linha do seu ataque: "))
    col = int(input("Digite a coluna do seu ataque: "))

    # Envia os dados de ataque para o servidor via UDP
    udp_client_socket.sendto(f"{row} {col}".encode(), ('localhost', 12346))
    udp_client_socket.close()
