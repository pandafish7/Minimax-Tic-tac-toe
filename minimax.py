import pygame, sys#sys is only used to exit game
pygame.init()
screen = pygame.display.set_mode((300, 360))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.SysFont(None, 30)
#declare initially
board = [[None]*3 for _ in range(3)]#using a 2d array for the board
player = 'X'
game_over = False

def draw_board():
    screen.fill((0, 0, 0))
    for i in range(1, 3):
        pygame.draw.line(screen, (255, 255, 255), (0, i*100), (300, i*100), 2)#horizontal line
        pygame.draw.line(screen, (255, 255, 255), (i*100, 0), (i*100, 300), 2)#vertical line
    for row in range(3):#drawing x and o
        for col in range(3):
            x = col*100 + 50
            y = row*100 + 50
            if board[row][col] == 'X':
                pygame.draw.line(screen, (255, 255, 255), (x-25, y-25), (x+25, y+25), 4)
                pygame.draw.line(screen, (255, 255, 255), (x+25, y-25), (x-25, y+25), 4)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 30, 4)
    
    pygame.draw.rect(screen, (255, 255, 255), (100, 310, 100, 30))#rectangle for reset button
    text = font.render("RESET", True, (0, 0, 0))
    screen.blit(text, (125, 317))

    pygame.display.update()

def check_winner(player):
    for i in range(3):
        if board[i] == [player]*3: return True#checks vertically
        if board[0][i] == player and board[1][i] == player and board[2][i] == player: return True#checks horizontally
    if board[0][0] == player and board[1][1] == player and board[2][2] == player: return True#diagonal1
    if board[0][2] == player and board[1][1] == player and board[2][0] == player: return True#diagonal2
    return False

def is_board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def minimax(depth, is_maximizing):
    if check_winner('O'): return 1
    if check_winner('X'): return -1
    if is_board_full(): return 0
    
    if is_maximizing:#maximising bot score on bot turn
        max_eval = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = 'O'
                    eval = minimax(depth + 1, False)#human turn
                    board[r][c] = None#cleans up board after move stimulated
                    max_eval = max(max_eval, eval)#compares to previous scores
        return max_eval
    else:
        min_eval = float('inf')#minimising human score on human turn
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = 'X'
                    eval = minimax(depth + 1, True)
                    board[r][c] = None
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move():
    best_score = -float('inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                board[r][c] = 'O'
                score = minimax(0, False)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def bot_move():
    move = best_move()
    if move is not None:
        r, c = move
        board[r][c] = 'O'
        return check_winner('O')
    return False

def reset_game():
    global board, player, game_over
    board = [[None]*3 for _ in range(3)]
    player = 'X'
    game_over = False
    return board, player, game_over

draw_board()
while True:#infinite loop for game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()#user can quit game if window is closed
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 100 <= x <= 200 and 310 <= y <= 340:
                reset_game()
            elif not game_over and y < 300 and player == 'X':#mouse select = place x
                row = y // 100
                col = x // 100
                if board[row][col] is None:
                    board[row][col] = 'X'
                    if check_winner('X'): game_over = True
                    elif bot_move(): game_over = True
                    draw_board()
    draw_board()
