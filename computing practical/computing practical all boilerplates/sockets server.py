import socket

server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen()
print("waiting for client to connect")
client, address = server.accept()
print(f"connected to client at {address}")

while 1+1==2:
    # 1. Receive client's guess
    data = b''
    while b'\n' not in data:
        data += client.recv(1024)
    guess = data.decode().strip()
    
    # 2. Process logic (Check win/loss)
    if guess == "QUIT":
        break
    elif guess == secret_word:
        client_socket.sendall(b"WIN\n")
        break
    else:
        client_socket.sendall(b"WRONG\n")

client_socket.close()

client.close()
server.close()
