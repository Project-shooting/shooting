import pygame
import random
import shooting_db as db
import time
from datetime import datetime

# 1. 게임 초기화
pygame.init()

db_user = "dogyu"
db_password = "dogyu0081"
db.db_connecting(db_user, db_password)
# 2. 게임창 옵션 설정
size = [600, 900]
screen = pygame.display.set_mode(size)

title = "My Game"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()
# 각 폰트 사이즈
font_element = pygame.font.Font("C:/Windows/Fonts/HMKMRHD.TTF", 20)
font_board = pygame.font.Font("C:/Windows/Fonts/HMKMRHD.TTF", 30)
font_headline = pygame.font.Font("C:/Windows/Fonts/HMKMRHD.TTF", 40)

class obj:
    def __ini__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        self.health = 2

    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))


def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False


ss = obj()
ss.put_img("./src/cat.png")
ss.change_size(60, 80)
ss.x = round(size[0] / 2 - ss.sx / 2)
ss.y = size[1] - ss.sy - 15
ss.move = 10

black = (0, 0, 0)
left_go = False
right_go = False
space_go = False

m_list = []
a_list = []
k = 0

score = 0
loss = 0
GO = 0

# 4-0. 게임 시작 대기 화면
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(black)
    text = font_element.render("PRESS SPACE KEY TO START THE GAME", True, (255, 255, 255))
    screen.blit(text, (40, round(size[1] / 2 - 50)))
    pygame.display.flip()

# 레벨(난이도) 설정
level = 1
max_level = 10
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if level > 1:
                    level -= 1
            elif event.key == pygame.K_UP:
                 if level < max_level:
                    level += 1
            elif event.key == pygame.K_SPACE:
                    SB = 1
    screen.fill(black)

    text = font_element.render("LEVEL {}".format(level), True, (255, 255, 255))
    screen.blit(text, (40, round(size[1] / 2 - 10)))

    text_setting = font_element.render(("↑,  ↓,  SpaceBar"), True, (255, 255, 0))
    screen.blit(text_setting, (40, round(size[1] / 2 + 20)))

    pygame.display.flip()

# 4. 메인 이벤트
start_time = datetime.now()
regen = 0.95 - ((level - 1)*0.05)
gravity = 1 + ((level -1) * 0.4)
SB = 0
while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60)
    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())

    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0
    elif right_go == True:
        ss.x += ss.move
        if ss.x > size[0] - ss.sx:
            ss.x = size[0] - ss.sx

    # 미사일 생성
    if space_go == True and k % 6 == 0:
        mm = obj()
        mm.put_img("./src/bullet.png")
        mm.change_size(10, 10)
        mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)
    k += 1
    # 미사일 발사

    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y <= -m.sy:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del m_list[d]

    if random.random() > regen:
        aa = obj()
        aa.put_img("./src/rat.png")
        aa.change_size(45, 45)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2))
        aa.y = 10
        aa.move = gravity
        a_list.append(aa)

    d_list = []
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del a_list[d]
        loss += 1

    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m, a) == True:
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))

    dm_list.reverse()
    for dm in dm_list:
        del m_list[dm]
    da_list.reverse()
    for da in da_list:
        del a_list[da]
        score += 1

    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1
            GO = 1
    # 4-4. 그리기
    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()

    # level/time/score
    text_level = font_element.render("LEVEL {}".format(level), True, (255,255,0))
    screen.blit(text_level, (10,5))

    text_score = font_element.render("SCORE : {}".format(score), True, (255, 255, 0))
    screen.blit(text_score, (size[0] - text_score.get_width() - 5, 5))

    text_time = font_element.render("TIME : {}".format(delta_time), True, (255, 255, 0))
    screen.blit(text_time, (size[0]/2 - 40, 5))

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                GO = 0

    text_end = font_board.render("GAME OVER", True, (255, 0, 0))
    text_end_width = text_end.get_rect().width
    screen.blit(text_end, (round(size[0]/2 - text_end_width/2), round(size[1]/2 - 40)))

    pygame.display.flip()

# 이름 입력
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect((size[0]/2 - 100), 250, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
input_name = ''
done = False

while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    done = True
                    db.db_inserting(level, input_name, score)
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    input_name += event.unicode

    screen.fill((0,0,0))
    # Render the current text.
    text_board = font_board.render("write your name", True, (255,255,0))
    screen.blit(text_board, (round(size[0]/2-text_board.get_rect().width/2), 200))

    txt_surface = font.render(input_name, True, color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
    clock.tick(30)
# 랭킹
# 클라우드 DB 조회, 생성
RK = 1
data = db.printing_data(level)

while RK == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RK = 0
    screen.fill(black)

    headline = font_headline.render("LEVEL {} RANKING".format(level), True, (255, 255, 0))
    headline_width = headline.get_rect().width
    headline_height = headline.get_rect().height
    screen.blit(headline, (round(size[0]/2 - headline_width/2), 55))


    legend_player = font_board.render("PLAYER", True, (255, 255, 0))
    legend_player_width = legend_player.get_rect().width
    screen.blit(legend_player, ((round(size[0]/2 - headline_width/2), 80 + headline_height)))

    legend_score = font_board.render("SCORE", True, (255, 255, 0))
    legend_score_width = legend_score.get_rect().width
    screen.blit(legend_score, ((round(size[0]/2 - headline_width/2) + headline_width - legend_score_width), 80 + headline_height))

    board_y = 80 + headline_height + legend_score.get_rect().height
    for ele in data:
        board_y += 5
        player = font_board.render("{}".format(ele['name']), True, (255, 255, 255))
        screen.blit(player, ((round(size[0]/2 - headline_width/2), board_y)))
        score = font_board.render("{} ".format(ele['score']), True, (255, 255, 255))
        score_width = score.get_rect().width
        screen.blit(score, (round(size[0]/2 - headline_width/2) + headline_width - score_width + 15, board_y))
        board_y += player.get_rect().height
    pygame.display.flip()

db.db_disconnecting()
pygame.quit()