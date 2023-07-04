import os
import random

import pygame

from button.button import Button
from utils.constants import *
from pygame.locals import *

from letter.letter import Letter
from plane.plane import Plane
from utils.helpers import scale_image

global SCORE, NEXT_LETTER, LIVES


# Link para generar audio en mp3 (parametro q="texto"):
# https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=es&q=
# Link para trabajar con audios:
# https://pythonprogramming.net/adding-sounds-music-pygame/

class Game:
    def __init__(self):
        global SCORE, NEXT_LETTER, LIVES

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("assets/sounds", "8bit-game-music-sound.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.plane_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "plane-sound.ogg"))
        self.search_letter_a_sound = pygame.mixer.Sound(os.path.join("assets/audio", "audio-buscar-la-letra-a.mp3"))
        self.search_letter_e_sound = pygame.mixer.Sound(os.path.join("assets/audio", "audio-buscar-la-letra-e.mp3"))
        self.search_letter_i_sound = pygame.mixer.Sound(os.path.join("assets/audio", "audio-buscar-la-letra-i.mp3"))
        self.search_letter_o_sound = pygame.mixer.Sound(os.path.join("assets/audio", "audio-buscar-la-letra-o.mp3"))
        self.search_letter_u_sound = pygame.mixer.Sound(os.path.join("assets/audio", "audio-buscar-la-letra-u.mp3"))
        self.success_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "success-sound.mp3"))
        self.error_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "error-sound.mp3"))
        self.game_start_sound = pygame.mixer.Sound(os.path.join("assets/sounds", "game-start-sound.mp3"))

        pygame.init()
        pygame.display.set_caption(TITLE)

        self.replay = True
        self.intro = True
        self.play = True
        self.gameover = True

        self.font = pygame.font.SysFont("Gaegu", 80)
        self.font2 = pygame.font.SysFont("Gaegu", 50)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg_scroll = 0
        self.bg = pygame.image.load('assets/images/bg.png').convert_alpha()

        self.numbers_images = []
        for i in range(10):
            number_image = pygame.image.load(f'assets/images/numeros/number{i}.png').convert_alpha()
            self.numbers_images.append(number_image)

        self.heart_images = []
        self.heart_image_index = 0
        for i in range(8):
            heart_image = pygame.image.load(f'assets/images/hearts/heart{i}.png').convert_alpha()
            heart_image = scale_image(heart_image, 30)
            self.heart_images.append(heart_image)

        self.gameover_image = pygame.image.load('assets/images/textGameOver.png').convert_alpha()

        self.ADDLETTER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDLETTER, 2000)

        SCORE = SCORE_INITIAL
        LIVES = LIVES_INITIAL
        NEXT_LETTER = random.choice(list(LETTERS_UPPER))

        while self.replay:
            self.replay = False
            self.menu()
            self.game_play()
            self.game_over()
            if not self.replay:
                break
            else:
                SCORE = SCORE_INITIAL
                LIVES = LIVES_INITIAL
                NEXT_LETTER = random.choice(list(LETTERS_UPPER))
                self.intro = True
                self.play = True
                self.gameover = True

        pygame.quit()

    def play_audio_letter(self, letter):
        if letter == "A":
            self.search_letter_a_sound.play()
        elif letter == "E":
            self.search_letter_e_sound.play()
        elif letter == "I":
            self.search_letter_i_sound.play()
        elif letter == "O":
            self.search_letter_o_sound.play()
        elif letter == "U":
            self.search_letter_u_sound.play()

    def draw_bg_image(self):
        self.screen.blit(self.bg, (0 - self.bg_scroll, 0))
        self.screen.blit(self.bg, (WIDTH - self.bg_scroll, 0))
        self.bg_scroll += 1
        if self.bg_scroll == WIDTH:
            self.bg_scroll = 0

    def show_score(self, score):
        num_digits = len(str(score))
        score_x = int(WIDTH / 2 - self.numbers_images[0].get_width() * num_digits / 2)
        for digit in str(score):
            number_image = self.numbers_images[int(digit)]
            self.screen.blit(number_image, (score_x, 30))
            score_x += number_image.get_width()

    def show_letter_to_capture(self):
        letter_image = pygame.image.load(LETTERS_UPPER[NEXT_LETTER]).convert_alpha()
        letter_image = scale_image(letter_image, 50)
        self.screen.blit(letter_image, (WIDTH - letter_image.get_width() - 20, 20))

    def show_lives_remaining(self, lives):
        for i in range(lives):
            heart_image = self.heart_images[int(self.heart_image_index)]
            heart_x = 30 + i * (heart_image.get_width() + 10)
            heart_y = 30
            self.screen.blit(heart_image, (heart_x, heart_y))
        self.heart_image_index += 0.1
        if self.heart_image_index >= len(self.heart_images):
            self.heart_image_index = 0

    def menu(self):
        self.draw_bg_image()

        prefijo = self.font2.render("Vamos a jugar", True, WHITE)
        prefijo_position = (
            WIDTH / 2 - prefijo.get_width() // 2,
            HEIGHT / 2 - prefijo.get_height() - 350 // 2
        )

        title = self.font.render("-= AviOn AtrApA VoCaLes =-", True, WHITE)
        title_position = (
            WIDTH / 2 - title.get_width() // 2,
            HEIGHT / 2 - title.get_height() - 120 // 2
        )

        buttons = pygame.sprite.Group()
        play_button = Button(500, 400, 'assets/images/play-button.png', self.play_button_click)
        buttons.add(play_button)

        while self.intro:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.intro = False
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    for entity in buttons:
                        entity.on_click(event)

            buttons.update()
            self.screen.fill(BLUE)

            self.screen.blit(title, title_position)
            self.screen.blit(prefijo, prefijo_position)

            for entity in buttons:
                self.screen.blit(entity.surface, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)

    def play_button_click(self):
        self.intro = False
        self.game_start_sound.play()

    def game_play(self):
        global SCORE, NEXT_LETTER, LIVES
        self.play_audio_letter(NEXT_LETTER)

        plane = Plane()
        self.plane_sound.play(loops=-1)
        self.plane_sound.set_volume(0.2)

        letters = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(plane)

        while self.play:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.play = False
                    exit()
                elif event.type == self.ADDLETTER:
                    new_letter = Letter()
                    letters.add(new_letter)
                    all_sprites.add(new_letter)

            if pygame.mouse.get_pressed()[0]:
                plane.fly_up()

            plane.update()
            letters.update()

            self.draw_bg_image()

            for entity in all_sprites:
                self.screen.blit(entity.image, entity.rect)

            for le in letters:
                if pygame.sprite.spritecollide(plane, letters, False, pygame.sprite.collide_mask):
                    if le.key == NEXT_LETTER:
                        self.success_sound.play()
                        SCORE += 1
                        NEXT_LETTER = random.choice(list(LETTERS_UPPER))
                        self.play_audio_letter(NEXT_LETTER)
                    else:
                        self.error_sound.play()
                        LIVES -= 1
                        if LIVES == 0:
                            self.play = False
                    le.kill()

            self.show_letter_to_capture()
            self.show_score(SCORE)
            self.show_lives_remaining(LIVES)

            pygame.display.flip()
            self.clock.tick(60)

    def game_over(self):
        buttons = pygame.sprite.Group()
        restart_button = Button(500, 300, 'assets/images/restart-button.png', self.restart_button_click)
        buttons.add(restart_button)
        self.plane_sound.stop()

        while self.gameover:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gameover = False
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    for entity in buttons:
                        entity.on_click(event)

            gameover_x = WIDTH / 2 - self.gameover_image.get_width() / 2
            gameover_y = HEIGHT / 2 - self.gameover_image.get_height() / 2 - 150
            self.screen.blit(self.gameover_image, (gameover_x, gameover_y))

            buttons.update()
            for entity in buttons:
                self.screen.blit(entity.surface, entity.rect)

            pygame.display.flip()

    def restart_button_click(self):
        self.gameover = False
        self.replay = True
        pygame.display.flip()


if __name__ == "__main__":
    g = Game()
