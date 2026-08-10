import socket
import random

# Define constants for map dimensions and treasures
MAP_WIDTH = 5
MAP_HEIGHT = 5
NUM_TREASURES = 5

# Define the map representation
EMPTY = '.'
TREASURE = 'T'
PLAYER = 'P'

# Define the server class
class TreasureHuntServer:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 5000))
        self.socket.listen()  # Allow player to connect
        print("Server is waiting for the player to connect...")
        self.player_socket, address = self.socket.accept()
        print("Player connected at",address)
        self.found = 0 # Keep track of number of treasures found, Initially 0
        self.player_position = () # Store position of player

    def start_game(self):
        self.map = self.generate_map() # Generate the map
        self.map = self.generate_player_position() # Generate the player's position
        self.send_map_state() # Send the initial state of the map to the player
        self.play_game() # Start the game loop

    def generate_map(self): # Generate a random map with treasures
        map_data = [[EMPTY for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        for _ in range(NUM_TREASURES): # Loop to create treasures on map
            # Generate random position for treasure using x and y coordinate
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            while map_data[y][x] == TREASURE: # Make sure no treasure is already at that position
                x = random.randint(0, MAP_WIDTH - 1)
                y = random.randint(0, MAP_HEIGHT - 1)
            map_data[y][x] = TREASURE # Put treasure at generated position
        return map_data

    def generate_player_position(self): # Generate a random position for the player on the map with treasures
        map_data = self.map
        # Generate random position for player using player_x and player_y coordinate
        player_x = random.randint(0, MAP_WIDTH - 1)
        player_y = random.randint(0, MAP_HEIGHT - 1)
        while map_data[player_y][player_x] == TREASURE: # Make sure player is not at treasure's position
            player_x = random.randint(0, MAP_WIDTH - 1)
            player_y = random.randint(0, MAP_HEIGHT - 1)
        map_data[player_y][player_x] = PLAYER # Put player at generated position on the map
        self.player_position = (player_y,player_x) # Store player's position
        print("Player is at", self.player_position) # Display player's position
        return map_data
    
    def send_map_state(self):
        # Send the current state of the map to the player
        map_data = '\n'.join(''.join(row) for row in self.map) # Format the map into rows and columns for ease of view
        print("Current state of map (Server's view with Treasure symbols):")
        print(map_data) # Display map
        
        # Replace treasure symbols(T) with empty symbools(.) before sending to player so that player can't see where the treasures are
        map_data = '\n'.join(''.join(EMPTY if cell == TREASURE else cell for cell in row) for row in self.map)
        print("Sending map to player (without the Treasure symbols) ...")
        self.player_socket.sendall(map_data.encode()) # Send map to client

    def play_game(self):
        # Initial player position
        player_y, player_x = self.player_position # Extract position of player from tuple
        # Game loop
        while True:
            move = self.player_socket.recv(1024).decode().strip().lower() # Receive player move

            # Update player position based on the move
            self.map[player_y][player_x] = EMPTY # Change player's current position to '.' as player has moved
            if move == 'up'[0]:                  # Move up
                player_y = max(0, player_y - 1)  # Update y-coordinate
            elif move == 'down'[0]:              # Move down
                player_y = min(MAP_HEIGHT - 1, player_y + 1) # Update y-coordinate
            elif move == 'left'[0]:              # Move left
                player_x = max(0, player_x - 1)  # Update x-coordinate
            elif move == 'right'[0]:             # Move right
                player_x = min(MAP_WIDTH - 1, player_x + 1) # Update x-coordinate

            self.player_position = (player_y,player_x)     # Store player's new position
            print("Player is now at",self.player_position) # Display player's position

            # Check if the player found a treasure
            if self.map[player_y][player_x] == TREASURE: # Found one treasure
                self.found += 1                          # Increment found counter
                self.player_socket.sendall("You found a treasure!\n".encode()) # Send message to client that a treasure is found

            self.map[player_y][player_x] = PLAYER # Update player's new position on map with 'P'

            # Check for gameover condition (when all treasures are found)
            if self.found == NUM_TREASURES: # found counter matches total number of treasures
                self.end_game()             # gameover, call end_game function
                break

            # Send updated map state to the player
            self.send_map_state()

    def end_game(self):
        # Game over: All treasures found
        print("Game over! Player found all treasures!")
        self.player_socket.sendall("Congratulations! You found all treasures.\n".encode()) # Send congratulatory message to client
        self.player_socket.close() # Close socket

# Main function to start the server
def main():
    server = TreasureHuntServer() # Create server object for game
    server.start_game()           # Start game

if __name__ == "__main__":
    main()
