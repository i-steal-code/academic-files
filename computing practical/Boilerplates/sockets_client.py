import socket

def recv_line(sock):
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

client = socket.socket()
client.connect(("127.0.0.1", 5000))
state = "WRONG"

while state == "WRONG":
    guess = input("key in your guess: ")
    client.sendall((guess + "\n").encode())
    if guess == "QUIT":
        break
    state = recv_line(client)
    if state == "WIN":
        print("you won")
        break
    print("try again")

print("program has ended")
client.close()
