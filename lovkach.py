import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 10
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
     pygame.quit()
     sys.exit()

def waitForPlayerToPressKey():
     while True:
         for event in pygame.event.get():
             if event.type == QUIT:
                 terminate()
             if event.type == KEYDOWN:
                 if event.key == K_ESCAPE: # Нажатие ESC.
                     terminate()
                 return

def playerHasHitBaddie(playerRect, baddies):
     for b in baddies:
         if playerRect.colliderect(b['rect']):
             return True
     return False

def drawText(text, font, surface, x, y):
     textobj = font.render(text, 1, TEXTCOLOR)
     textrect = textobj.get_rect()
     textrect.topleft = (x, y)
     surface.blit(textobj, textrect)

 # Инициализация библиотеки, окна и курсора.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

 # Шрифты.
font = pygame.font.SysFont(None, 48)

 # Звуки.
#gameOverSound = pygame.mixer.Sound('gameover.wav')
#pygame.mixer.music.load('background.mid')

 # Изображения.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

 # Стартовый экран.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3),
       (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface,
       (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

#При старте игры лучший результат равен 0
topScore = 0
while True:
     # Подготовка к началу игры.
     baddies = []
     score = 0
     playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
     moveLeft = moveRight = moveUp = moveDown = False
     reverseCheat = slowCheat = False
     baddieAddCounter = 0
     #pygame.mixer.music.play(-1, 0.0)

     while True: # Игровой цикл.
         score += 1 

         for event in pygame.event.get():
             if event.type == QUIT:
                 terminate()

             if event.type == KEYDOWN:
                 if event.key == K_z:
                     reverseCheat = True
                 if event.key == K_x:
                     slowCheat = True
                 if event.key == K_LEFT or event.key == K_a:
                     moveRight = False
                     moveLeft = True
                 if event.key == K_RIGHT or event.key == K_d:
                     moveLeft = False
                     moveRight = True
                 if event.key == K_UP or event.key == K_w:
                     moveDown = False
                     moveUp = True
                 if event.key == K_DOWN or event.key == K_s:
                     moveUp = False
                     moveDown = True

             if event.type == KEYUP:
                 if event.key == K_z:
                     reverseCheat = False
                     score = 0
                 if event.key == K_x:
                     slowCheat = False
                     score = 0
                 if event.key == K_ESCAPE:
                     terminate()

                 if event.key == K_LEFT or event.key == K_a:
                     moveLeft = False
                 if event.key == K_RIGHT or event.key == K_d:
                     moveRight = False
                 if event.key == K_UP or event.key == K_w:
                     moveUp = False
                 if event.key == K_DOWN or event.key == K_s:
                     moveDown = False

             if event.type == MOUSEMOTION:
                 # Движение с помощью.
                 playerRect.centerx = event.pos[0]
                 playerRect.centery = event.pos[1]
         # Добавление новых препятствий при необходимости.
         if not reverseCheat and not slowCheat:
             baddieAddCounter += 1
         if baddieAddCounter == ADDNEWBADDIERATE:
             baddieAddCounter = 0
             baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
             newBaddie = {'rect': pygame.Rect(random.randint(0,
                                WINDOWWIDTH - baddieSize), 0 - baddieSize,
                                baddieSize, baddieSize),
                          'speed': random.randint(BADDIEMINSPEED,
                                BADDIEMAXSPEED),
                          'surface':pygame.transform.scale(baddieImage,
                                (baddieSize, baddieSize)),
                         }

             baddies.append(newBaddie)

         # Движение игрока.
         if moveLeft and playerRect.left > 0:
             playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
         if moveRight and playerRect.right < WINDOWWIDTH:
             playerRect.move_ip(PLAYERMOVERATE, 0)
         if moveUp and playerRect.top > 0:
             playerRect.move_ip(0, -1 * PLAYERMOVERATE)
         if moveDown and playerRect.bottom < WINDOWHEIGHT:
             playerRect.move_ip(0, PLAYERMOVERATE)

         # Движение препятствий.
         for b in baddies:
             if not reverseCheat and not slowCheat:
                 b['rect'].move_ip(0, b['speed'])
             elif reverseCheat:
                 b['rect'].move_ip(0, -5)
             elif slowCheat:
                 b['rect'].move_ip(0, 1)

         # Удаление препятствий за экраном.
         for b in baddies[:]:
             if b['rect'].top > WINDOWHEIGHT:
                 baddies.remove(b)

         # Прорисовка окна.
         windowSurface.fill(BACKGROUNDCOLOR)

         # Прорисовка счета.
         drawText('Score: %s' % (score), font, windowSurface, 10, 0)
         drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)

         # Прорисовка игрока.
         windowSurface.blit(playerImage, playerRect)

         # Прорисовка препятствий.
         for b in baddies:
             windowSurface.blit(b['surface'], b['rect'])

         pygame.display.update()

         # Проверка на попадание по игроку.
         if playerHasHitBaddie(playerRect, baddies):
             if score > topScore:
                 topScore = score # Set new top score.
             break

         mainClock.tick(FPS)

     # Оставнока игры и показ экрана окончания игры.
     #pygame.mixer.music.stop()
     #gameOverSound.play()

     drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3),
           (WINDOWHEIGHT / 3))
     drawText('Press a key to play again.', font, windowSurface,
           (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
     pygame.display.update()
     waitForPlayerToPressKey()

     #gameOverSound.stop()
