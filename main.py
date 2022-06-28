from pygame.locals import *
import random
import pygame

FPS = 30
BACKGROUND = pygame.image.load('./assets/background.png')
WINDOW_WIDTH = BACKGROUND.get_rect().size[0]
WINDOW_HEIGHT = BACKGROUND.get_rect().size[1]
PENGUIN_ACCELERATION = .2
PENGUIN_MAX_SPEED = 10.0
SCORE = 0


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, color, x, y, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def init(self):
        self.rect.x = random.randrange(37, WINDOW_WIDTH - 37)
        self.rect.y = 0

    def update(self):
        pass


def init_game():
    global DISPLAY_SURF, FPS_CLOCK, WINDOW_WIDTH, WINDOW_HEIGHT
    global BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    DISPLAY_SURF.convert_alpha()
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Penguin\'s Basket')

    # ----------- Load Resources

    global SPRITES, PENGUIN
    global BACKGROUND_IMAGE, PENGUIN_IMAGE, PENGUIN_RECT
    BACKGROUND_IMAGE = pygame.image.load('./assets/background.png')
    PENGUIN = Entity(pygame.image.load('./assets/penguin.png'), DISPLAY_SURF.get_rect(
    ), WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.8)
    # https://stackoverflow.com/questions/13851051/how-to-use-sprite-groups-in-pygame
    SPRITES = pygame.sprite.Group()
    SPRITES.add(PENGUIN)

    global FISHES, SEAGULLS, GOOD, BAD
    FISHES = []
    FISHES.append(Entity(pygame.image.load('./assets/fish1.png'),
                  DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))
    FISHES.append(Entity(pygame.image.load('./assets/fish2.png'),
                  DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))
    FISHES.append(Entity(pygame.image.load('./assets/fish3.png'),
                  DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))
    FISHES.append(Entity(pygame.image.load('./assets/fish4.png'),
                  DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))
    FISHES.append(Entity(pygame.image.load('./assets/fish5.png'),
                  DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))

    SEAGULLS = []
    SEAGULLS.append(Entity(pygame.image.load('./assets/gull1.png'),
                    DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))
    SEAGULLS.append(Entity(pygame.image.load('./assets/gull2.png'),
                    DISPLAY_SURF.get_rect(), WINDOW_WIDTH * 0.5, 0))

    GOOD = Entity(pygame.image.load('./assets/good.png'), DISPLAY_SURF.get_rect(
    ), WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.2)
    BAD = Entity(pygame.image.load('./assets/bad.png'), DISPLAY_SURF.get_rect(),
                 WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.2)

    # -- GOOD, BAD 이미지 투명하게 만들기 위해서
    # -- 참고링크 : https://stackoverrun.com/ko/q/10998578
    GOOD.image.convert_alpha()
    BAD.image.convert_alpha()


