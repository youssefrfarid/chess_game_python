# Import Statement
import pygame

# This Class is responsible for the piece representation and loading of images. 
class Pieces:
  def __init__(self):
    # The Numbers represent Binary
    self.empty = 0 # 00000
    self.king = 1 # 00001
    self.pawn = 2 # 00010
    self.knight = 3 # 00011
    self.bishop = 4 # 00100
    self.rook = 5 # 00101
    self.queen = 6 # 00110
    # These are added to each binary number to represent the color (the last 2 bits)
    self.white = 8 # 01000
    self.black = 16 # 10000
    # Here the images are loaded ONCE in memory and scaled to 100*100 to match the square size
    self.images = {
      9: pygame.transform.scale(pygame.image.load('images\\wK.png'), (100,100)),
      17: pygame.transform.scale(pygame.image.load('images\\bK.png'),(100,100)),
      10: pygame.transform.scale(pygame.image.load('images\\wP.png'),(100,100)),
      18: pygame.transform.scale(pygame.image.load('images\\bP.png'),(100,100)),
      11: pygame.transform.scale(pygame.image.load('images\\wN.png'),(100,100)),
      19: pygame.transform.scale(pygame.image.load('images\\bN.png'),(100,100)),
      12: pygame.transform.scale(pygame.image.load('images\\wB.png'),(100,100)),
      20: pygame.transform.scale(pygame.image.load('images\\bB.png'),(100,100)),
      13: pygame.transform.scale(pygame.image.load('images\\wR.png'),(100,100)),
      21: pygame.transform.scale(pygame.image.load('images\\bR.png'),(100,100)),
      14: pygame.transform.scale(pygame.image.load('images\\wQ.png'),(100,100)),
      22: pygame.transform.scale(pygame.image.load('images\\bQ.png'),(100,100))
    }

