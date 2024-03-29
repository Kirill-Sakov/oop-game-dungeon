import pygame
import os
import Objects
from ScreenEngine import GameSurface, ProgressBar, InfoWindow, HelpWindow, ScreenHandle
import Logic
import Service


SCREEN_DIM = (820, 820)
SPRITE_SIZE = 20

pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("MyRPG")
KEYBOARD_CONTROL = True

if not KEYBOARD_CONTROL:
    import numpy as np
    answer = np.zeros(4, dtype=float)

base_stats = {
    "strength": 20,
    "endurance": 20,
    "intelligence": 5,
    "luck": 5
}


def create_game(sprite_size, is_new):
    global hero, engine, drawer, iteration
    path = os.path.join("texture", "Hero.png")
    sprite = Service.create_sprite(path, sprite_size)
    if is_new:
        hero = Objects.Hero(base_stats, sprite)
        engine = Logic.GameEngine()
        engine.step = sprite_size
        Service.service_init(sprite_size)
        Service.reload_game(engine, hero)
        help_window = HelpWindow((700, 500), pygame.SRCALPHA, (0, 0), ScreenHandle((0, 0)))
        info_window = InfoWindow((160, 600), (50, 50), help_window)
        progress_bar = ProgressBar((640, 120), (640, 0), info_window)
        drawer = GameSurface(SCREEN_DIM, pygame.SRCALPHA, (0, 480), progress_bar)

    else:
        engine.sprite_size = sprite_size
        hero.sprite = sprite
        Service.service_init(sprite_size, False)

    Logic.GameEngine.sprite_size = sprite_size

    drawer.connect_engine(engine)

    iteration = 0


create_game(SPRITE_SIZE, True)


while engine.working:

    if KEYBOARD_CONTROL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    engine.show_help = not engine.show_help
                if event.key == pygame.K_KP_PLUS:
                    size = size + 1
                    create_game(size, False)
                if event.key == pygame.K_KP_MINUS:
                    size = size - 1
                    create_game(size, False)
                if event.key == pygame.K_r:
                    create_game(size, True)
                if event.key == pygame.K_ESCAPE:
                    engine.working = False
                if engine.game_process:
                    if event.key == pygame.K_UP:
                        engine.move_up()
                        iteration += 1
                    elif event.key == pygame.K_DOWN:
                        engine.move_down()
                        iteration += 1
                    elif event.key == pygame.K_LEFT:
                        engine.move_left()
                        iteration += 1
                    elif event.key == pygame.K_RIGHT:
                        engine.move_right()
                        iteration += 1
                else:
                    if event.key == pygame.K_RETURN:
                        create_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
        if engine.game_process:
            actions = [
                engine.move_right,
                engine.move_left,
                engine.move_up,
                engine.move_down,
            ]
            answer = np.random.randint(0, 100, 4)
            prev_score = engine.score
            move = actions[np.argmax(answer)]()
            state = pygame.surfarray.array3d(gameDisplay)
            reward = engine.score - prev_score
            print(reward)
        else:
            create_game()

    gameDisplay.blit(drawer, (0, 0))
    drawer.draw(gameDisplay)

    pygame.display.update()

pygame.display.quit()
pygame.quit()
exit(0)
