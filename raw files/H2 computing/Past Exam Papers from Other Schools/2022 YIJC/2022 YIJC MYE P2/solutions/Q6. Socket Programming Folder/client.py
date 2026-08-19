from socket import *                    #Client total: 6 marks
my_socket = socket()
my_socket.connect(('127.0.0.1', 12345))

data =  ''
while '\n' not in data:
    data += my_socket.recv(1024).decode()
print(data)         #[1] receive and print start game msg

for i in range(5):  #[1] repeat receiving/guessing 5 words

    data =  ''
    while '\n' not in data:
        data += my_socket.recv(1024).decode()

    guess = input(data.strip())
    guess = guess.upper() + '\n'       #[1] obtain player's input
    my_socket.sendall(guess.encode())  #[1] send player's input in upper case

    data =  ''
    while '\n' not in data:
        data += my_socket.recv(1024).decode()

    print(data)              #[1] receive and print correct/incorrect msg

data =  ''
while '\n' not in data:
    data += my_socket.recv(1024).decode()
print(data)                  #[1] receive and print final msg


my_socket.close()
