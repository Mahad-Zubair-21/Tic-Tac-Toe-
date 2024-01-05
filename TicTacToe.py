import sys
import copy
import pygame
import random
import numpy as np

pygame.init()
#----------------------------------------------------------#
# Constants
WIDTH = 600
HEIGHT = 600
bg_color = (0, 0, 0)
rows = 3
cols = 3
square = WIDTH // cols
line_color = (197, 179, 88)
color = (139,0,0)
color2 = (0,66,66)
radius = square // 4
circle_width = 15
#----------------------------------------------------------#
# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC-TAC-TOE')
screen.fill(bg_color)

#----------------------------------------------------------#
class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        self.empty_squares = self.squares
        self.marked_squares = 0
        
    def final_state(self, show = False):
        # 0 = draw, 1 = player , 2 = ai
        #---to check vertical win---#
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    Color = color if self.squares[0][col]== 2 else color2
                    iPos = (col * square + square //2,20)
                    fPos = (col * square + square //2,HEIGHT - 20)
                    pygame.draw.line(screen,Color,iPos,fPos,15)
                return self.squares[0][col]
        #---to check horizontal win---#    
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    Color = color if self.squares[row][0]== 2 else color2
                    iPos = (20,row*square + square //2)
                    fPos = (WIDTH - 20, row*square+square //2)
                    pygame.draw.line(screen,Color,iPos,fPos,15)
                return self.squares[row][0]
        #---to check ascending diagonal win---#
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    Color = color if self.squares[1][1]== 2 else color2
                    iPos = (20,HEIGHT - 20)
                    fPos = (WIDTH -20 , 20)
                    pygame.draw.line(screen,Color,iPos,fPos,15)
            return self.squares[1][1]   
        #---to check descending diagonal win---#    
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    Color = color if self.squares[1][1]== 2 else color2
                    iPos = (20,20)
                    fPos = (WIDTH -20 , HEIGHT - 20)
                    pygame.draw.line(screen,Color,iPos,fPos,15)
            return self.squares[1][1]
        return 0 #---depicting no win/draw---#    
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1 
    ##--- for the ai ---##
    def get_empty(self):
        empty_squares = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row,col):
                    empty_squares.append((row,col))
        return empty_squares
    
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty (self):
        return self.marked_squares == 0
#----------------------------------------------------------#

class AI:
    def __init__(self,level = 1, player =2):
        self.level = level
        self.player = player
    def rnd(self,board):
        empty_squares = board.get_empty()
        index = random.randrange(0,len(empty_squares))
    
        return empty_squares[index]
    
    def minimax(self,board,maximizing): ##ai is the player that is minimizing
        #---terminal cases --#
        case = board.final_state()
        
        #---player 1 wins---#
        if case == 1:
            return 1,None #--eval,move--#
        #--AI wins---#
        if case == 2:
            return -1,None
        #--if its a draw--#
        elif board.is_full():
            return 0,None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty()
            
            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimax(temp_board,False)[0]#--tels that next move is by minimizing player
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
            return max_eval,best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty()
            
            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
            return min_eval,best_move
                            
    def eval(self,main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval,move = self.minimax(main_board,False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move
    
    
#----------------------------------------------------------#
class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 ## set to 2 if u want ai to start
        self.game_mode = 'ai'
        self.running = True
        self.display_lines()
        self.font = pygame.font.SysFont(None ,40)

    def display_lines(self):
        screen.fill(bg_color)
        
        for i in range(1, cols):
            pygame.draw.line(screen, line_color, (i * square, 0), (i * square, HEIGHT), 15)
            pygame.draw.line(screen, line_color, (0, i * square), (WIDTH, i * square), 15)
            

    def next_turn(self):
        self.player = self.player % 2 + 1
    
    def make_move(self,row,col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row,col)## responsible for drawing the figure
        self.next_turn()
    
    def draw_fig (self,row,col):
        Color = (255,105,180)
        if self.player == 1:
            triangle_points = [
            (col * square + square // 2, row * square + 30),
            (col * square + 30, row * square + square - 30),
            (col * square + square - 30, row * square + square - 30)
        ]
            pygame.draw.polygon(screen, Color, triangle_points)
        elif self.player == 2:
            paint = (138,43,226)
            center  = (col * square + square // 2, row * square + square//2 )
            pygame.draw.circle(screen, paint,center, radius, circle_width)
    
    def change_gamemode(self):
        self.game_mode = 'ai' if self.game_mode =='pvp' else 'pvp'
    
    def reset(self):
        self.__init__() #-- resets all attributes to default values--#
        
    def is_over(self):
        result = self.board.final_state(show=True)
        if result != 0:
            if result == 1:
                self.display_message("Player wins!", color)
            elif result == 2:
                self.display_message("AI wins!", color)
            return True

        if self.board.is_full():
            self.display_message("It's a draw!", color)
            return True

        return False
    
    def display_message(self, text, text_color):
        box_width = 300
        box_height = 100
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2

        pygame.draw.rect(screen, color2, (box_x, box_y, box_width, box_height))
        
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
#----------------------------------------------------------#
def main():
    game = Game()
    ai = game.ai
    board = game.board
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                #--g changes game mode--#
                if event.key == pygame.K_g:
                    game.change_gamemode()
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                
                #-- O for random ai--#
                if event.key == pygame.K_0:
                    ai.level = 0
                #-- I for random ai--#
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // square
                col = pos[0] // square
                if game.board.empty_sqr(row, col) and game.running:
                    game.make_move(row,col)
                    
                    if game.is_over():
                        game.running = False
                
        if game.game_mode == 'ai' and game.player == ai.player and game.running:
             pygame.display.update()
             
             #---ai method---#
             row,col = ai.eval(board)
             game.make_move(row,col)
        
        pygame.display.update()


if __name__ == "__main__":
    main()
