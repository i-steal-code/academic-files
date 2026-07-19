#init and connect socket
import socket
client = socket.socket()
client.connect(("127.0.0.1", 5000))
state = "WRONG"

#client-side loop
while state = "WRONG":
    #send
    guess = input('key in your guess: ')
    client.sendall(f"{guess}\n".encode())
    print("sent to server...")
    if guess == 'QUIT':
        break
    #receive
    data = b''
    while b'\n' not in data:
        data += client.recv(1024)
    state = data.decode().strip()
    #process
    if state == 'WIN':
        print("you won woohoo")
        break
    print("try again")
#kill
print("program has ended. thanks for playing the game.")
client.close()
