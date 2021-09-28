import pygame
import time
from sys import exit as exit_from_sys
from button import Button, ImageButton
from player import Player
pygame.init()

class Inventory:
    def __init__(self, SIZE, players_images, inventory):
        self.inventory = inventory
        self.player_images = players_images
        self.SIZE = SIZE
        self.put_on = []
        self.player = Player('Muhammed', (SIZE[0]//2-50, SIZE[1]//2), self.put_on)

        self.colors = {}
        self.cells = []



    def start(self, window, inventory):
        self.inventory = inventory
        print(inventory)
        print(self.colors)
        print(self.put_on)
        print(self.cells)

        exit = Button((self.SIZE[0]//2-100, self.SIZE[1]//2+200, 200, 100), (255, 153, 51), 'Exit', 48, width_text=45)

        tim = time.time()


        x, y = 50, 200
        for i in self.inventory.items():
            self.cells.append(ImageButton(i[1], (x, y), text=i[0], color=self.colors.get(i[0], (255, 255, 255))))
            x += 125
            if x > self.SIZE[0] - 150:
                x, y = 50, y + 130

        while True:
            keys = pygame.key.get_pressed()
            poss = pygame.mouse.get_pos()
            press = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_from_sys()
            window.fill((51, 51, 153))

            self.player.render(window, self.player_images)
            exit.render()
            if exit.press(poss, press) and time.time()-tim>0.3: return self.put_on
            if keys[pygame.K_ESCAPE]: return self.put_on

            for i in self.cells:
                i.render()
                if i.press(poss, press) and i.text not in self.put_on:
                    self.put_on.append(i.text)# = i.image
                    i.__init__(i.image, (i.cord_x, i.cord_y), i.price, i.text, i.size, (51, 204, 51))
                    self.colors[i.text] = (51, 204, 51)
                if i.press(poss, press, 2) and i.text in self.put_on:
                    i.__init__(i.image, (i.cord_x, i.cord_y), i.price, i.text, i.size, (255,255,255))
                    self.put_on.pop(self.put_on.index(i.text))
                    self.colors.pop(i.text)





            pygame.display.update()
