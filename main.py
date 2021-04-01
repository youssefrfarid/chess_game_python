# Import Statements
import pygame
from constants import *
from engine import Board, Pieces, Move

# Initialising the Pieces and Board
pieces = Pieces()
board = Board()


# Drawing the board
def drawBoard(screen):  
  colors = [LIGHTCOL, DARKCOL]
  
  for rank in range(RANKS):
    for file in range(FILES):
      # Decide if its a light or a dark square
      color = colors[((rank+file) % 2)]
      # drawing the square
      pygame.draw.rect(screen, color, pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen):
  for rank in range(8):
    for file in range(8):
      if board.board[rank][file] != 0:
        # loops through every non-empty square on the board
        screen.blit(pieces.images[board.board[rank][file]], pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))


def highlightSquares(screen, board, validMoves, squareSelected):
  if squareSelected != ():
    # Highlight Square
    r, f = squareSelected
    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
    s.set_alpha(150)
    s.fill(pygame.Color('blue'))
    if board[r][f] != 0:
      screen.blit(s, (f*SQUARE_SIZE, r*SQUARE_SIZE))
      # Highlight Moves from Square
      s.fill(pygame.Color('purple'))
      for move in validMoves:
        if move.startRow == r and move.startCol == f:
          screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))
        
def drawGame(screen, validMoves, squareSelected):
  drawBoard(screen)
  highlightSquares(screen, board.board, validMoves, squareSelected)
  drawPieces(screen)
   
# Initialising the Window
def main():
  # Variables needed for pygame
  run = True
  
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Chess')
  
  selectedSquare = () # (x, y)
  playerClicks = [] # Has 2 tuples Start, End
  validMoves = board.getValidMoves()
  
  madeMove = False # flag to only check valid moves once a move is made boosting performance
  
  while run:
    for event in pygame.event.get():
      # if user closes the program
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # if the user clicks the left mouse button
        if event.button == 1:
          # Gets the mouse location and divides by the square size this integer value is the index of the square
          location = pygame.mouse.get_pos()
          col = location[0] // SQUARE_SIZE
          row = location[1] // SQUARE_SIZE
          
          if selectedSquare == (row, col):
            selectedSquare = () # Deselect as user clicked twice
            playerClicks = [] # Reset Clicks
          else:  
            selectedSquare = (row, col)
            playerClicks.append(selectedSquare)

          if len(playerClicks) == 2:
            # deselects the clicks on empty squares
            if board.board[playerClicks[0][0]][playerClicks[0][1]] == 0:
              playerClicks = []
            else:
              # creates the Move object and executes the move if its in the Valid moves
              move = Move(playerClicks[0], playerClicks[1], board)
              print(move.getChessNotation())
              if move in validMoves:
                board.makeMove(move)
                madeMove = True
              # resets the variables for the next move
              selectedSquare = ()
              playerClicks = []
              
        elif event.button == 3:
          # if the user clicks the right mouse button
          board.undoMove()
          madeMove = True
      
      # if a move is made or unmade check for the valid moves for this position             
      if madeMove:
          validMoves = board.getValidMoves()
          madeMove = False
          
      clock.tick(FPS)
      drawGame(screen, validMoves, selectedSquare)      
      pygame.display.flip()
      
  pygame.quit()  
  
if __name__ == '__main__':
  main()