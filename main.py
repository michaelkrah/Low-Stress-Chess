# Chesss

# Import and initialize the pygame library
import pygame as p
import engine
import math
import random

p.init()
p.font.init()
myfont = p.font.SysFont('Times New Roman', 30)
smallFont = p.font.SysFont('Times New Roman', 20)
display_width = 400
display_height = 600
screen = p.display.set_mode((display_width, display_height))
piece_size = display_width // 8
images = {}
game = engine.GameState()
numPiece = [16, 16]
lst = ["This is tough, but you are tougher", "Don’t stress. You got this!", "Sending some good vibes",
       "I believe in you!", "Things are going to start looking up soon", "I admire how strong you are!",
       "Take a deep breath; it’s just a bad day, not a bad life", "Storms don’t last forever!",
       "Don’t wait for opportunity. Create it!"]

def loadImages():
    """Loads images to the file"""
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), (piece_size, piece_size))


def createBoard():
    """Creates the board template"""
    screen.fill((255, 255, 255))

    # Creates the text for whose turn it is
    turnCount = turnCounter(game.whiteTurn)
    screen.blit(turnCount, (125, 10))

    if check(game.board, game.whiteTurn):
        if game.whiteTurn:
            piece = 'White'
        else:
            piece = 'Black'
        checkTurn = smallFont.render(piece + ' is in check', True, (0, 0, 0))
        screen.blit(checkTurn, (120, 50))

    x = 0
    y = 200
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                color = (65, 189, 82)
            else:
                color = (22, 98, 137)
            p.draw.polygon(screen, color, [(x, y), (x + 50, y), (x + 50, y + 50), (x, y + 50)])
            x += 50
        y += 50
        x = 0
    for r in range(8):
        p.draw.line(screen, (0, 0, 0), (0, 200 + 50 * r), (400, 200 + 50 * r))
    for c in range(8):
        p.draw.line(screen, (0, 0, 0), (50 * c, 200), (50 * c, 600))


def turnCounter(turn):
    """Creates the text needed every turn at the top of the board screen"""
    numPiece = num_pieces()
    if turn:
        if numPiece[0] < numPiece[1]:
            message = random.choice(lst)
            screen.blit(smallFont.render(message, True, (0, 0, 0)), (10, 150))
        return myfont.render('White Turn', True, (0, 0, 0))

    else:
        if numPiece[0] > numPiece[1]:
            message = random.choice(lst)
            screen.blit(smallFont.render(message, True, (0, 0, 0)), (10, 150))
        return myfont.render('Black Turn', True, (0, 0, 0))


def num_pieces():
    w = 0
    b = 0
    for r in range(8):
        for c in range(8):
            if game.board[r][c][0] == 'w':
                w += 1
            elif game.board[r][c][0] == 'b':
                b += 1
    return [w, b]


def piecePicked(piece):
    """Writes text for the piece that has been picked every turn"""
    pieceName = piece[1]

    dictPiece = {'B': 'bishop', 'K': 'King', 'N': 'Knight', 'P': 'Pawn', 'Q': 'Queen', 'R': 'Rook'}
    print("dictionary name seleected", dictPiece[pieceName])
    piecePick = smallFont.render('The player has selected a ' + dictPiece[pieceName], True, (0, 0, 0))
    screen.blit(piecePick, (70, 40))
    p.display.flip()


def createPieces(s, b):
    """Updates the pieces based on engine file"""
    for r in range(len(b)):
        for c in range(len(b[0])):
            # b is a 2d array
            piece = b[r][c]
            if piece != '  ':
                s.blit(images[piece], p.Rect(c * piece_size, r * piece_size + 200, piece_size, piece_size))


def getPiece(turn, pieceGot):
    """Checks if player has picked a valid piece"""
    getPieceValid = True
    while getPieceValid:
        for event in p.event.get():
            if event.type == p.QUIT:
                return False

            if event.type == p.MOUSEBUTTONUP:
                # turn checker
                if turn:
                    color = 'w'
                else:
                    color = 'b'

                # checks if piece below mouse can currently move based on turn
                mousePosition = p.mouse.get_pos()
                xSquare = math.floor(mousePosition[0] / 50)
                ySquare = math.floor((mousePosition[1] - 200) / 50)

                if color == game.board[ySquare][xSquare][0] and validMove([ySquare, xSquare]):
                    pieceGot[0] = True
                    pieceMoving = game.board[ySquare][xSquare]
                    position = [ySquare, xSquare]
                    
                    # Adds the text to the top screen
                    piecePicked(pieceMoving)

                    getPieceValid = False
                    return [pieceMoving, position]
                print('pick another piece')


