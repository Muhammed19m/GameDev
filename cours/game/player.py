import pygame
from button import shop_png as items
import time
class Player:
    font = pygame.font.Font(None, 24)
    def __init__(self, name: str, first_cord: tuple, inventory=[], HP=100, pos="stop"):
        self.x, self.y = first_cord
        name.title()
        self.name = name
        self.image = pos
        self.hp = HP
        self.timer = 0
        self.inventory = inventory
        self.jump = False
        self.jump_velocity = 15
        self.down = False
        self.bullet = []
        self.del_ind = []

    def render(self, window, player_images):
        window.blit(player_images[self.image], [self.x, self.y])
        for name in self.inventory:
            if name == 'helmet':
                cord = (self.x+50-10, self.y-2)
                window.blit(items[name], cord)
            elif name == 'armor':
                cord = (self.x+50-13, self.y+25)
                window.blit(items[name], cord)
            elif name == 'short':
                cord = (self.x+50-13, self.y+52)
                window.blit(items[name], cord)
            elif name == 'boot':
                if self.image=='stop':
                    window.blit(items[name], (self.x+27, self.y+93))
                    window.blit(items[name], (self.x+57, self.y+93))
                elif self.image == 'goL1':
                    window.blit(items[name], (self.x + 15, self.y + 80))
                    window.blit(items[name], (self.x + 57, self.y + 93))
                elif self.image == 'goL2':
                    window.blit(items[name], (self.x + 27, self.y + 93))
                    window.blit(items[name], (self.x + 57, self.y + 93))
                elif self.image == 'goR1':
                    window.blit(items[name], (self.x + 40, self.y + 93))
                    window.blit(items[name], (self.x + 72, self.y + 82))
                elif self.image == 'goR2':
                    window.blit(items[name], (self.x + 47, self.y + 80))
                    window.blit(items[name], (self.x + 60, self.y + 93))
                elif self.image == 'wL':
                    window.blit(items[name], (self.x + 28, self.y + 93))
                    window.blit(items[name], (self.x + 47, self.y + 93))
                elif self.image == 'wR':
                    window.blit(items[name], (self.x + 38, self.y + 93))
                    window.blit(items[name], (self.x + 57, self.y + 93))

    def move(self, keys, press_mouse, pos, window, weapons, SIZE_MAP, player_rect, block_rect, stolbs_rect, bull,ti):
        speed = 3
        t = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and not self.jump and self.down == False:
            self.jump = True
        if self.jump:
            self.y -= self.jump_velocity
            player_rect.x, player_rect.y = self.x+20, self.y
            if player_rect.collidelistall(block_rect) or player_rect.collidelistall(stolbs_rect):
                self.y += self.jump_velocity
                self.jump = False
                self.jump_velocity = 15
            self.jump_velocity -= 0.5
            if self.jump_velocity <= 0:
                self.jump = False
                self.jump_velocity = 15


        if keys[pygame.K_a] and self.x > 0:
            self.x -= 1*speed
            player_rect.x -= 1*speed
            if player_rect.collidelistall(block_rect) or player_rect.collidelistall(stolbs_rect):
                self.x+=1*speed

            if self.timer < 15:
                self.image = 'goL1'
            else:
                self.image = 'goL2'
                if self.timer == 30: self.timer = 0
            self.timer += 1
            t*=0
            player_rect.x, player_rect.y = self.x+20, self.y

        if keys[pygame.K_d] and self.x < SIZE_MAP[0]-100:
            self.x += 1*speed
            player_rect.x += 1*speed

            if player_rect.collidelistall(block_rect) or player_rect.collidelistall(stolbs_rect):
                self.x -=1*speed

            if self.timer < 15: self.image = 'goR1'
            else:
                self.image = 'goR2'
                if self.timer == 30: self.timer = 0
            self.timer += 1
            t*=0
            player_rect.x, player_rect.y = self.x+20, self.y

        if self.y < SIZE_MAP[1] - 100 - 40 and not self.jump:# and not player_rect.collidelistall(stolbs_rect) and not player_rect.collidelistall(block_rect):
            self.y += 4
            player_rect.x, player_rect.y = self.x+20, self.y

            if player_rect.collidelistall(stolbs_rect) or player_rect.collidelistall(block_rect):
                player_rect.x, player_rect.y = self.x + 20, self.y
                self.y -= 4
                self.down = False
            else: self.down = True

            player_rect.x, player_rect.y = self.x+20, self.y
        else: self.down = False

        if t: self.image = 'stop'
        if press_mouse[2]:
            if pos[0] > self.x:
                self.image = 'wR'
                window.blit(weapons['m1R'], (self.x+50, self.y+25))
                if press_mouse[0] and ti%40==0:
                    self.bullet.append((pygame.rect.Rect(self.x+30, self.y+20, 10, 10), 'r'))
            else:
                self.image = 'wL'

                window.blit(weapons['m1L'], (self.x+9, self.y+25))
                if press_mouse[0] and ti%40==0:
                    self.bullet.append((pygame.rect.Rect(self.x, self.y+20, 10, 10), 'l'))
        for bul in range(len(self.bullet)):
            if self.bullet[bul][0].x>SIZE_MAP[0] or self.bullet[bul][0].x <0:
                self.del_ind.append(bul)
            if self.bullet[bul][0].collidelistall(block_rect) or self.bullet[bul][0].collidelistall(stolbs_rect):
                self.del_ind.append(bul)
            else:
                if self.bullet[bul][1]=='r':    self.bullet[bul][0].x+=4
                else: self.bullet[bul][0].x-=4
                window.blit(bull, self.bullet[bul][0])
        for ind in self.del_ind:
            self.bullet.pop(ind)
        self.del_ind.clear()
        bullet = [[i[0].x, i[0].y] for i in self.bullet]

    def cursor(self, position_mouse, window):
        if position_mouse[0] > self.x and position_mouse[0] < self.x + 100:
            if position_mouse[1] > self.y and position_mouse[1] < self.y + 100:
                self.render_name(window)

    def render_name(self, window):
        window.blit(Player.font.render(self.name, 1, (0, 153, 51)), (self.x+15, self.y-25))






