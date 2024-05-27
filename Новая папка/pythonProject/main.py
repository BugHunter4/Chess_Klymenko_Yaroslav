import pygame
from datetime import datetime
import chess
from ui import main_menu, game_over_menu, pause_menu, draw_game_state, draw_game_info, load_images
from game_logic import get_bot_move, save_game, load_game

# Ініціалізація Pygame
pygame.init()

# Константи
BOARD_SIZE = 640
INFO_PANEL_HEIGHT = 100
WIDTH, HEIGHT = BOARD_SIZE, BOARD_SIZE + INFO_PANEL_HEIGHT
DIMENSION = 8  # розмір шахової дошки 8x8
SQ_SIZE = BOARD_SIZE // DIMENSION
MAX_FPS = 15  # для анімації
IMAGES = {}
COLORS = {'white': 'w', 'black': 'b'}
TIME_LIMITS = {'15 seconds': 15, '1 minute': 60, '1 hour': 3600, 'No limit': None}

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    load_images(SQ_SIZE, IMAGES)

    running = True

    while running:
        player_color, opponent, time_limit = main_menu(screen, WIDTH, HEIGHT, COLORS, TIME_LIMITS)

        gs = chess.Board()
        sq_selected = ()  # відстеження вибраного квадрата (рядок, стовпець)
        player_clicks = []  # відстеження кліків користувача (дві кліки для ходу)
        move_made = False  # прапорець для руху
        valid_moves = list(gs.legal_moves)
        game_time = datetime.now()  # Відстеження часу гри
        move_count = 0  # Лічильник ходів
        game_over = False
        move_start_time = datetime.now()

        result = ""
        winner = ""

        while not game_over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    game_over = True
                    pygame.quit()
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        option = pause_menu(screen, WIDTH, HEIGHT)
                        if option == "restart":
                            gs = chess.Board()
                            sq_selected = ()
                            player_clicks = []
                            move_made = False
                            valid_moves = list(gs.legal_moves)
                            game_time = datetime.now()
                            move_count = 0
                            move_start_time = datetime.now()
                        elif option == "continue":
                            continue
                        elif option == "main_menu":
                            game_over = True
                            break

                elif e.type == pygame.MOUSEBUTTONDOWN and not game_over and (opponent == 'human' or (opponent == 'bot' and gs.turn == (player_color == COLORS['white']))):
                    location = pygame.mouse.get_pos()  # x,y позиції миші
                    if location[1] < BOARD_SIZE:  # Ігноруємо кліки в інформаційній панелі
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sq_selected == (row, col):  # якщо користувач натискає ту ж саму квадрату двічі
                            sq_selected = ()  # скидання вибору
                            player_clicks = []  # скидання кліків
                        else:
                            sq_selected = (row, col)
                            player_clicks.append(sq_selected)  # додавання для першого і другого кліку
                        if len(player_clicks) == 2:  # після другого кліку
                            move = chess.Move.from_uci(f"{chr(player_clicks[0][1] + 97)}{8 - player_clicks[0][0]}{chr(player_clicks[1][1] + 97)}{8 - player_clicks[1][0]}")
                            if move in valid_moves:
                                gs.push(move)
                                move_made = True
                                sq_selected = ()  # скидання вибору
                                player_clicks = []  # скидання кліків
                                move_count += 1
                                move_start_time = datetime.now()  # Скинути час після кожного ходу
                            else:
                                player_clicks = [sq_selected]

            if opponent == 'bot' and gs.turn != (player_color == COLORS['white']) and not game_over:
                bot_move = get_bot_move(gs)
                gs.push(bot_move)
                move_made = True
                move_start_time = datetime.now()

            if move_made:
                valid_moves = list(gs.legal_moves)
                move_made = False

            if gs.is_checkmate():
                game_over = True
                result = "Checkmate!"
                winner = "White" if gs.turn == chess.BLACK else "Black"
            elif gs.is_stalemate() or gs.is_insufficient_material() or gs.is_seventyfive_moves() or gs.is_fivefold_repetition():
                game_over = True
                result = "Draw!"
                winner = "No one"
            elif time_limit is not None and (datetime.now() - move_start_time).seconds >= time_limit:
                game_over = True
                result = "Time's up!"
                winner = "White" if gs.turn == chess.BLACK else "Black"

            draw_game_state(screen, gs, valid_moves, sq_selected, DIMENSION, SQ_SIZE, IMAGES)
            draw_game_info(screen, game_time, move_count, game_over, time_limit, WIDTH, BOARD_SIZE, INFO_PANEL_HEIGHT)

            clock.tick(MAX_FPS)
            pygame.display.flip()

        if not running:
            continue  # Повернення до головного меню

        option = game_over_menu(screen, result, winner, WIDTH, HEIGHT)

        if option == "play_again":
            continue  # Повернення до головного меню
        elif option == "exit_game":
            running = False

if __name__ == "__main__":
    main()