def movePiece(piece, position):
    validPiece = True
    while validPiece:
        for event in p.event.get():
            if event.type == p.QUIT:
                return False
            if event.type == p.MOUSEBUTTONDOWN:
                # print(piece, position)
                mousePosition = p.mouse.get_pos()
                xGoal = math.floor(mousePosition[0] / 50)
                yGoal = math.floor((mousePosition[1] - 200) / 50)
                # print(yGoal, xGoal)
                if canMove(position[0], position[1], yGoal, xGoal):
                    validPiece = False
                    print('yep')
                    executeMove(position[0], position[1], yGoal, xGoal)
                    return
                print('choose a valid move')


def executeMove(r_current, c_current, row_next, col_next):
    """Updates board stored in engine"""
    # print(row_next, col_next)
    # print(r_current,c_current)
    game.board[row_next][col_next] = game.board[r_current][c_current]
    game.board[r_current][c_current] = '  '


def updateBoard(boardPositions):
    """Updates and rewrites board position on screen"""
    createBoard()
    createPieces(screen, game.board)


def canMove(r_current, c_current, row_next, col_next):
    """" Returns whether it can move or not ,i.e. True or False """
    print(r_current, c_current, row_next, col_next)
    print("piece name", game.board[r_current][c_current][1])

    # if check(game.board, game.whiteTurn) == True:
    # return False

    # Check if space is filled by teammate
    # print(c_current-col_next)
    if game.board[r_current][c_current][0] == game.board[row_next][col_next][0]:
        return False

    # Bishop
    if game.board[r_current][c_current][1] == 'B':
        # It can only move diagonally
        if abs(r_current - row_next) == abs(c_current - col_next) and (c_current - col_next != 0):

            # Checks to make sure piece can't skip other pieces
            if row_next < r_current and col_next > c_current:
                r_Count = -1
                c_Count = 1
                for r in range(row_next + 1, r_current):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count -= 1
                    c_Count += 1
            elif row_next < r_current and c_current > col_next:
                r_Count = -1
                c_Count = -1
                for r in range(row_next + 1, r_current):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count -= 1
                    c_Count -= 1
            elif r_current < row_next and col_next > c_current:
                r_Count = 1
                c_Count = 1
                for r in range(r_current + 1, row_next):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count += 1
                    c_Count += 1
            elif r_current < row_next and c_current > col_next:
                r_Count = 1
                c_Count = -1
                for r in range(r_current + 1, row_next):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count += 1
                    c_Count -= 1

            return True


    # Rook
    elif game.board[r_current][c_current][1] == 'R':
        if r_current - row_next == 0:
            if c_current - col_next != 0:
                # Checks to make sure piece can't skip along the row
                if c_current > col_next:
                    oldC = col_next
                    newC = c_current
                else:
                    oldC = c_current
                    newC = col_next

                for n in range(oldC + 1, newC):

                    if game.board[r_current][n][0] == "b" or game.board[r_current][n][0] == "w":
                        return False
                return True
        elif c_current - col_next == 0:
            if r_current - row_next != 0:

                # Checks to make sure piece can't skip along the column
                if r_current > row_next:
                    oldR = row_next
                    newR = r_current
                else:
                    oldR = r_current
                    newR = row_next
                for n in range(oldR + 1, newR):
                    if game.board[n][c_current][0] == "b" or game.board[n][c_current][0] == "w":
                        return False
                return True

    # King
    elif game.board[r_current][c_current][1] == 'K':
        # It can only move one spaces
        if abs(r_current - row_next) <= 1 and abs(c_current - col_next) <= 1:
            if r_current != row_next or c_current != col_next:
                return True
                # if not validMoveKing((row_next,col_next), game.board, game.whiteTurn):
                # return True

    # Knight
    elif game.board[r_current][c_current][1] == 'N':
        if abs(r_current - row_next) == 2:
            if abs(c_current - col_next) == 1:
                return True
        elif abs(r_current - row_next) == 1:
            if abs(c_current - col_next) == 2:
                return True

    # Pawn
    elif game.board[r_current][c_current][1] == 'P':
        if game.board[r_current][c_current][0] != game.board[row_next][col_next][0] and game.board[row_next][
            col_next] != '  ':
            if game.board[r_current][c_current][0] == 'w':
                if r_current - row_next == 1 and abs(c_current - col_next) == 1:
                    return True
            else:
                if row_next - r_current == 1 and abs(c_current - col_next) == 1:
                    return True

        if c_current == col_next:
            if game.board[r_current][c_current][0] == 'w':
                if r_current == 6 and row_next == 4:
                    return True
                if r_current - row_next == 1 and c_current == col_next and game.board[row_next][col_next] == '  ':
                    return True
            if game.board[r_current][c_current][0] == 'b':
                if r_current == 1 and row_next == 3:
                    return True
                if row_next - r_current == 1 and c_current == col_next and game.board[row_next][col_next] == '  ':
                    return True

    # Queen
    elif game.board[r_current][c_current][1] == 'Q':
        if r_current - row_next == 0:
            if c_current - col_next != 0:

                # Checks if queen skips along a row
                if c_current > col_next:
                    oldC = col_next
                    newC = c_current
                else:
                    oldC = c_current
                    newC = col_next
                for n in range(oldC + 1, newC):
                    if game.board[r_current][n][0] == "b" or game.board[r_current][n][0] == "w":
                        return False
                return True
        elif c_current - col_next == 0:
            if r_current - row_next != 0:

                # Checks if queen can skip along column
                if r_current > row_next:
                    oldR = row_next
                    newR = r_current
                else:
                    oldR = r_current
                    newR = row_next
                for n in range(oldR + 1, newR):
                    if game.board[n][c_current][0] == "b" or game.board[n][c_current][0] == "w":
                        return False
                return True
        if abs(r_current - row_next) == abs(c_current - col_next) and (r_current - row_next != 0):

            # Checks if queen skips a space diagonally:
            if row_next < r_current and col_next > c_current:
                r_Count = -1
                c_Count = 1
                for r in range(row_next + 1, r_current):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count -= 1
                    c_Count += 1
            elif row_next < r_current and c_current > col_next:
                r_Count = -1
                c_Count = -1
                for r in range(row_next + 1, r_current):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count -= 1
                    c_Count -= 1
            elif r_current < row_next and col_next > c_current:
                r_Count = 1
                c_Count = 1
                for r in range(r_current + 1, row_next):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count += 1
                    c_Count += 1
            elif r_current < row_next and c_current > col_next:
                r_Count = 1
                c_Count = -1
                for r in range(r_current + 1, row_next):
                    if game.board[r_current + r_Count][c_current + c_Count][0] == "b" or \
                            game.board[r_current + r_Count][c_current + c_Count][0] == "w":
                        return False
                    r_Count += 1
                    c_Count -= 1
            return True

    # If selected, not possible to move
    return False


