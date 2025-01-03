import pygame
import sys
from RoomConnect import RoomConnect

# The room number is displayed on the terminal upon execution. 
# I've also put my ngrok token inside a file named ".ngrok_token.txt" which gets read by the initialization script. 
# This is just a simple game for demonstration purposes, needs further development.

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Online Tic Tac Toe')
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.my_symbol = None
        self.game_active = False
        
        # Network
        self.network = RoomConnect(27555, "eu")
        with open(".ngrok_token.txt") as f:
            token = f.read().strip()
            self.network.set_token(token)
        
        self.network.register_message_type("move")
        self.network.register_message_type("reset")
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
        # Setup network connection
        self.setup_connection()
        
    def setup_connection(self):
        choice = input("Enter 'H' to host or 'J' to join: ").upper()
        nickname = input("Enter your nickname: ")
        
        if choice == 'H':
            self.my_symbol = 'X'
            room_number = self.network.host_game(nickname)
            print(f"Your room number is: {room_number}")
            self.game_active = True
            
        elif choice == 'J':
            self.my_symbol = 'O'
            room_number = input("Enter room number: ")
            if self.network.join_game(room_number, nickname):
                print("Connected successfully!")
                self.game_active = True
            else:
                print("Connection failed!")
                pygame.quit()
                exit()
        
    def draw_board(self):
        self.screen.fill(self.WHITE)
        
        # Draw grid lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, self.BLACK, 
                           (i * self.WIDTH // 3, 0), 
                           (i * self.WIDTH // 3, self.WIDTH), 3)
            pygame.draw.line(self.screen, self.BLACK, 
                           (0, i * self.WIDTH // 3), 
                           (self.WIDTH, i * self.WIDTH // 3), 3)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(row, col)
                    
    def draw_x(self, row, col):
        padding = 30
        x = col * self.WIDTH // 3 + padding
        y = row * self.WIDTH // 3 + padding
        size = self.WIDTH // 3 - 2 * padding
        pygame.draw.line(self.screen, self.RED, (x, y), (x + size, y + size), 3)
        pygame.draw.line(self.screen, self.RED, (x + size, y), (x, y + size), 3)
        
    def draw_o(self, row, col):
        padding = 30
        x = col * self.WIDTH // 3 + self.WIDTH // 6
        y = row * self.WIDTH // 3 + self.WIDTH // 6
        radius = self.WIDTH // 6 - padding
        pygame.draw.circle(self.screen, self.BLUE, (x, y), radius, 3)
        
    def handle_click(self, pos):
        if not self.game_active:
            return
            
        if self.my_symbol != self.current_player:
            return
            
        x, y = pos
        row = y // (self.WIDTH // 3)
        col = x // (self.WIDTH // 3)
        
        if row < 3 and self.board[row][col] == '':
            self.make_move(row, col)
            
    def make_move(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.my_symbol
            self.network.send_game_data('move', {
                'position': (row, col),
                'symbol': self.my_symbol
            })
            self.current_player = 'O' if self.my_symbol == 'X' else 'X'
        
    def check_win(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
            
        return None
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                    
            # Handle network messages
            if self.game_active:
                messages = self.network.get_messages()
                if messages:
                    for msg in messages:
                        if msg['type'] == 'move':
                            row, col = msg['data']['position']
                            symbol = msg['data']['symbol']
                            self.board[row][col] = symbol
                            self.current_player = 'O' if symbol == 'X' else 'X'
                            
            # Check for win
            winner = self.check_win()
            if winner:
                print(f"Player {winner} wins!")
                self.game_active = False
                self.board = [['' for _ in range(3)] for _ in range(3)]
                
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
