from socket import *                          #Server total: 7 marks
from random import *


my_socket = socket()
my_socket.bind(('127.0.0.1', 12345))
my_socket.listen()

new_socket, addr = my_socket.accept()
print('Connected to: ' + str(addr))

lst = ['WELL', 'YOGA', 'TRIP', 'WORD', 'RICH', 
       'CAKE', 'BIRD', 'SURF', 'DUCK', 'DOLL', 
       'FAME', 'GIFT', 'SILK', 'LADY', 'EASY',
       'LIKE', 'PATH', 'PLAY', 'REST', 'EPIC',
       'SAIL', 'TREE', 'TAIL', 'SELL', 'LEAF']      #[1] import list of words

msg = 'Welcome to the WORD GAME. You will be given 5 scrambled words to answer ... here we go:\n'
new_socket.sendall(msg.encode())                    #[1] send msg to start game 

score = 0

lst = sample(lst, 5)
for word in lst:                #[1] iterate list of 5 random words

    random_word = ''.join(sample(list(word), 4))
    msg = 'Enter the word you can form with "' + random_word + '": \n'
    new_socket.sendall(msg.encode())       #[1] send scrambled word with msg

    answer = ''
    while '\n' not in answer:
        answer += new_socket.recv(1024).decode()

    if answer.strip() == word:             #[1] compare player's input with correct word
        new_socket.sendall('Correct \n'.encode())
        score += 1
    else:
        new_socket.sendall('Incorrect \n'.encode())   #[1] send correct/incorrect msg
        
msg = 'You have answered ' + str(score) + ' out of 5 correctly. \n'
new_socket.sendall(msg.encode())                   #[1] send final msg with score

    
new_socket.close()
my_socket.close()
