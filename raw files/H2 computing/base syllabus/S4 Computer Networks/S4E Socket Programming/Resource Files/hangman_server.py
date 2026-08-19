class Hangman():
    def __init__(self, word):
        self.word = word
        # ? means the letter is not guessed correctly yet
        self.current_word_guessed = "?"*len(word)
    def check_and_update_letter(self, letter):
        result = []
        #return the positions of letter in word
        for i in range(len(word)):
            if word[i] == letter:
                result.append(i)
                self.current_word_guessed = self.current_word_guessed[:i] + letter + self.current_word_guessed[i+1:]
        return result
    def win(self):
        return self.word == self.current_word_guessed
    def quick_win(self, current_word_guessed):
        return self.word == current_word_guessed
    def display(self):
        print("Hidden secret word : " + self.word)
        print("Current guessed word  : " + self.current_word_guessed)
            
import socket
#socket.AF_INET => Using IPv4
#socket.SOCK_STREAM => Using TCP
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#'127.0.0.1 loop back address, 2345 port number
listen_socket.bind(('127.0.0.1', 12345))
print("waiting connection...")
listen_socket.listen()
game_socket, addr = listen_socket.accept()
print("connection accepted:")


game_over = False
# server sets secret word
word = ""
while len(word) == 0:
    word = input("Type a secret word:").lower()
    
hm_game = Hangman(word)
hm_game.display()
    
# server sends number of letters in the hidden word to client in START msg
msg_start = "START," + str(len(word))+"\n"
game_socket.send(msg_start.encode())
    
while not game_over:
    # server waits for client's GUESS msg or HWORD msg
    print("Waiting oppoent's move...")
    rx_msg_str = ""
    while "\n" not in rx_msg_str:
        rx_msg_str += game_socket.recv(1024).decode()
        
    if rx_msg_str[:5] == "GUESS":
        # send GUESS msg with positions of the correctly guessed letter
        positions = hm_game.check_and_update_letter(rx_msg_str[6])
             
        if not hm_game.win():
            msg_guess = "GUESS"
            for pos in positions:
                msg_guess += ","+str(pos)
            msg_guess += "\n"
            game_socket.send(msg_guess.encode())
        else:
            game_socket.send("WIN\n".encode())
            game_over = True
            print("Player wins.")
            
    elif rx_msg_str[:5] == "HWORD":
        game_over = True
        if hm_game.quick_win(rx_msg_str[6:-1]):
            game_socket.send("WIN\n".encode())
            print("Player wins.")
        else:
            game_socket.send("LOSE\n".encode())
            print("Player loses.")
    elif rx_msg_str[:4] == "QUIT":
        game_over = True
        game_socket.send("QUIT\n".encode())
        print("Player quits.")
    else:
        game_socket.send("INVALID\n".encode())
    hm_game.display()
        
game_socket.close()
listen_socket.close()
