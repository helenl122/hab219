import pygame
import math
import player
import obstacle
from random import randint
from sys import exit
import asyncio

class Game():
    async def run(self):
        def display_score():
            global curr_time
            curr_time = int(pygame.time.get_ticks()/18) - start_time
            score_surf = font.render(f'Puntos: {curr_time}', False, 'Black')
            score_rect = score_surf.get_rect(center = (400,50))
            pygame.draw.rect(screen, 'White', score_rect)
            screen.blit(score_surf, score_rect)

        def collision():
            if pygame.sprite.spritecollide(man.sprite, obstacle_group, True):
                obstacle_group.empty()
                return False
            return True

        pygame.init()

        width = 800
        height = 400
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Habitación 219')
        clock = pygame.time.Clock()
        font = pygame.font.Font('font/Pixeltype.ttf', 30)
        game_active = False
        start_time = 0

        # intro screen surfaces & vars
        door_surf = pygame.image.load('graphics/door.jpg').convert_alpha()
        door_surf = pygame.transform.rotozoom(door_surf, 0, 0.25)
        door_rect = door_surf.get_rect(center = (400,200))

        # background surfaces & vars
        bgm = pygame.mixer.Sound('audio/retroGame.wav')
        bgm.play(loops = -1)
        bgm.set_volume(0.75)
        carpet_surf = pygame.image.load('graphics/carpet2.png').convert()
        hallway_surf = pygame.image.load('graphics/hallway.png').convert()
        windows_surf = pygame.image.load('graphics/windows.png').convert()
        carpet_width = carpet_surf.get_width()
        hallway_width = hallway_surf.get_width()
        windows_width = windows_surf.get_width()
        scroll = 0
        tiles = math.ceil(width / hallway_width) + 1

        # sprite surfaces & vars
        man = pygame.sprite.GroupSingle()
        man.add(player.Player())
        obstacle_group = pygame.sprite.Group()

        # timer
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer, 1500)

        # Runs the game window
        while True:
            for event in pygame.event.get():
                # to close out window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # when space is pressed, activate game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/18)
                # add new obstacle to obstacle group every timer time increment (and game is active)
                if event.type == obstacle_timer and game_active:
                    obstacle_group.add(obstacle.Obstacle())

            if game_active:
                # draw scrolling background
                for i in range(0,tiles):
                    screen.blit(hallway_surf, (i*hallway_width + scroll,0))
                    screen.blit(carpet_surf, (i*carpet_width + scroll,116))
                    screen.blit(windows_surf, (i*carpet_width + scroll,284))
                # scroll background
                scroll -= 1
                # reset scroll
                if abs(scroll) > hallway_width:
                    scroll = 0
                # Display text score
                display_score()

                # player & obstacle movements
                man.draw(screen)
                man.update()
                obstacle_group.draw(screen)
                obstacle_group.update()     

                # collision detection
                game_active = collision()

            else:
                # game over screen
                screen.fill((116, 127, 166))
                screen.blit(door_surf, door_rect)
                # text surfs & vars
                if (start_time == 0):
                    # instruction screen
                    instr_surf = font.render('Pulse \'ESPACIO\' para empezar', False, 'Black')
                    instr_rect = instr_surf.get_rect(center = (400,350))
                    pygame.draw.rect(screen, 'White', instr_rect)
                    screen.blit(instr_surf, instr_rect)
                else:
                    # user score screen
                    score_surf = font.render(f'Puntos: {curr_time}', False, 'Black')
                    score_rect = score_surf.get_rect(center = (400,350))
                    pygame.draw.rect(screen, 'White', score_rect)
                    screen.blit(score_surf, score_rect)
                # render the 219 room label
                title_surf = font.render('219', False, 'Black')
                title_rect = title_surf.get_rect(center = (400,180))
                pygame.draw.rect(screen, 'White', title_rect)
                screen.blit(title_surf, title_rect)
                # render the game title label
                header_surf = font.render('Habitacion 219', False, 'Black')
                header_surf = pygame.transform.rotozoom(header_surf, 0, 2)
                header_rect = header_surf.get_rect(center = (400,50))
                pygame.draw.rect(screen, 'White', header_rect)
                screen.blit(header_surf, header_rect)
                
            # draw all elements, update everything
            pygame.display.update()
            clock.tick(60) # ceil = 60fps
            await asyncio.sleep(0)

if __name__ == '__main__':
    app = Game()
    asyncio.run(app.run())