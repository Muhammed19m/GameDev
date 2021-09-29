import pygame
import time
import os
import json
import pyautogui
import button
from button import ImageButton, Button, globalization, TextBox, Text, Top, Money, Market
from autorization import Reg, ConfigGame
from inventory import Inventory
from player import Player

import client

pygame.init()
pygame.font.init()


# -----------------ОКНО-----------------
width, height = pyautogui.size().width, pyautogui.size().height
SIZE = (width, height)
window = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Cyber cringe 2D city")

display = pygame.Surface(SIZE)
button.SIZE = SIZE
globalization(window)


# ______________________________________

player_images = {"stop": pygame.image.load("images\player\stop.png"), "goL1": pygame.image.load("images\player\goL1.png"), "goL2": pygame.image.load("images\player\goL2.png"), "goR1": pygame.image.load("images\player\goR1.png"), "goR2": pygame.image.load("images\player\goR2.png"), "wR": pygame.image.load('images\player\wR.png'), "wL": pygame.image.load('images\player\wL.png'), "dead": pygame.image.load("images\player\dead.png")}
weapons = {'m1L': pygame.image.load('images\weapon\m1L.png'), 'm1R': pygame.image.load('images\weapon\m1R.png')}

profile_photo = os.listdir("images\profile")
if profile_photo:
    profile_photo = pygame.image.load('images\profile\\' + os.listdir("images\profile")[0])
else:
    profile_photo = pygame.Surface((100, 100))
    profile_photo.fill((255,255,255))

glass = pygame.image.load("images\\block\glass.png")
platform_glass = pygame.image.load("images\\block\platform_glass.png")
platform_stone = pygame.image.load("images\\block\platform_stone.png")
stolb = pygame.image.load("images\\block\stolb.png")
rope = pygame.image.load("images\\block\\rope.png")


file = open('data\data.json', mode='r')
data = json.load(file)
SIZE_MAP = (1600, 900)

bullet = pygame.image.load("images\\additional\\bul.png")

game_over = pygame.image.load("images\\additional\game over.png")