def game_loop():
    global DISPLAY_SURF, FPS_CLOCK, FPS, BASIC_FONT
    global BACKGROUND_IMAGE
    global PENGUIN_MAX_SPEED, PENGUIN_ACCELERATION, PENGUIN_IMAGE, PENGUIN_RECT, PENGUIN
    global SPRITES, SCORE, FISHES, SEAGULLS, GOOD, BAD

    SCORE = 0
    penguin_speed = 0.0             # 펭귄의 이동값
    penguin_acceleration = 0.0      # 펭귄의 가속도
    is_left_moving = False
    is_right_moving = False
    is_fish_falling = False
    is_seagull_falling = False
    good_alpha = 0
    bad_alpha = 0

    while True:
        # ----------- get fish
        if (is_fish_falling == False):
            fish = FISHES[random.randint(0, 4)]
            fish.init()
            SPRITES.add(fish)
            is_fish_falling = True

        if (is_fish_falling == True):
            fish.rect.y += 5

        if ((is_seagull_falling == False) and (random.randint(0, 99) >= 90)):
            seagull = SEAGULLS[random.randint(0, 1)]
            seagull.init()
            SPRITES.add(seagull)
            is_seagull_falling = True

        if (is_seagull_falling == True):
            seagull.rect.y += 5

        # ----------- keyboard event
        for event in pygame.event.get():
            if (event.type == QUIT):
                pygame.quit()
                # return

            elif (event.type == KEYUP):
                if (event.key == K_LEFT):
                    is_left_moving = False
                elif (event.key == K_RIGHT):
                    is_right_moving = False

            elif (event.type == KEYDOWN):
                if (event.key == K_LEFT):
                    is_left_moving = True
                    penguin_acceleration = -float(PENGUIN_ACCELERATION)
                elif (event.key == K_RIGHT):
                    is_right_moving = True
                    penguin_acceleration = float(PENGUIN_ACCELERATION)

        if (not is_left_moving and not is_right_moving):
            penguin_acceleration = 0
        penguin_speed += PENGUIN_MAX_SPEED * penguin_acceleration
        if (not is_left_moving and not is_right_moving):
            penguin_speed *= 0.9

        if (is_left_moving and penguin_speed < -PENGUIN_MAX_SPEED):
            penguin_speed = -PENGUIN_MAX_SPEED
        elif (is_right_moving and penguin_speed > PENGUIN_MAX_SPEED):
            penguin_speed = PENGUIN_MAX_SPEED
        PENGUIN.rect.x += round(penguin_speed)

        if (PENGUIN.rect.x < 0):
            PENGUIN.rect.x = 0
        if (PENGUIN.rect.x + PENGUIN.rect.size[0] > WINDOW_WIDTH):
            PENGUIN.rect.x = round(WINDOW_WIDTH - PENGUIN.rect.size[0])

        #print(PENGUIN.rect.x, PENGUIN.rect.y, (PENGUIN.rect.x + PENGUIN.rect.size[0])*0.5, (PENGUIN.rect.y + PENGUIN.rect.size[1])*0.5)

        if (is_fish_falling == True):
            if (PENGUIN.rect.x + PENGUIN.rect.size[0] >= fish.rect.x and PENGUIN.rect.x <= fish.rect.x + fish.rect.size[0] and PENGUIN.rect.y + PENGUIN.rect.size[1] * 0.5 >= fish.rect.y and PENGUIN.rect.y <= fish.rect.y + fish.rect.size[1]):
                SPRITES.remove(fish)
                GOOD.rect.x = PENGUIN.rect.x + \
                    float(PENGUIN.rect.size[0] * 0.25) + \
                    random.randint(-20, 20)
                GOOD.rect.y = PENGUIN.rect.y - random.randint(0, 20)
                good_alpha = 255
                is_fish_falling = False
                SCORE += 1
            if (fish.rect.y > WINDOW_HEIGHT):
                SPRITES.remove(fish)
                is_fish_falling = False

        if (is_seagull_falling == True):
            if (PENGUIN.rect.x + PENGUIN.rect.size[0] >= seagull.rect.x and PENGUIN.rect.x <= seagull.rect.x + seagull.rect.size[0] and PENGUIN.rect.y + PENGUIN.rect.size[1] * 0.5 >= seagull.rect.y and PENGUIN.rect.y <= seagull.rect.y + seagull.rect.size[1]):
                SPRITES.remove(seagull)
                BAD.rect.x = PENGUIN.rect.x + \
                    float(PENGUIN.rect.size[0] * 0.25) + \
                    random.randint(-20, 20)
                BAD.rect.y = PENGUIN.rect.y - random.randint(0, 20)
                bad_alpha = 255
                is_seagull_falling = False
                SCORE -= 1
            if (seagull.rect.y > WINDOW_HEIGHT):
                SPRITES.remove(seagull)
                is_seagull_falling = False

        # if (SCORE < 0):
        #    return

        if (good_alpha > 0):
            good_alpha *= 0.9
            if(good_alpha < 0.01):
                good_alpha = 0

        if (bad_alpha > 0):
            bad_alpha *= 0.9
            if (bad_alpha < 0.01):
                bad_alpha = 0

        # draw
        DISPLAY_SURF.fill((255, 255, 255))
        DISPLAY_SURF.blit(BACKGROUND_IMAGE, (0, 0))
        scoreboard = BASIC_FONT.render(
            "score : {}".format(SCORE), True, (0, 102, 102))
        DISPLAY_SURF.blit(scoreboard, (WINDOW_WIDTH / 2, 20))
        SPRITES.update()
        SPRITES.draw(DISPLAY_SURF)
        blit_alpha(DISPLAY_SURF, GOOD.image,
                   (GOOD.rect.x, GOOD.rect.y), good_alpha)
        blit_alpha(DISPLAY_SURF, BAD.image,
                   (BAD.rect.x, BAD.rect.y), bad_alpha)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def run_game():
    global DISPLAY_SURF

    init_game()
    game_loop()


if __name__ == "__main__":
    run_game()
