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
    # White and blacks kings positions will be used in checks and castling
    # Updated in makeMove and undoMove
    self.wKingPos = (7, 4) # Row, Col in internal board
    self.bKingPos = (0, 4) # Row, Col in internal board
    
    self.inCheck = False
    self.pins = []
    self.checks = []
   
   
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
    # Update Kings location
    if move.pieceMoved == 9:
      self.wKingPos = (move.endRow, move.endCol)
    elif move.pieceMoved == 17:
      self.bKingPos = (move.endRow, move.endCol)
      
  # A Move is undone by drawing whatever was on the target square and return the piece to the starting square
  def undoMove(self):
    try:
      undo = self.moveLog[-1] # Gets last item in moveLog
      self.board[undo.startRow][undo.startCol] = undo.pieceMoved # redraws the piece moved in its initial position
      self.board[undo.endRow][undo.endCol] = undo.pieceCaptured # redraws the piece captured in its initial position
      self.moveLog.pop() # removes the last move after its undone
      self.whiteToMove = not self.whiteToMove # switches the turn
      # Update Kings location
      if undo.pieceMoved == 9:
        self.wKingPos = (undo.endRow, undo.endCol)
      elif undo.pieceMoved == 17:
        self.bKingPos = (undo.endRow, undo.endCol)  
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
    
    self.lookForCaptures(r, f, color, moves)
    
  def generateKnightMoves(self, r, f, moves):
    targets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)] # the 8 squares a knight can go to
    opponentColor = 'b' if self.whiteToMove else 'w' # assigns opponentColor based on whiteToMove
    
    for t in targets:
      # adds the all possible squares in a direction
      targetRow = r + t[0] 
      targetCol = f + t[1]
      if 0 <= targetRow < 8 and 0 <= targetCol < 8: # makes sure the square is on the board
        targetPiece = self.board[targetRow][targetCol]
        if targetPiece == 0: # Empty Space
          moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
        elif self.BinaryToPieces[targetPiece][0] == opponentColor: # Checks if the piece is an enemy piece
          moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
          pass 
        else: # Friendly piece
          pass
      else: # The square is off the board
        pass
    
    
  def generateDiagonalMoves(self, r, f, moves):
    # For Bishop and Queen
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # 4 diagonals
    opponentColor = 'b' if self.whiteToMove else 'w' # assigns opponentColor based on whiteToMove
    
    for d in directions:
      for i in range(1, 8):
        # adds the all possible squares in a direction
        targetRow = r + d[0] * i 
        targetCol = f + d[1] * i
        if 0 <= targetRow < 8 and 0 <= targetCol < 8: # makes sure the square is on the board
          targetPiece = self.board[targetRow][targetCol]
          if targetPiece == 0: # Empty Space
            moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
          elif self.BinaryToPieces[targetPiece][0] == opponentColor: # Checks if the piece is an enemy piece
            moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
            break # No need to look beyond a piece
          else: # Friendly piece
            break # No need to look beyond a piece
        else: # The square is off the board
          break
          
  def generateSlidingMoves(self, r, f, moves):
    # For Rook and Queen
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)] # Up, left, down, right
    opponentColor = 'b' if self.whiteToMove else 'w' # assigns opponentColor based on whiteToMove
    
    for d in directions:
      for i in range(1, 8):
        # adds the all possible squares in a direction
        targetRow = r + d[0] * i 
        targetCol = f + d[1] * i
        if 0 <= targetRow < 8 and 0 <= targetCol < 8: # makes sure the square is on the board
          targetPiece = self.board[targetRow][targetCol]
          if targetPiece == 0: # Empty Space
            moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
          elif self.BinaryToPieces[targetPiece][0] == opponentColor: # Checks if the piece is an enemy piece
            moves.append(Move((r, f), (targetRow, targetCol), self)) # Adds the move to the possible moves
            break # No need to look beyond a piece
          else: # Friendly piece
            break # No need to look beyond a piece
        else: # The square is off the board
          break
  
  def generateKingMoves(self, r, f, moves):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, -1)] # 8 squares around a king
    opponentColor = 'b' if self.whiteToMove else 'w'
    
    for d in directions:
      # adds the all possible squares in a direction
      targetRow = r + d[0] 
      targetCol = f + d[1]
      if 0 <= targetRow < 8 and 0 <= targetCol < 8: # makes sure the square is on the board
        piece = self.board[targetRow][targetCol]
        pieceColor, pieceType = self.getPieceData(piece)
        
        if not self.isAttacked(targetRow, targetCol):
          if piece == 0:
            moves.append(Move((r, f), (targetRow, targetCol), self))
          elif pieceColor == opponentColor:
            moves.append(Move((r, f), (targetRow, targetCol), self))

      else: # The square is off the board
        pass
      
  def lookForCaptures(self, r, f, color, moves):
    # Pawn Captures
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
    if pieceType == 'B' or pieceType == 'Q':
      self.generateDiagonalMoves(r, f, moves)
    if pieceType == 'R' or pieceType == 'Q':
      self.generateSlidingMoves(r, f, moves)
    if pieceType == 'N':
      self.generateKnightMoves(r, f, moves)
    #if pieceType == 'K':
     # self.generateKingMoves(r, f, moves)
      
    return []

  def getValidMoves(self):
    self.inCheck, self.pins, self.checks = self.lookForChecksPins()
    print(self.inCheck, self.pins, self.checks)
    if self.whiteToMove:
      kingR = self.wKingPos[0]
      kingC = self.wKingPos[1]
    else:
      kingR = self.bKingPos[0]
      kingC = self.bKingPos[1]
    
    if self.inCheck:
      if len(self.checks) == 1:
        moves = self.generateAllMoves()
        check = self.checks[0]
        checkR = check[0]
        checkC = check[1]
        checkPiece = self.board[checkR][checkC]
        checkPieceColor, checkPieceType = self.getPieceData(checkPiece)
        validSquares = []
        
        if checkPieceType == 'N':
          validSquares = [(checkR, checkC)]
        else:
          for i in range(1, 8):
            validSquare = (kingR + check[2] * i, kingC + check[3] * i)
            validSquares.append(validSquare)
            if validSquare[0] == checkR and validSquare[1] == checkC:
              break
        
        for i in range(len(moves) - 1, -1, -1):
          if moves[i].pieceMoved != 9 or moves[i].pieceMoved != 17:
            if not (moves[i].endRow, moves[i].endCol) in validSquares:
              moves.remove(moves[i])
        self.generateKingMoves(kingR, kingC, moves)
      else:
        moves = []
        self.generateKingMoves(kingR, kingC, moves)
    else:
      moves = self.generateAllMoves()
      self.generateKingMoves(kingR, kingC, moves)
    
    return moves

  def lookForChecksPins(self):
    pins = []
    checks = []
    inCheck = False
    
    if self.whiteToMove:
      opponentColor = 'b'
      startRow = self.wKingPos[0]
      startCol = self.wKingPos[1]
    else:
      opponentColor = 'w'
      startRow = self.bKingPos[0]
      startCol = self.bKingPos[1]
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for j in range(len(directions)):
      d = directions[j]
      maybePinned = ()
      for i in range(1, 8):
        endRow = startRow + d[0] * i
        endCol = startCol + d[1] * i
        
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          if self.board[endRow][endCol] != 0:
            piece = self.board[endRow][endCol]
            pieceColor, pieceType = self.getPieceData(piece)
            
            if pieceColor != opponentColor:
              if maybePinned == ():
                maybePinned = (endRow, endCol, d[0], d[1])
              else:
                break
            elif pieceColor == opponentColor:
              if (
                pieceType == 'Q' or
                pieceType == 'R' and 0 <= j <= 3 or 
                pieceType == 'B' and 4 <= j <= 7 or 
                pieceType == 'P' and i == 1 and ((opponentColor == 'w' and 6 <= j <= 7) or (opponentColor == 'b' and 4 <= j <= 5)) or
                pieceType == 'K' and i == 1
              ):
                if maybePinned == ():
                    inCheck == True
                    checks.append((endRow, endCol, d[0], d[1]))
                    break
                else:
                  pins.append(maybePinned)
              else:
                break
        else:
          break
    
    knightDirections = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for n in knightDirections:
      endRow = startRow + n[0]
      endCol = startCol + n[1]
      
      if 0 <= endRow < 8 and 0 <= endCol < 8:
        piece = self.board[endRow][endCol]
        pieceColor, pieceType = self.getPieceData(piece)
        
        if pieceType == 'N' and pieceColor == opponentColor:
          inCheck == True
          checks.append((endRow, endCol, n[0], n[1]))
    
    if len(checks) > 0:
      inCheck = True
    
    return inCheck, pins, checks

  def isAttacked(self, r, c):
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    opponentColor = 'b' if self.whiteToMove else 'w'
      
    for j in range(len(directions)):
      d = directions[j]
      for i in range(1, 8):
        endRow = r + d[0] * i
        endCol = c + d[1] * i
        
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          if self.board[endRow][endCol] != 0:
            piece = self.board[endRow][endCol]
            pieceColor, pieceType = self.getPieceData(piece)
            
            if pieceColor != opponentColor:
              break
            elif pieceColor == opponentColor:
              if (
                pieceType == 'Q' or
                pieceType == 'R' and 0 <= j <= 3 or 
                pieceType == 'B' and 4 <= j <= 7 or 
                pieceType == 'P' and i == 1 and ((opponentColor == 'w' and 6 <= j <= 7) or (opponentColor == 'b' and 4 <= j <= 5)) or
                pieceType == 'K' and i == 1
              ):
                return True
              else:
                break
        else:
          break
  
      knightDirections = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
      
      for n in knightDirections:
        endRow = r + n[0]
        endCol = c + n[1]
        
        if 0 <= endRow < 8 and 0 <= endCol < 8:
          piece = self.board[endRow][endCol]
          pieceColor, pieceType = self.getPieceData(piece)
          
          if pieceType == 'N' and pieceColor == opponentColor:
            return True
          
    return False

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