class Menu:
    def __init__(self):
        self.buttons = \
        [
            [(20, SIZE[1]-220, 300, 200), (255, 153, 51), (SIZE[0]+30, SIZE[1]-55), 'Играть', 48, 65],
            [(SIZE[0]-320, SIZE[1]-220, 300, 200), (255, 153, 51), (), 'Выйти', 48, 65],
            [(20, SIZE[1]-340, 300, 100), (194, 194, 163), (SIZE[0]+30, SIZE[1]-55), 'Настройки', 32, 50],
            [(SIZE[0]/2-150, SIZE[1] - 250, 300, 100), (255, 153, 51), (SIZE[0] + 30, SIZE[1] - 55), 'Маркет', 32, 90],
            [(SIZE[0] / 2 - 150, SIZE[1] - 370, 300, 100), (255, 153, 51), (SIZE[0] + 30, SIZE[1] - 55), 'Инвентарь', 32, 65]
        ]
        self.buttons_ready = [Button(but[0], but[1], but[3], but[4], width_text=but[5]) for but in self.buttons]

        self.prof = ImageButton(profile_photo, (20, 20), size=(200, 200))
        #self.name_profile = Text('Player', (20, 230), 40)
        self.enter_name = False
        self.moneys = 0
        self.coins = 0
        self.market = Market(self.moneys)

        self.reg = Reg(height, width)

        self.inventory = {}
        self.inventory_m = Inventory(SIZE, player_images, self.inventory)
        self.put_on = []
        self.name = "Player"
        self.count_players = "2"
        self.ip = '127.0.0.1'
        self.port = "7978"
        self.data = None
    def start(self):

        players = {'Player1': 0,
                   'Player2': 0,
                   'Player3': 0,
                   'Player4': 0,
                   'Player5': 0,
                   'Player6': 0,
                   'Player7': 0,
                   'Player8': 0,
                   'Player9': 0,
                   'Player10': 0,
                   }
        top = Top((SIZE[0]-340, 20), (320, 550), players)
        reg_button = Button((20, 240, 200, 80), (255, 153, 51), 'Сохранить', 24, width_text=25)

        tim = time.time()
        player = Player("D", (SIZE[0]/2-32, SIZE[1]/2-32), self.put_on)

        config_game = ConfigGame(height, width)

        while True:
            if self.data != None:
                js = json.loads(self.data)
                self.moneys = int(js['money'])
                self.market.moneys = self.moneys
                self.coins = js['coins']
                self.data = None
            position_mouse = pygame.mouse.get_pos()
            press_mouse = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            window.fill((119, 51, 255))

            Money((SIZE[0]/2-200, 0), self.moneys).render()


            for button in self.buttons_ready:
                if button.name_button('Играть') and button.press(position_mouse, press_mouse):
                    self.enter_name = False
                    if self.name!="" and (self.count_players.isdigit()):
                        if int(self.count_players) in [1, 2, 3,4,5]:
                            mon, con = game.start(self.name, self.put_on, self.count_players, self.ip, int(self.port))
                            self.moneys += mon
                            self.coins += con
                elif button.name_button("Настройки") and button.press(position_mouse, press_mouse):
                    self.count_players, self.name, self.ip, self.port = config_game.start(window)
                elif button.name_button('Выйти', 'Нее...') and button.press(position_mouse, press_mouse):
                    pygame.quit()
                    exit()



            if self.buttons_ready[1].cursor(position_mouse):
                self.buttons_ready[1].replace_text('Нее...')
            else: self.buttons_ready[1].replace_text('Выйти')


            #---------profile---------
            window.blit(*self.prof())
            #self.name_profile.render()
            #if self.name_profile.press(position_mouse, press_mouse) or self.enter_name:
            #    self.enter_name = True
            #if self.enter_name:
            #    if self.name_profile.input():
            #        self.enter_name = False
            #        I[0] = self.name_profile.text
            reg_button.render()
            if reg_button.press(position_mouse, press_mouse):
                self.data = self.reg.start(window, self.ip, self.port, self.name, self.moneys, self.coins)
                tim = time.time()




            #-------------------------

            player.render(window, player_images, weapons)
            #----------TOP------------
            top.render(players)
            top.press(position_mouse, press_mouse, self.ip, self.port)
            #-------------------------


            if self.buttons_ready[3].press(position_mouse, press_mouse) and time.time()-tim > 0.3:
                self.inventory, self.moneys = self.market.start()
                tim = time.time()

            if self.buttons_ready[4].press(position_mouse, press_mouse) and time.time()-tim > 0.3:
                self.put_on = self.inventory_m.start(window, self.inventory)
                player.inventory = self.put_on

                tim = time.time()



            if self.prof.press(position_mouse, press_mouse):
                pass
            [button.render() for button in self.buttons_ready]



            pygame.display.update()










scroll = [0, 0]

