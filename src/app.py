import tkinter as tk
import ctypes
import random
user32 = ctypes.windll.user32

from PIL import Image, ImageTk
from src.config import *
from src.utils import *

class TicTacToe(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.iconbitmap ('src/img/puzzle.ico')
        self.title('TicTac Give Me Your Toe')
        self.geometry(f"400x500+{int(user32.GetSystemMetrics(0)/2)-250}+{int(user32.GetSystemMetrics(1)/2)-325}") #https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python
        self.resizable(False, False)

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(GamePage, BACKGROUND)

    def show_frame(self, page, *args, **kwargs):
        frame = page(self.container, self, *args, **kwargs)
        frame.grid(sticky='nsew')
        frame.tkraise() # Ensures frame is visible in GUI

class GamePage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller

        self.option_tile = []
        self.game_tile = []
        self.curr_state = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.user = ''
        self.ai =''
        self.is_done = False
        self.is_winner = ''
        self.is_user_first = False

        self.o_image = ImageTk.PhotoImage(Image.open(f'src/img/O.png'))
        self.x_image = ImageTk.PhotoImage(Image.open(f'src/img/X.png'))
        self.n_image = ImageTk.PhotoImage(Image.open(f'src/img/N.png'))

        self.initial_prompt()
    
    # Prompt user if they want to be 'X' or 'O'
    def initial_prompt(self):
        self.frame_question = tk.Frame(self, BACKGROUND)
        self.frame_question.pack(pady=(175, 0))
        
        self.prompt_title = tk.Label(self.frame_question, text='Choose your side', **TITLE)
        self.prompt_title.pack()

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.frame_question, BACKGROUND)
        self.button_frame.pack(pady=10)

        # Create two buttons inside the button frame
        btn_p = ['X', 'O']
        for index in range(2):
            self.option_tile.append(tk.Button(self.button_frame, text=btn_p[index], command=lambda index=index: self.on_option_click(index), **TILE))
            self.option_tile[index].pack(side='left', padx=5)
        
        # Add images
        self.option_tile[0].configure(image = self.x_image)
        self.option_tile[1].configure(image = self.o_image)

    def on_option_click(self, index):
        print(f"Chosen side: {self.option_tile[index]['text']}")
        # Set condition if user is first
        if self.option_tile[index]['text'] == 'X': self.is_user_first = True

        # Destroy widgets to clear the window
        self.frame_question.destroy()
        for button in self.option_tile: button.destroy()

        # After destroying elements, display new elements
        self.display_elements()
        
    def display_elements(self):
        # Title
        self.frame_title = tk.Frame(self, BACKGROUND)
        self.frame_title.pack(pady=(40, 0))
        self.title = tk.Label(self.frame_title, text='TicTacToes', **TITLE)
        self.title.pack()

        # Appears when there is a winner
        self.subtitle = tk.Label(self.frame_title, text='', **TITLE)
        self.subtitle.pack()

        # Container for the game elements
        self.frame_game = tk.Frame(self, BACKGROUND)
        self.frame_game.pack(pady=(20, 0))

        # Tile frame
        self.frame_board = tk.Frame(self.frame_game, BACKGROUND)
        self.frame_board.grid(row=2, columnspan=2)

        self.initialize_board()
        self.populate_tiles()

        # Make AI 'X'
        self.ai = 'X'

        # Randomize first move of AI
        if not self.is_user_first and not self.is_done: 
            random_index = random.randint(0, 8)  # Generate a random index between 0 and 8
            self.curr_state[random_index // BOARD_SIZE][random_index % BOARD_SIZE] = 'X'
            self.game_tile[random_index].configure(image=self.x_image, text='1')
        
    def initialize_board(self):
        for index in range(9):
            self.game_tile.append(tk.Button(self.frame_board, **TILE))
            self.game_tile[index].grid(row=int(index/BOARD_SIZE), column=index%BOARD_SIZE, padx=5, pady=5)

    def populate_tiles(self):
        for tile_index in range(9):
            self.game_tile[tile_index].configure(
                image = self.n_image,
                text = -1,
                state = 'normal',
                command = lambda tile_index=tile_index: self.user_move(tile_index)
            )
    
    # USER'S TURN
    def user_move(self, tile_index):
        tile_value = self.game_tile[tile_index].cget('text')

        if self.is_user_first:
            if tile_value == -1 and not self.is_done:
                self.curr_state[tile_index//BOARD_SIZE][tile_index%BOARD_SIZE] = 'X'
                # Change tile image
                self.game_tile[tile_index].configure(
                    image=self.x_image,
                    text='1'
                )
                self.ai = 'O'
                self.ai_move()
        else:
            if tile_value == -1 and not self.is_done:
                self.curr_state[tile_index//BOARD_SIZE][tile_index%BOARD_SIZE] = 'O'
                # Change tile image
                self.game_tile[tile_index].configure(
                    image=self.o_image,
                    text='1'
                )
                self.ai_move()  

    # AI'S TURN
    def ai_move(self):
        m = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        move = []

        # Initial maximization
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.curr_state[row][column] == ' ':
                    self.curr_state[row][column] = self.ai
                    # Maximization/Minization of TicTacToe
                    self.user = 'O' if self.ai == 'X' else 'X'
                    score = min_max(0, False, self.curr_state, alpha, beta, self.ai, self.user)
                    self.curr_state[row][column] = ' '
                    if score > m:
                        m = score
                        move = (row, column)
    
        # Update moves after min_max returns a result
        if move:                
            row, column = move
            self.curr_state[row][column] = self.ai
            img = self.o_image if self.is_user_first else self.x_image 
            self.game_tile[row*BOARD_SIZE+column].configure(image=img,text='1')

        # Check if there is a winner
        if check_state(self.curr_state) == self.user: 
            self.is_done = True
            self.is_winner = 'USER'
        elif check_state(self.curr_state) == self.ai: 
            self.is_done = True
            self.is_winner = 'AI'
        elif check_draw(self.curr_state): 
            self.is_done = True 
            self.is_winner = 'No one'

        # PRINT
        print('\nWINNER: ', self.is_winner)
        print('IS DONE: ', self.is_done)
        for row in self.curr_state:
            print(row)
        # PRINT

        if self.is_done: self.subtitle.configure(text=f'{self.is_winner} wins!')
