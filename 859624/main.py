import pygame
from pygame import mixer, font, image, sprite, transform, mouse, time, key, event
from pygame.locals import *

pygame.init()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, wight, height, x, y, angle):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture), (wight, height))
        self.rect = self.image.get_rect()
        self.angle = angle
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def moving(self):
        variable_x = True
        if variable_x == True:
            image_2 = transform.rotate(self.image, self.angle)
            window.blit(image_2, ((self.rect.x), (self.rect.y)))


class Player(GameSprite):
    def __init__(self, picture, wight, height, x, y, speed_x, speed_y, angle):
        GameSprite.__init__(self, picture, wight, height, x, y, angle)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.original_image = self.image
        self.rect.x = 1300
        self.rect.y = 760
        self.angle = 180
        self.jumping = False    
        self.jump_height = 30  # Висота стрибка
        self.jump_speed = 5    # Швидкість стрибка

    def update(self):
        global R
        global click
        global run
        keys = key.get_pressed()
        if keys[K_SPACE] and not self.jumping:  # Перевіряти, чи не знаходиться гравець в стрибку
            self.jumping = True  
            self.jump_start_y = self.rect.y  
        elif keys[K_RIGHT]:
            self.rect.x += self.speed_x
            self.angle = 0
        elif keys[K_LEFT]:
            self.rect.x -= self.speed_x
            self.angle = 180

        if self.jumping:
            # Виконувати стрибок
            self.rect.y -= self.jump_speed
            if self.rect.y <= self.jump_start_y - self.jump_height:
                # Досягнута максимальна висота стрибка, завершити стрибок
                self.jumping = False
        else:
            # Гравець не стрибає, рухається вниз під впливом гравітації
            self.rect.y += self.speed_y

        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    self.speed_x = 10
                    self.angle = 0
                elif e.key == K_LEFT:
                    self.speed_x = -10
                    self.angle = 180
            elif e.type == KEYUP:
                if e.key == K_RIGHT or e.key == K_LEFT:
                    self.speed_x = 0

            elif e.type == QUIT:
                run = False

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 740:
            self.rect.x = 740
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 420:
            self.rect.y = 420

        touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y > 0:
            for p in touched:
                self.rect.bottom = p.rect.top
        else:
            if self.speed_x > 0:
                for p in touched:
                    self.rect.right = p.rect.left
            elif self.speed_x < 0:
                for p in touched:
                    self.rect.left = p.rect.right

        if self.speed_y < 0:
            for p in touched:
                self.rect.top = p.rect.bottom

        # Перевірка на зіткнення з водою
        water_hit = sprite.spritecollide(self, water_group, False)
        if water_hit:
            self.rect.x = 200  
            self.rect.y = 600
            self.speed_x = 5
            self.speed_y = 5
            self.angle = 10
            self.jumping = False

        if show_player:
            self.image = transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)


class Button():
    def __init__(self, picture, width, height, x, y, scaleW, scaleH):
        self.width = width
        self.height = height
        self.image = image.load(picture)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.scaleW = scaleW
        self.scaleH = scaleH
        self.image2 = pygame.transform.scale(image.load(picture), (scaleW, scaleH))
        self.rect.x = x
        self.rect.y = y

    def draw(self, show=True):
        agree = True
        pos = mouse.get_pos()
        if show and self.rect.collidepoint(pos):
            agree = False
            window.blit(self.image2, (self.rect.x, self.rect.y))
        elif show:
            window.blit(self.image, (self.rect.x, self.rect.y))
        return agree

pygame.init()

barriers = sprite.Group()
splaer = sprite.Group()
water_group = sprite.Group()  

level1 = Button('lvl1.png', 70, 70, 260, 590, 80, 80)
level2 = Button('lvl2.png', 70, 70, 490, 300, 80, 80)
level3 = Button('lvl3.png', 70, 70, 940, 100, 80, 80)
level4 = Button('lvl4.png', 70, 70, 1330, 290, 80, 80)
Musicon = Button('orig.png', 70, 70, 100, 100, 70, 70)

mixer.init()
mixer.music.load('background_music.mp3')
mixer.music.play(-1)

font.init()
font1 = font.SysFont('font2.ttf', 25)

win_width = 1440
win_height = 900
pygame.display.set_caption("Mario")
window = pygame.display.set_mode((win_width, win_height))
background_color = (0, 0, 0)

background = pygame.transform.scale(image.load("main_screen.jpg"), (win_width, win_height))

player = None  
show_player = False  

button_width = 200
button_height = 50
button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)
font_obj = font.SysFont('font2.ttf', 25)

change = 0
main_menu = True
settings_menu = False
music_enabled = True

