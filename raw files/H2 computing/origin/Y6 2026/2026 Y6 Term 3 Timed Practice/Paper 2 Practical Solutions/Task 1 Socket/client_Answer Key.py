def encrypt(plaintext):
    #process
    ciphertext = ""
    value_to_add = len(plaintext)

    for i in range(len(plaintext)):

        ascii_value = ord(plaintext[i]) + value_to_add 
        
        if ascii_value > 126: 
            ascii_value = ascii_value - 95

        ciphertext = ciphertext + chr(ascii_value)
        
        value_to_add = value_to_add - 1
    
    return ciphertext
	

#main program
import socket

print("-------------------")
print("CLIENT OPEN")
print("-------------------")
print()

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 9999))

message = input("Enter message: ")
encrypted_message = encrypt(message)

data = encrypted_message.encode()
my_socket.sendall(data + b'\n')
print("message sent")
my_socket.close()

print("-------------------")
print("CLIENT CLOSED")
print("-------------------")
