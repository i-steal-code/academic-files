import socket

def recv_line(sock):
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

SECRET = "apple"

server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen()
print("waiting for client...")
client, address = server.accept()
print("connected to", address)

while True:
    guess = recv_line(client)
    if guess == "QUIT":
        break
    elif guess == SECRET:
        client.sendall(b"WIN\n")
        break
    else:
        client.sendall(b"WRONG\n")

client.close()
server.close()
print("server closed")