# This class is responsible for the board.
# Generates moves
# Updates the board
# makes and undos moves
# Has the internal representation of the board
class Board:
  def __init__(self):
    # The internal representation of the board is a 2D 8*8 array
    # Binary values of pieces are used to indicate the starting position of a chess game
    self.board = [
      [21,19,20,22,17,20,19,21],
      [18,18,18,18,18,18,18,18],
      [0 for i in range(8)],
      [0 for i in range(8)],
      [0 for i in range(8)],
      [0 for i in range(8)],
      [10,10,10,10,10,10,10,10],
      [13,11,12,14,9,12,11,13]
    ]
    # Translates the Binary representation of the pieces to a string
    self.BinaryToPieces = {
      0: '--',
      9: 'wK',
      17: 'bK',
      10: 'wP',
      18: 'bP',
      11: 'wN',
      19: 'bN',
      12: 'wB',
      20: 'bB',
      13: 'wR',
      21: 'bR',
      14: 'wQ',
      22: 'bQ'
    }
    # Translates the other way around
    self.PiecesToBinary = {v: k for k,v in self.BinaryToPieces.items()}
    # Boolean flag indicating who to move
    self.whiteToMove = True
    # Keeps a list of Move objects used in undoing a move or several
    self.moveLog = []
   
  # Returns the Color, Type of a piece ex: 'w', 'P'
  def getPieceData(self, piece):
    data = self.BinaryToPieces[piece]
    return data[0], data[1]
    
  # A Move is made by drawing nothing in the staring square and redrawing the piece in the target square
  def makeMove(self, move):
    self.board[move.startRow][move.startCol] = 0 # places an empty space in the initial position of the piece to move
    self.board[move.endRow][move.endCol] = move.pieceMoved # places the piece to move in the target square
    self.moveLog.append(move) # appends the move to the move log used for undoMove()
    self.whiteToMove = not self.whiteToMove # switches the turn
  
  # A Move is undone by drawing whatever was on the target square and return the piece to the starting square
  def undoMove(self):
    try:
      undo = self.moveLog[-1] # Gets last item in moveLog
      self.board[undo.startRow][undo.startCol] = undo.pieceMoved # redraws the piece moved in its initial position
      self.board[undo.endRow][undo.endCol] = undo.pieceCaptured # redraws the piece captured in its initial position
      self.moveLog.pop() # removes the last move after its undone
      self.whiteToMove = not self.whiteToMove # switches the turn
    except:
      return  
  
  # This generates all possible moves in a given board without concerning checks
  def generateAllMoves(self):
    moves = []
    
    for r in range(len(self.board)):
      for f in range(len(self.board[r])):
        # loops the board and grabs each piece and gets its data
        if self.board[r][f] != 0:
          piece = self.board[r][f]
          pieceColor, pieceType = self.getPieceData(piece)
          # Deciding if white or black to move and if the piece selected is of same color
          if (self.whiteToMove and pieceColor == 'w'):
            self.generatePieceMoves(r, f, pieceColor, pieceType, moves)
          elif (not self.whiteToMove and pieceColor == 'b'):
            self.generatePieceMoves(r, f, pieceColor, pieceType, moves)
              
    return moves 

  def generatePawnMoves(self, r, f, color, moves):
    # Checks to see which color is the pawn
    if color == 'w':
      # White pawns start on row 6 on the board
      # checks to see if 2 squares ahead are available for a move
      if r == 6 and (self.board[r - 2][f] == 0) and (self.board[r - 1][f] == 0):
        moves.append(Move((r, f), (r - 2, f), self))
      # Checks the square infront of the pawn to move
      try:
        if self.board[r - 1][f] == 0:
          moves.append(Move((r, f), (r - 1, f), self))
      except:
        pass
        
    elif color == 'b':
      # Black pawns start on row 1 on the board
      # checks to see if 2 squares ahead are available for a move
      if r == 1 and (self.board[r + 2][f] == 0) and (self.board[r + 1][f] == 0):
        moves.append(Move((r, f), (r + 2, f), self))
      try:  
        # Checks the square infront of the pawn to move
        if self.board[r + 1][f] == 0:
          moves.append(Move((r, f), (r + 1, f), self))
      except:
        pass      
    
    self.lookForCaptures(r, f, color, 'P', moves)
  
  def generateDiagonalMoves(self, r, f, pieceColor, moves):
    if pieceColor == 'w':
      startRow = r
      startCol = f
      while f >= 0:
        if self.board[r - 1][f - 1] == 0:
          moves.append(Move((startRow, startCol), (r - 1, f - 1), self))
        r = r - 1
        f = f - 1
      r = startRow
      f = startCol
      while f < 7 and r < 7:
        if self.board[r + 1][f + 1] == 0:
          moves.append(Move((startRow, startCol), (r - 1, f - 1), self))
        r = r + 1
        f = f + 1
      
  
  def lookForCaptures(self, r, f, color, pieceType, moves):
    if pieceType == 'P': # Pawn Captures
      if color == 'w':
        # Checks if the pawn is on any edge 
        if f == 0:
          if self.board[r - 1][f + 1] > 16:
            moves.append(Move((r, f), (r - 1, f + 1), self))
        elif f == 7:
          if self.board[r - 1][f - 1] > 16:
            moves.append(Move((r, f), (r - 1, f - 1), self))
        else:
          # looks at both diagonal squares for captures
          if self.board[r - 1][f + 1] > 16:
            moves.append(Move((r, f), (r - 1, f + 1), self))
          if self.board[r - 1][f - 1] > 16:
            moves.append(Move((r, f), (r - 1, f - 1), self))
              
      elif color == 'b':
          if r == 0:
            pass
          # Checks if the pawn is on any edge
          elif f == 0:
            if self.board[r + 1][f + 1] < 16 and self.board[r + 1][f + 1] != 0:
              moves.append(Move((r, f), (r + 1, f + 1), self))
          elif f == 7:
            if self.board[r + 1][f - 1] < 16 and self.board[r + 1][f - 1] != 0:
              moves.append(Move((r, f), (r + 1, f - 1), self))
          else: 
            try:
              # looks at both diagonal squares for captures
              if self.board[r + 1][f + 1] < 16 and self.board[r + 1][f + 1] != 0:
                moves.append(Move((r, f), (r + 1, f + 1), self))
              if self.board[r + 1][f - 1] < 16 and self.board[r + 1][f - 1] != 0:
                moves.append(Move((r, f), (r + 1, f - 1), self))
            except:
              pass
  
  def generatePieceMoves(self, r, f, pieceColor, pieceType, moves):
    if pieceType == 'P':
      self.generatePawnMoves(r, f, pieceColor, moves)
    if pieceType == 'B':
      self.generateDiagonalMoves(r, f, pieceColor, moves)
    return []

  def getValidMoves(self):
    # To add checks and checking legal moves
    return self.generateAllMoves()
      
class Move(Board):
  RanksToRows = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0
  }
  RowsToRanks = {v: k for k,v in RanksToRows.items()}
  FilesToCols = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
  }
  ColsToFiles = {v: k for k, v in FilesToCols.items()}
  
  def __init__(self, startSQ, targetSQ, board):
    super().__init__()
    self.startRow = startSQ[0]
    self.startCol = startSQ[1]
    self.endRow = targetSQ[0]
    self.endCol = targetSQ[1] 
    self.boardSnapshot = board.board
    
    # unique ID from 0 - 7777
    self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    self.pieceMoved = self.boardSnapshot[self.startRow][self.startCol] 
    self.pieceCaptured = self.boardSnapshot[self.endRow][self.endCol]
  
  def __eq__(self, other):
    if isinstance(other,Move):
      return self.moveID == other.moveID
    return False
      
  
  def getChessNotation(self):
    piece = self.BinaryToPieces[self.pieceMoved][1]
    endSQ = self.ColsToFiles[self.endCol] + self.RowsToRanks[self.endRow] 
    return piece + endSQ