def check(boardgame, turn):
    """Checks to see if every move results in check, returns true if it is"""
    if turn == True:
        ally = 'w'
        enemy = 'b'
    else:
        ally = 'b'
        enemy = 'w'
    for r in range(8):
        for c in range(8):
            if boardgame[r][c] == ally + 'K':
                kingPosition = (r, c)
                print('king position:', kingPosition)
    for r in range(8):
        for c in range(8):
            if boardgame[r][c][0] == enemy:
                enemyPosition = (r, c)
                if validMoveKingCheck(kingPosition, enemyPosition):
                    print('Hes in check')
                    return True
    print('no check')
    return False


def validMove(currentPiece):
    for r in range(8):
        for c in range(8):
            if canMove(currentPiece[0], currentPiece[1], r, c):
                return True
    print('check came back false')
    return False


def validMoveKingCheck(kingPosition, enemyPosition):
    if canMove(enemyPosition[0], enemyPosition[1], kingPosition[0], kingPosition[1]):
        return True
    else:
        return False


def validMoveKing(kingPosition, boardGame, turn):
    if turn:
        enemy = 'b'
    else:
        enemy = 'w'

    for r in range(8):
        for c in range(8):
            if boardGame[r][c][0] == enemy:
                enemyPosition = (r, c)
                if not validMoveKingCheck((kingPosition), (enemyPosition)):
                    print('the king can move')
                    return False

    return True


def main():
    loadImages()
    createBoard()
    createPieces(screen, game.board)
    pieceGot = [False]
    running = True
    while running:

        for event in p.event.get():
            # Did the user click the window close button?
            if event.type == p.QUIT:
                running = False

            # Checks if user has clicked

            if event.type == p.MOUSEBUTTONDOWN:
                moveData = getPiece(game.whiteTurn, pieceGot)
                print('you picked a piece')
                movePiece(moveData[0], moveData[1])
                if game.whiteTurn == True:
                    game.whiteTurn = False
                else:
                    game.whiteTurn = True
                check(game.board, game.whiteTurn)
                updateBoard(game.board)

            p.display.update()

        # Update the entire display
        p.display.flip()

    p.quit()

main()