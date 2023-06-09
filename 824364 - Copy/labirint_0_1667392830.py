from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
    
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):  
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) 
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    def fire(self):
        bullet = Bullet('bulllet1.png', self.rect.centerx, self.rect.top, 30, 35, 10)
        bullets.add(bullet)

class Enemy_x(GameSprite):
    side = "left"
    def __init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y, x_left_granica, x_right_granica, x_speed,):
        GameSprite.__init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y)
        self.x_right_granica = x_right_granica
        self.x_left_granica = x_left_granica
        self.x_speed = x_speed
    def update(self):
        if self.rect.x <= self.x_left_granica:
            self.side = 'right'
        if self.rect.x >= self.x_right_granica:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.x_speed
        elif self.side == 'right':
            self.rect.x += self.x_speed
class Enemy_y(GameSprite):
    side = "left"
    def __init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y, y_up_granica, y_down_granica, y_speed):
        GameSprite.__init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y)
        self.y_up_granica = y_up_granica
        self.y_down_granica = y_down_granica
        self.y_speed = y_speed
    def update(self):
        if self.rect.y <= self.y_up_granica:
            self.side = 'down'
        if self.rect.y >= self.y_down_granica:
            self.side = 'up'

        if self.side == 'up':
            self.rect.y -= self.y_speed
        elif self.side == 'down':
            self.rect.y += self.y_speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()

font.init()
font1 = font.SysFont('arial', 25)

coins_amount=0

win_width = 1200
win_height = 800
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load("background111.jpg"), (win_width, win_height)) 

barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

coins = sprite.Group()

w1 = GameSprite("wall1.png",234,335, 100, 469 )
w2 = GameSprite("wall2.jpg", 102, 650, 135, 60)
w3 = GameSprite("wall2.jpg", 0, 500, 135, 60)
w4 = GameSprite("wall2.jpg", 102, 335, 135, 60)
w5 = GameSprite("wall2.jpg", 330, 500, 145, 85)
w6 = GameSprite("wall2.jpg", 0, 55, 338, 90)
w7 = GameSprite("wall2.jpg", 0, 137, 150,75)
w8 = GameSprite("wall2.jpg", 700, 125, 500, 50)
w9 = GameSprite("wall1.png", 800, 453, 69, 349)
w10 = GameSprite("wall2.jpg", 606, 533, 200, 50)
w11 = GameSprite("wall2.jpg", 865, 453, 145, 50)
w12 = GameSprite("wall1.png", 960, 337, 50, 120)
w13 = GameSprite("wall2.jpg", 1007, 337, 105, 40)
w14 = GameSprite("wall2.jpg", 1000, 600, 200, 30)

barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)
barriers.add(w14)

coin1 = GameSprite("coin.png", 259, 286, 50, 50)
coin2 = GameSprite("coin.png", 807, 404, 50, 50)
coin3 = GameSprite("coin.png", 370, 690, 50, 50)
coin4 = GameSprite("coin.png", 1112, 75, 50, 50)
coin5 = GameSprite("coin.png", 1100, 552, 50, 50)

coins.add(coin1)
coins.add(coin2)
coins.add(coin3)
coins.add(coin4)
coins.add(coin5)

packman = Player('packman1.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy_x('enemy22.png', win_width - 100, 33, 85, 85, 700, 1100, 1)
monster2 = Enemy_y('enemy22.png', win_width - 1020, 270, 80, 80, 140, 270, 1)
monster3 = Enemy_x("enemy22.png", win_width - 825, 630, 100, 100, 330, 710, 1)
monster4 = Enemy_y("enemy22.png", win_width - 412, 370, 80, 80, 175, 370, 1)
monster5 = Enemy_y("enemy22.png", win_width - 80, 150, 70, 70, 170, 526, 2)
final_sprite = GameSprite('cup.png', win_width - 129, win_height - 120, 125, 110)

monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

finish = False
run = True
while run:
    if sprite.spritecollide(packman, coins, True):
        coins_amount += 1
        if coins_amount == 5:
            final_sprite.reset()

    time.delay(5)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -2
            elif e.key == K_RIGHT:
                packman.x_speed = 2
            elif e.key == K_UP:
                packman.y_speed = -2
            elif e.key == K_DOWN:
                packman.y_speed = 2
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0 
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.blit(back, (0,0))

        text = font1.render(f'Бургерів зібрано: {coins_amount}/5', True, (0, 0, 0))
        window.blit(text, (10, 10))
        
        packman.update()
        bullets.update()

        packman.reset()
        bullets.draw(window)
        barriers.draw(window)
        coins.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, coins, True):
            coins_amount += 1
        if coins_amount == 5:
            final_sprite.reset()

        if sprite.spritecollide(packman, monsters, False):
            finish = False

            img = image.load('lose.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('winner.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    
    display.update()
