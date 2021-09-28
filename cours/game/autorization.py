import pygame
import random
import socket
from time import sleep
pygame.init()

from button import Button, Text, TextBox

class Reg:
    def __init__(self, h, w):
        self.h = h
        self.w = w

        self.login = Text((500, 40), '', (self.w/2-200, self.h/2-150), 32)
        self.password1 = Text((500, 40), '', (self.w/2-200, self.h/2-90), 32)

        #self.password2 = Text((500, 40), '', (self.w / 2 - 200, self.h / 2 - 30), 32)
        #self.code = Text((500, 40), '', (self.w / 2 - 200, self.h / 2 + 30), 32)

        self.dec1 = Text((100, 40), 'login:', (self.w/2-275, self.h/2-150), 32, color_box=(0,0,0), color=(255,255,255))
        self.dec2 = Text((120, 40), 'password:', (self.w/2-320, self.h/2-90), 32, color_box=(0,0,0), color=(255,255,255))
        #self.dec3 = Text((120, 40), 'password:', (self.w/2-320, self.h/2-30), 32, color_box=(0,0,0), color=(255,255,255))
        #self.dec4 = Text((210, 40), ' confirmation code:', (self.w/2-420, self.h/2+30), 32, color_box=(0,0,0), color=(255,255,255))

        self.code_m = str(random.randrange(10, 100))+str(random.randrange(100, 1000))

    def start(self, window, ip_s, port_s, name, money, coins):
        exit_b = Button((self.w/2-150, self.h/2+200, 300, 100), (255, 153, 51), 'Сохранить', 48, width_text=10)
        get_data = Button((self.w/2-150, self.h/2+100,  300, 90), (255, 153, 51), 'Получить данные', 30, width_text=10)

        email = 'muhammed.clans_2002@mail.ru'
        my_json_for_server = f'"name": "{name}", ' \
            f'"money": "{money}",' \
            f'"coins": "{coins}"'
        my_json_for_server = "{" + my_json_for_server + "}"
        while True:
            press_mouse = pygame.mouse.get_pressed()
            poss = pygame.mouse.get_pos()
            press_key = pygame.key.get_pressed()
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if press_key[pygame.K_ESCAPE]: break

            self.dec1.render()
            self.dec2.render()
            #self.dec3.render()
            #self.dec4.render()

            self.password1.render()
            #self.password2.render()
            self.login.render()
            #self.code.render()
            exit_b.render()
            get_data.render()

            if exit_b.press(poss, press_mouse):

                sock = socket.socket()
                try:
                    sock.connect((ip_s, int(port_s)))
                except:
                    continue
                sock.send(b"save")
                log_pas = self.login.text + "+" + self.password1.text
                sleep(0.5)
                sock.send(log_pas.encode())
                sleep(0.5)
                sock.send(my_json_for_server.encode())


                break
            if get_data.press(poss, press_mouse):
                sock = socket.socket()
                try:
                    sock.connect((ip_s, int(port_s)))
                except: continue
                sock.send(b"get_data")
                log_pas = self.login.text+"+"+self.password1.text
                sock.send(log_pas.encode())
                data = sock.recv(1024)
                if data == b'null': continue
                else: return data

            if self.login.press(poss, press_mouse):
                self.login.input_text = True
                self.password1.input_text = False
                #self.password2.input_text = False
                #self.code.input_text = False
            if self.login.input_text:
                self.login.input()



            if self.password1.press(poss, press_mouse):
                self.login.input_text = False
                self.password1.input_text = True
                #self.password2.input_text = False
                #self.code.input_text = False
            if self.password1.input_text:
                self.password1.input()


            #if self.password2.press(poss, press_mouse):
            #    self.password2.input_text = True
            #    self.login.input_text = False
            #    self.password1.input_text = False
                #self.code.input_text = False
            #if self.password2.input_text:
            #    self.password2.input()


            #if self.code.press(poss, press_mouse):
                #self.code.input_text = True
                #self.login.input_text = False
                #self.password1.input_text = False
                #self.password2.input_text = False
            #if self.code.input_text:
                #self.code.input()



            #send.render()
            #if send.press(poss, press_mouse):
                #break


            pygame.display.update()

class ConfigGame:
    def __init__(self, h, w):
        self.h = h
        self.w = w

        self.count_player = Text((500, 40), '2', (self.w / 2 - 200, self.h / 2 - 150), 32)
        self.name = Text((500, 40), 'Muha', (self.w / 2 - 200, self.h / 2 - 90), 32)
        self.ip = Text((500, 40), '127.0.0.1', (self.w / 2 - 200, self.h / 2 - 30), 32)
        self.port = Text((500, 40), '7978', (self.w / 2 - 200, self.h / 2 + 30), 32)

        self.dec1 = Text((200, 40), 'Count players 2-5:', (self.w / 2 - 400, self.h / 2 - 150), 32, color_box=(0, 0, 0),
                         color=(255, 255, 255))
        self.dec2 = Text((130, 40), 'your name:', (self.w / 2 - 330, self.h / 2 - 90), 32, color_box=(0, 0, 0),
                         color=(255, 255, 255))

        self.dec3 = Text((120, 40), 'ip server:', (self.w/2-315, self.h/2-30), 32, color_box=(0,0,0), color=(255,255,255))
        self.dec4 = Text((210, 40), 'port server:', (self.w/2-330, self.h/2+30), 32, color_box=(0,0,0), color=(255,255,255))

        #self.code_m = str(random.randrange(10, 100)) + str(random.randrange(100, 1000))

    def start(self, window):
        exit_b = Button((self.w / 2 - 100, self.h / 2 + 200, 200, 100), (255, 153, 51), 'Готово', 48, width_text=15)

        email = 'muhammed.clans_2002@mail.ru'

        while True:
            press_mouse = pygame.mouse.get_pressed()
            poss = pygame.mouse.get_pos()
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.dec1.render()
            self.dec2.render()
            self.dec3.render()
            self.dec4.render()

            self.count_player.render()
            self.ip.render()
            self.name.render()
            self.port.render()
            exit_b.render()
            if exit_b.press(poss, press_mouse):
                return self.count_player.text, self.name.text, self.ip.text, self.port.text

            if self.name.press(poss, press_mouse):
                self.name.input_text = True
                self.count_player.input_text = False
                self.ip.input_text = False
                self.port.input_text = False
            if self.name.input_text:
                self.name.input()

            if self.count_player.press(poss, press_mouse):
                self.name.input_text = False
                self.count_player.input_text = True
                self.ip.input_text = False
                self.port.input_text = False
            if self.count_player.input_text:
                self.count_player.input()

            if self.ip.press(poss, press_mouse):
                self.ip.input_text = True
                self.name.input_text = False
                self.count_player.input_text = False
                self.port.input_text = False
            if self.ip.input_text:
                self.ip.input()

            if self.port.press(poss, press_mouse):
                self.port.input_text = True
                self.name.input_text = False
                self.count_player.input_text = False
                self.ip.input_text = False
            if self.port.input_text:
                self.port.input()

            # send.render()
            # if send.press(poss, press_mouse):
            # break

            pygame.display.update()