class Game:
    def __init__(self):

        self.FPS = pygame.time.Clock()



    def start(self, name, put_on, count_players, ip, port):#, players={'Muhammed': {self.player.x}}):
        self.player = Player(name, (100, 100), inventory=put_on)
        #self.player.name = name
        players = {}
        print(f'-{count_players}-')
        try:
            client.main(count_players=count_players, ip=ip, port=port)
        except:
            return
        iteration = 0


        names_inventory_items = '['
        for i in put_on:
            names_inventory_items = names_inventory_items+f'"{i}"'+","
        names_inventory_items = names_inventory_items[:-1]+"]"
        if len(names_inventory_items)<3:
            names_inventory_items = "[]"

        cords_blocks = [(1500, 700), (1350, 550), (1500, 350), (0, 450), (0, 200), (1300, 150), (1400, 150), (200, 650), (300, 650), (700, 500), (800, 500), (900, 500), (1000, 500), (400, 200), (500, 200), (600, 200), (700, 200), (800, 200), (900, 200), (280, 350  )]
        blocks = [pygame.rect.Rect(x, y, 100, 40) for x, y in cords_blocks]
        del cords_blocks
        old_cord = [self.player.x, self.player.y]

        stolbs = [pygame.rect.Rect(1300, 190, 40, 100), pygame.rect.Rect(1300, 290, 40, 100)]
        player_rect = pygame.rect.Rect(self.player.x + 20, self.player.y, 50, 100)
        players_rect = [[pygame.rect.Rect(0,0,50, 100), 'name'] for i in range(int(count_players))]
        timer = 0
        bullets = 50
        player_hit = ""
        bullets_fly = []
        count_players = int(count_players)
        game_over_timer = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            window.fill((255, 255, 255))
            timer += 1

            for i in range(16):
                window.blit(glass, (100*i, 900-40))

            for block_rect in blocks:
                window.blit(platform_stone, block_rect)
            #if player_rect.collidelistall(blocks) or player_rect.collidelistall(stolbs):
            #    self.player.x, self.player.y = old_cord


            window.blit(stolb, stolbs[0])
            window.blit(stolb, stolbs[1])
            window.blit(rope, (220, 0))
            window.blit(rope, (220, 200))
            window.blit(rope, (1300, 390))
            window.blit(rope, (1300, 590))


            my_json_for_server = f'"Name": "{self.player.name}", ' \
                f'"cord": {[self.player.x, self.player.y]},' \
                f'"hp": {self.player.hp},' \
                f'"inventory": {names_inventory_items},' \
                f'"bullets": {bullets_fly},' \
                f'"hit": "{player_hit}",' \
                f'"pos": "{self.player.image}"'

          #  print(my_json_for_server)
            my_json_for_server = "{"+my_json_for_server+"}"

            client.send(my_json_for_server.encode("utf-8"))

            mes_from_server = client.get_mes()
            if type(mes_from_server) == int:
                if mes_from_server == 0: break
            try:
                json_from_server = json.loads(mes_from_server)  # here error
            except:
                continue
            #print(mes_from_server)


            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            press_mouse = pygame.mouse.get_pressed()



            if self.player.hp <= 0:
                self.player.image = "dead"
                window.blit(player_images[self.player.image], [self.player.x, self.player.y])
            else:
                bullets_fly, player_hit = self.player.move(keys, press_mouse, mouse_pos, window, weapons, SIZE_MAP, player_rect, blocks, stolbs, bullet, timer, players)
                self.player.render(window, player_images,weapons)



            iter_player = 0
            for user in json.loads(mes_from_server):
                if iteration >= 5 and user["Name"]!=self.player.name:
                    if user["hit"] == self.player.name:

                        self.player.hp -= 20
                        if self.player.hp == 0:
                            count_players -= 1
                    if iteration == 5:

                        players[user["Name"]]=[Player(user["Name"], user["cord"], user["inventory"], user["hp"], user["pos"]), pygame.rect.Rect(user["cord"][0], user["cord"][1], 50, 100)]
                    for bu in user["bullets"]:
                        window.blit(bullet, (bu[0], bu[1]))

                    for player in players.items():
                        if player[1][0].name == user["Name"]:

                            player[1][0].x, player[1][0].y = user['cord']
                            player[1][0].inventory = user["inventory"]
                            player[1][0].hp = user["hp"]
                            player[1][0].image = user["pos"]
                            player[1][1].x, player[1][1].y = int(user["cord"][0]), int(user["cord"][1])
                            player[1][0].cursor(mouse_pos, window)
                            player[1][0].render(window, player_images, weapons)

            if count_players <= 1:
                window.blit(game_over, (SIZE[0]/2-175, SIZE[1]/2-22))
                game_over_timer +=1
                if game_over_timer > 1000:
                    client.send("exit".encode())
                    time.sleep(0.5)
                    if self.player.hp > 0:
                        return 25, 50
                    else:
                        return 10, 0



            if keys[pygame.K_ESCAPE]:
                client.send("exit".encode())
                time.sleep(0.5)
                break



            pygame.display.update()

            iteration += 1
            self.FPS.tick(120)



class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0,0,width,height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target): pass
        #self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + SIZE[0]/2
    t = -target_rect.y + SIZE[1]/2

    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(camera.width-SIZE[0]), l)
    t = max(-(camera.height-SIZE[1]), t)
    t = min(0, t)

    return pygame.Rect(l,t,w,h)





class Map:
    def __init__(self, map):
        self.map = map
        #self.glass = pygame.image.load('images\\additional\grass.png')

    def render(self):
        camera = Camera(camera_func, 1000, 1000)

        for line in range(len(self.map)):
            for block in range(len(self.map[line])):
                if self.map[line][block] == 1:
                    window.blit(self.glass, camera.update(block))




map1 = Map(data['map1'])
menu = Menu()
game = Game()

menu.start()

