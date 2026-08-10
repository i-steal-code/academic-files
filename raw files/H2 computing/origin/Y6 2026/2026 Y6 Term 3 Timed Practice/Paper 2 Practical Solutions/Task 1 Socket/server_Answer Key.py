def decrypt(ciphertext):
    
    plaintext = ""
    value_to_subtract = len(ciphertext)
    
    for i in range(len(ciphertext)):
        cipher_ASCII_value = ord(ciphertext[i])
        plain_ASCII_value = cipher_ASCII_value - value_to_subtract 

        if plain_ASCII_value < 32: 
            plain_ASCII_value = plain_ASCII_value + 95

        plaintext = plaintext + chr(plain_ASCII_value)
        
        value_to_subtract = value_to_subtract - 1
    
    return plaintext
	
#main
import socket #1 mark for importing all the needed libraries
import csv
import datetime


listen = True

print("-------------------")
print("SERVER OPEN")
print("-------------------")
print()


while listen:
    listen_socket = socket.socket() 
    listen_socket.bind(('127.0.0.1', 9999)) #1 mark for creating the socket with correct ip address and port number
    print("Waiting for message")
    print("-------------------")
    listen_socket.listen() #1 mark for starting the socket successfully and create new socket when received request from client program (next line)

    new_socket, addr = listen_socket.accept()

    data = b''
    while b'\n' not in data: #1 mark for receiving message from client program successfully
        data += new_socket.recv(1024)

    encrypted_message = data.decode().strip("\n") #1 mark for decoding the encrypted message
    print("Encrypted message: " + encrypted_message)
    decryted_message = decrypt(encrypted_message) #1 mark for decrypting the message
    print("Decrypted message: " + decryted_message)
    print("-------------------")

    now = datetime.datetime.now() 
	
    with open("log.csv", "a", newline = "") as outfile: #1 mark for writing successfully into log.csv file
        writer = csv.writer(outfile, delimiter=",")
        writer.writerow([now, addr[0], addr[1], encrypted_message, decryted_message]) #2 marks for writing all the correct details into log.csv. 1 mark if incomplete.
    #outfile closes automatically
    new_socket.close()
    listen_socket.close() #1 mark for closing both sockets
    
    user_input = input("Do you want to continue listening? [Y/N]: ") #1 mark for getting user input
    print()
    if user_input == "N": #2 marks for restarting the socket/end the program based on the user input
        listen = False
        print("-------------------")
        print("SERVER CLOSED")
        print("-------------------")
