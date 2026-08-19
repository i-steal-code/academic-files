#client.py
'''Player will be given 7 tries to
input x and y coordinates and send to server.
After each input, the region data
consisting of characters '.', 'S', 'X', 'O'
will be displayed.
After 7 input by player, the final region data will be displayed.
'''

from socket import socket

my_socket = socket()
my_socket.connect(('127.0.0.1', 12345))     #connect to server

for i in range(7): #player has 7 tries to fire missile
    data = my_socket.recv(1024).decode() #receive region data from server 
    print(data)                          #display region data
    while True:
        xloc = input('Enter x location (0-11) : ') #player input x-coordinate
        if xloc.isdigit() and 0<=int(xloc)<=11:
            break
    
    while True:
        yloc = input('Enter y location (0-7) : ') #player input y-coordinate
        if yloc.isdigit() and 0<=int(yloc)<=7:
            break
        
    loc = xloc + ',' + yloc  #join x and y coordinate with a comma ','
    print(loc)               #display x and y coordinate input by player
    my_socket.sendall(loc.encode()) #send user input to server
   
data = my_socket.recv(1024).decode() #receive final region data, after player finishes 7 input
print(data)                          #display final region data

my_socket.close()                    # close client


