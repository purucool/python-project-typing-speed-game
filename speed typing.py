import pygame
from pygame import mixer
from pygame.locals import *
import sys
import time
import random

class App:
    def __init__(self):
        self.width = 1280
        self.height = 800
        self.active = False
        self.reset = True
        self.inputText = ''
        self.word = ''
        self.startTime = 0
        self.totalTime = 0
        self.accuracy = '0%'
        self.wpm = 0
        self.end = False
        self.result = 'Time: 0 | Accuracy: 0% | WPM: 0'
        self.primary = (29, 161, 242)
        self.secondary = (0, 0, 0)

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Speed Typing Test')
        pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))

        self.img = pygame.image.load('assets/images/loading screen.png')
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        self.bg = pygame.image.load('assets/images/background.png')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

    def text(self, screen, header, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(header, 1, color)
        text_rect = text.get_rect(center=(self.width / 2, y))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def sentence(self):
        f = open('assets/text files/sentences.txt').read()
        s = f.split('\n')
        s = random.choice(s)
        return s

    def show_result(self, screen):
        if (not self.end):
            self.totalTime = time.time() - self.startTime

            count = 0
            for i, j in enumerate(self.word):
                try:
                    if self.inputText[i] == j:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            self.wpm = len(self.inputText) * 60 / (5 * self.totalTime)
            self.end = True
            print('Total time taken: ' + str(round(self.totalTime, 2)) + 's\n')

            self.result = 'Time: ' + str((round(self.totalTime, 2))) + 's | Accuracy: ' + str(
                round(self.accuracy)) + '% | WPM: ' + str(round(self.wpm))

            self.time_img = pygame.image.load('assets/images/reset.png')
            self.time_img = pygame.transform.scale(self.time_img, (156, 56))

            self.screen.blit(self.time_img, (self.width / 2 - 75, self.height - 140))
            self.text(screen, 'Reset', self.height - 110, 26, (240, 240, 240))

            print(self.result)
            pygame.display.update()

    def run(self):
        self.resetApp()

        self.running = True
        while (self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (160, 360, 950, 50))
            pygame.draw.rect(self.screen, self.primary, (160, 360, 950, 50), 2)
            self.text(self.screen, self.inputText, 385, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    print('\n!!! THANKS FOR USING !!!')
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if (x >= 160 and x <= 950 and y >= 360 and y <= 410):
                        self.active = True
                        self.inputText = ''
                        self.startTime = time.time()
                    if (x >= 565 and x <= 721 and y >= 660 and self.end):
                        self.resetApp()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print('\nRESULTS:')
                            print('Input sentence: ', self.inputText)
                            self.show_result(self.result)
                            self.text(self.screen, self.result, 620, 28, self.secondary)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            stroke_sound = mixer.Sound('assets/sound/keystroke.wav')
                            stroke_sound.play()
                            self.inputText = self.inputText[:-1]
                        else:
                            try:
                                stroke_sound = mixer.Sound('assets/sound/keystroke.wav')
                                stroke_sound.play()
                                self.inputText += event.unicode
                            except:
                                pass
            pygame.display.update()
        clock.tick(60)
    def resetApp(self):
        self.screen.blit(self.img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.inputText = 'Click here to start...'
        self.word = ''
        self.startTime = 0
        self.totalTime = 0
        self.wpm = 0
        self.word = self.sentence()
        if (not self.word): self.resetApp()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        header = 'Speed Typing Test'
        self.text(self.screen, header, 100, 80, self.primary)
        pygame.draw.rect(self.screen, self.primary, (160, 360, 950, 50), 2)
        self.text(self.screen, self.word, 320, 28, self.secondary)
        pygame.display.update()
App().run()