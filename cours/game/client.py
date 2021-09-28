import socket

sock = None

def main(count_players="2", ip="127.0.0.1", port=7878):
    global sock
    sock = socket.socket()
    sock.connect((ip, int(port)))

    sock.send(count_players.encode())

    print(sock.recv(1024).decode().strip())




def send(mes_from_client):
    sock.send(mes_from_client)

def get_mes():
    mes_from_serv = sock.recv(1024)
    if mes_from_serv.decode().strip() == "0":
        sock.close()
        return 0
    return mes_from_serv

