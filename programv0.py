import pygame
import socket
import json

class MarioMMOClient:
    def __init__(self):
        self.server_address = ('localhost', 8000)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_data = {}
        self.player_data = {}
        
    def connect_to_server(self):
        try:
            self.socket.connect(self.server_address)
            self.socket.sendall(b'Ready')
            
            data = self.socket.recv(2048).decode()
            self.game_data = json.loads(data)
            print(f"Connected to {self.game_data['title']} server")
            
        except ConnectionRefusedError:
            print("Could not connect to the game server")
            return False
        
        return True
            
    def load_assets(self):
        # Load sprite sheets, fonts, audio, etc.
        pass
        
    def update_player(self, player_data):
        # Update local player data
        self.player_data = player_data
        
    def render_map(self, map_data):
        # Render the current map using pygame
        pass
        
    def render_characters(self, character_data):
        # Render players and NPCs on the map
        pass
        
    def render_ui(self):
        # Render player stats, inventory, etc.
        pass

    def handle_input(self):
        # Handle player input (movement, actions, etc.)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.player_data['x'] -= 1
        if keys[pygame.K_RIGHT]:  
            self.player_data['x'] += 1
        if keys[pygame.K_UP]:
            self.player_data['y'] -= 1  
        if keys[pygame.K_DOWN]:
            self.player_data['y'] += 1
            
        # Send updated player data to server
        self.socket.sendall(json.dumps(self.player_data).encode())
        
    def game_loop(self):
        pygame.init()
        
        self.load_assets()
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # Receive game state updates from server
            data = self.socket.recv(2048).decode()
            game_state = json.loads(data)
            
            self.update_player(game_state['player'])
            
            # Clear screen
            pygame.display.get_surface().fill((0, 0, 0))
            
            self.render_map(self.game_data['maps'][game_state['map']])  
            self.render_characters(game_state['characters'])
            self.render_ui()
            
            self.handle_input()
            
            pygame.display.flip()
            clock.tick(60)
                
if __name__ == "__main__":
    client = MarioMMOClient()
    
    if client.connect_to_server():
        client.game_loop()