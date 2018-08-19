import sys, random, pygame
from pygame.locals import *

# 初始化pygame
pygame.init()
# 窗口大小
window_width, window_height = 800, 600
# 设置窗口和游戏名称
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('玩仔接电池雨')
level = 0
# 导入背景图片
background_image = pygame.image.load("resources/images/background.png")
screen.blit(background_image, (0, 0))
# 导入玩仔图片
wanzai = pygame.image.load("resources/images/wanzai.png")
wanzai_width, wanzai_height = wanzai.get_size()
# 设置字体
font1 = pygame.font.SysFont('simhei', 24)
gameove_font = pygame.font.SysFont('simhei', 54)
# 计算中心坐标
wanzai_left, wanzai_top = window_width // 2, window_height // 2
# 计算玩仔中心对齐的左上角坐标
wanzai_left, wanzai_top = wanzai_left - wanzai_width // 2, wanzai_top - wanzai_height // 2
screen.blit(wanzai, (wanzai_left, wanzai_top))

lives, number = 1000, 0
game_over = False
game_win = False


class Dianchi(pygame.sprite.Sprite):
    def __init__(self,position,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources\images\dianchi.png")
        self.wanzai_width, self.wanzai_height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed=speed
        
    def move(self):
        self.rect=self.rect.move(self.speed)

dianchi=pygame.sprite.Group()

def next_battery():
    dianchi_top = random.randint(0, 30)
    dianchi_left = random.randint(0, 800)
    pos=(dianchi_left,dianchi_top)
    speed = [0,random.randint(5,10)]
    newdianchi = Dianchi(pos,speed)
    # 添加进电池组
    dianchi.add(newdianchi)

def print_text(font, x, y, text, color=(255, 0, 0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

    
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
    if game_over == True:
        print_text(gameove_font, 300, 300, "Game Over")
        pygame.display.update()
        continue
    if game_win == True:
        print_text(gameove_font, 300, 300, "Win")
        pygame.display.update()
        continue
    wanzai_left, wanzai_top = mouse_x - wanzai_width // 2, mouse_y - \
                              wanzai_height // 2
    #pygame.time.delay(20) # 延时
    screen.blit(background_image, (0, 0))
    screen.blit(wanzai, (wanzai_left, wanzai_top))
    for i in range(random.randint(1,5)):
        next_battery()
    for dian in dianchi:
        dian.move()
        screen.blit(dian.image,dian.rect)
        if wanzai_left <= dian.rect.left and dian.rect.left + dian.wanzai_width <= \
     wanzai_left + wanzai_width and wanzai_top < dian.rect.top:
            number += 1
            dianchi.remove(dian)
        if dian.rect.top > window_height:  # miss a dianchi
            lives -= 1
            dianchi.remove(dian)
        if lives == 0:
            game_over = True
        if number == 1000:
            game_win = True
    print_text(font1, 0, 0, "生命值: " + str(lives))
    print_text(font1, 200, 0, "已接电池数: " + str(number))
    pygame.display.update()