running = True
show_buttons = True
while running:
    time.delay(5)
    if change == 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            window.blit(background, (0, 0))

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if Musicon.rect.collidepoint(e.pos):
                    music_enabled = not music_enabled
                elif level1.rect.collidepoint(e.pos):
                    show_buttons = False
                    background = pygame.transform.scale(image.load("backgroundlvl1.jpg"), (win_width, win_height))
                    mixer.music.load('lvls.mp3')
                    mixer.music.play(-1)

                    w0 = GameSprite("block.png", 70, 70, 0, 760, 15)
                    w1 = GameSprite("block.png", 70, 70, 0, 830, 15)
                    w2 = GameSprite("block.png", 70, 70, 70, 830, 15)
                    w3 = GameSprite("block.png", 70, 70, 140, 830, 15)
                    w4 = GameSprite("block.png", 70, 70, 210, 830, 15)
                    w5 = GameSprite("block.png", 70, 70, 280, 830, 15)
                    w6 = GameSprite("block.png", 70, 70, 350, 830, 15)
                    w7 = GameSprite("block.png", 70, 70, 420, 830, 15)
                    water1 = GameSprite("water.png", 70, 70, 490, 830, 15)
                    water2 = GameSprite("water.png", 70, 70, 560, 830, 15)
                    water3 = GameSprite("water.png", 70, 70, 630, 830, 15)
                    water4 = GameSprite("water.png", 70, 70, 700, 830, 15)
                    water5 = GameSprite("water.png", 70, 70, 770, 830, 15)
                    water6 = GameSprite("water.png", 70, 70, 840, 830, 15)
                    water7 = GameSprite("water.png", 70, 70, 910, 830, 15)
                    w10 = GameSprite("block.png", 70, 70, 980, 830, 15)
                    w11 = GameSprite("block.png", 70, 70, 1050, 830, 15)
                    w12 = GameSprite("block.png", 70, 70, 1120, 830, 15)
                    w13 = GameSprite("block.png", 70, 70, 1190, 830, 15)
                    w14 = GameSprite("block.png", 70, 70, 1260, 830, 15)
                    w15 = GameSprite("block.png", 70, 70, 1330, 830, 15)
                    w16 = GameSprite("block.png", 70, 70, 1400, 830, 15)
                    wall2 = GameSprite("wall2.jpg", 60, 40, 620, 700, 15)
                    wall3 = GameSprite("wall2.jpg", 60, 40, 800, 700, 15)
                    w100 = GameSprite("block.png", 70, 70, 170, 575, 15)
                    w101 = GameSprite("block.png", 70, 70, 310, 575, 15)
                    w102 = GameSprite("lucky_block.png", 70, 70, 240, 575, 15)
                    w20 = GameSprite("wall2.jpg", 65, 30, 450, 500, 15)
                    w21 = GameSprite("wall2.jpg", 65, 30, 625, 430, 15)
                    w22 = GameSprite("wall2.jpg", 65, 30, 800, 370, 15)
                    w23 = GameSprite("wall2.jpg", 65, 30, 975, 300, 15)
                    w24 = GameSprite("wall2.jpg", 300, 40, 1100, 175, 15)

                    barriers.add(w0)
                    barriers.add(w1)
                    barriers.add(w2)
                    barriers.add(w3)
                    barriers.add(w4)
                    barriers.add(w5)
                    barriers.add(w6)
                    barriers.add(w7)
                    barriers.add(w10)
                    barriers.add(w11)
                    barriers.add(w12)
                    barriers.add(w13)
                    barriers.add(w14)
                    barriers.add(w15)
                    barriers.add(w16)
                    barriers.add(water1)
                    barriers.add(water2)
                    barriers.add(water3)
                    barriers.add(water4)
                    barriers.add(water5)
                    barriers.add(water6)
                    barriers.add(water7)
                    barriers.add(wall2)
                    barriers.add(wall3)
                    barriers.add(w100)
                    barriers.add(w101)
                    barriers.add(w102)
                    barriers.add(w20)
                    barriers.add(w21)
                    barriers.add(w22)
                    barriers.add(w23)
                    barriers.add(w24)

                    water_obj1 = GameSprite("water.png", 70, 70, 490, 830, 15)
                    water_obj2 = GameSprite("water.png", 70, 70, 560, 830, 15)
                    water_obj3 = GameSprite("water.png", 70, 70, 630, 830, 15)
                    water_obj4 = GameSprite("water.png", 70, 70, 700, 830, 15)
                    water_obj5 = GameSprite("water.png", 70, 70, 770, 830, 15)
                    water_obj6 = GameSprite("water.png", 70, 70, 840, 830, 15)
                    water_obj7 = GameSprite("water.png", 70, 70, 910, 830, 15)

                    water_group.add(water_obj1)
                    water_group.add(water_obj2)
                    water_group.add(water_obj3)
                    water_group.add(water_obj4)
                    water_group.add(water_obj5)
                    water_group.add(water_obj6)
                    water_group.add(water_obj7)

                    player = Player("main_hero.png", 100, 100, 1300, 700, 5, 5, 10)
                    splaer.add(player)
                    show_player = True  

        if show_buttons:
            level1_agree = level1.draw()
            level2_agree = level2.draw()
            level3_agree = level3.draw()
            level4_agree = level4.draw()
        Musicon_agree = Musicon.draw()

        if music_enabled:
            mixer.music.unpause()
        else:
            mixer.music.pause()

        if show_player:
            splaer.update()
            splaer.draw(window)
        if not show_buttons:
            barriers.draw(window)
            water_group.draw(window)  

        pygame.display.flip()
        pygame.display.update()
    
pygame.quit()