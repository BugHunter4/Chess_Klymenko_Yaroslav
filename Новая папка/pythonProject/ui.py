from datetime import datetime
import chess
import pygame
import os

def load_images(SQ_SIZE, IMAGES):
    pieces = ['wP', 'bP', 'wN', 'bN', 'wB', 'bB', 'wR', 'bR', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        path = os.path.join('images', f"{piece.lower()}.png")
        if not os.path.exists(path):
            print(f"File not found: {path}")
        else:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))

def display_text(screen, text, size, color, pos):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def button(screen, position, text, size, colors):
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, True, colors[0])
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), (x + w, y), 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    screen.blit(text_render, (x, y))
    return pygame.Rect(x, y, w, h)

def main_menu(screen, WIDTH, HEIGHT, COLORS, TIME_LIMITS):
    screen.fill(pygame.Color("white"))
    display_text(screen, "Chess Game", 48, pygame.Color('black'), (WIDTH//2 - 100, HEIGHT//2 - 250))

    btn_human = button(screen, (WIDTH//2 - 100, HEIGHT//2 - 150), "Play Human vs Human", 24, (255, 255, 255))
    btn_bot_white = button(screen, (WIDTH//2 - 100, HEIGHT//2 - 50), "Play as White vs Bot", 24, (255, 255, 255))
    btn_bot_black = button(screen, (WIDTH//2 - 100, HEIGHT//2), "Play as Black vs Bot", 24, (0, 0, 0))
    btn_15sec = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 50), "15 seconds", 24, (0, 0, 0))
    btn_1min = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 100), "1 minute", 24, (0, 0, 0))
    btn_1hour = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 150), "1 hour", 24, (0, 0, 0))
    btn_nolimit = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 200), "No limit", 24, (0, 0, 0))

    pygame.display.flip()

    choosing_options = True
    opponent = None
    player_color = COLORS['white']
    time_limit = TIME_LIMITS['No limit']

    while choosing_options:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if btn_human.collidepoint(pygame.mouse.get_pos()):
                    player_color = None  # Буде визначатися в грі
                    opponent = 'human'
                elif btn_bot_white.collidepoint(pygame.mouse.get_pos()):
                    player_color = COLORS['white']
                    opponent = 'bot'
                elif btn_bot_black.collidepoint(pygame.mouse.get_pos()):
                    player_color = COLORS['black']
                    opponent = 'bot'
                elif btn_15sec.collidepoint(pygame.mouse.get_pos()):
                    time_limit = TIME_LIMITS['15 seconds']
                elif btn_1min.collidepoint(pygame.mouse.get_pos()):
                    time_limit = TIME_LIMITS['1 minute']
                elif btn_1hour.collidepoint(pygame.mouse.get_pos()):
                    time_limit = TIME_LIMITS['1 hour']
                elif btn_nolimit.collidepoint(pygame.mouse.get_pos()):
                    time_limit = TIME_LIMITS['No limit']
                if opponent is not None:
                    choosing_options = False

    return player_color, opponent, time_limit

def game_over_menu(screen, result, winner, WIDTH, HEIGHT):
    screen.fill(pygame.Color("white"))
    display_text(screen, result, 48, pygame.Color('black'), (WIDTH//2 - 100, HEIGHT//2 - 200))
    display_text(screen, f"{winner} wins!", 36, pygame.Color('black'), (WIDTH//2 - 100, HEIGHT//2 - 150))

    btn_exit_game = button(screen, (WIDTH//2 - 100, HEIGHT//2 - 100), "Exit Game", 24, (255, 255, 255))
    btn_play_again = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 100), "Play Again", 24, (0, 0, 0))

    pygame.display.flip()

    choosing_option = True
    option = None

    while choosing_option:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if btn_exit_game.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
                elif btn_play_again.collidepoint(pygame.mouse.get_pos()):
                    option = "play_again"
                    choosing_option = False

    return option

def pause_menu(screen, WIDTH, HEIGHT):
    screen.fill(pygame.Color("white"))
    display_text(screen, "Paused", 48, pygame.Color('black'), (WIDTH//2 - 100, HEIGHT//2 - 200))

    btn_continue = button(screen, (WIDTH//2 - 100, HEIGHT//2 - 150), "Continue", 24, (0, 0, 0))
    btn_restart = button(screen, (WIDTH//2 - 100, HEIGHT//2 - 50), "Restart", 24, (0, 0, 0))
    btn_main_menu = button(screen, (WIDTH//2 - 100, HEIGHT//2 + 50), "Main Menu", 24, (0, 0, 0))

    pygame.display.flip()

    choosing_option = True
    option = None

    while choosing_option:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if btn_continue.collidepoint(pygame.mouse.get_pos()):
                    option = "continue"
                    choosing_option = False
                elif btn_restart.collidepoint(pygame.mouse.get_pos()):
                    option = "restart"
                    choosing_option = False
                elif btn_main_menu.collidepoint(pygame.mouse.get_pos()):
                    option = "main_menu"
                    choosing_option = False

    return option

def draw_game_state(screen, board, valid_moves, sq_selected, DIMENSION, SQ_SIZE, IMAGES):
    draw_board(screen, DIMENSION, SQ_SIZE)  # малювання квадратів на дошці
    highlight_squares(screen, board, valid_moves, sq_selected, SQ_SIZE)
    draw_pieces(screen, board, SQ_SIZE, IMAGES)  # малювання фігур на дошці

def draw_board(screen, DIMENSION, SQ_SIZE):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_squares(screen, board, valid_moves, sq_selected, SQ_SIZE):
    if sq_selected != ():
        r, c = sq_selected
        if board.color_at(chess.square(c, 7-r)) == (board.turn):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # прозорість
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.from_square == chess.square(c, 7-r):
                    screen.blit(s, ((move.to_square % 8)*SQ_SIZE, (7-(move.to_square // 8))*SQ_SIZE))

def draw_pieces(screen, board, SQ_SIZE, IMAGES):
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            piece_color = 'w' if piece.color == chess.WHITE else 'b'
            piece_image = f"{piece_color}{piece.symbol().upper()}"
            screen.blit(IMAGES[piece_image], pygame.Rect((sq % 8)*SQ_SIZE, (7-(sq // 8))*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_game_info(screen, start_time, move_count, game_over, time_limit, WIDTH, BOARD_SIZE, INFO_PANEL_HEIGHT):
    font = pygame.font.SysFont("Arial", 20)
    time_elapsed = (datetime.now() - start_time).seconds
    time_text = f"Time: {time_elapsed}s (Limit: {time_limit if time_limit else 'No limit'})"
    move_text = f"Moves: {move_count}"

    info_surface = pygame.Surface((WIDTH, INFO_PANEL_HEIGHT))
    info_surface.fill(pygame.Color("white"))
    info_surface.blit(font.render(time_text, True, pygame.Color('black')), (10, 20))
    info_surface.blit(font.render(move_text, True, pygame.Color('black')), (10, 50))

    screen.blit(info_surface, (0, BOARD_SIZE))
