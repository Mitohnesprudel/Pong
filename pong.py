from cv2 import imshow, putText, waitKey, FONT_HERSHEY_SIMPLEX
from numpy import zeros
from keyboard import is_pressed
from time import time
from random import choice, randint

given = int(input("Enter Windows Size (e.g 128): "))
if(given < 128):
    given = 128
    print("Width set to minimum of 128")
if(given % 2 != 0):
    given += 1
    print("Width adjusted to " + str(given) + " to make it divisible by 2")

WIDTH = given

print("Press Ctrl + C to close")
PADDLE_HEIGHT = int(WIDTH/9.14285714286)
PADDLE_WIDTH = int(WIDTH/64)

PADDLE_SPEED = int(WIDTH/2)
BALL_SPEED = int(WIDTH/3)

POSSIBILITIES = [-1,1]
FONT_SCALE = WIDTH/426.666666667
FONT_POSY = int(WIDTH/8)

PADDLE_SPACING = int(WIDTH/16)
FONT1_POSX = int(WIDTH/3*0.7)
FONT2_POSX = int(WIDTH/3*2.2)
FONT_WIDTH = int(WIDTH/128)

onemovementint = int(WIDTH/2)-PADDLE_HEIGHT
onemovementfloat = int(WIDTH/2)-PADDLE_HEIGHT

twomovementint = int(WIDTH/2)-PADDLE_HEIGHT
twomovementfloat = int(WIDTH/2)-PADDLE_HEIGHT

one = 0
two = 0

#P:Y,P:X,V:Y,V:X
ball = [0,0,randint(0,WIDTH-1),int(WIDTH/2),choice(POSSIBILITIES),choice(POSSIBILITIES)]

delta = 0
while True:
    collision = False
    end = time()
    frame = zeros((WIDTH,WIDTH))

    if(is_pressed("up") and onemovementint > 0):
        onemovementfloat -= PADDLE_SPEED*delta
    if(is_pressed("down") and onemovementint < WIDTH-PADDLE_HEIGHT):
        onemovementfloat += PADDLE_SPEED*delta

    if(is_pressed("w") and twomovementint > 0):
        twomovementfloat -= PADDLE_SPEED*delta
    if(is_pressed("s") and twomovementint < WIDTH-PADDLE_HEIGHT):
        twomovementfloat += PADDLE_SPEED*delta

    onemovementint = int(onemovementfloat)
    twomovementint = int(twomovementfloat)

    for x in range(PADDLE_WIDTH):
        for i in range(PADDLE_HEIGHT):
            if(i+twomovementint < WIDTH and i+onemovementint < WIDTH):
                frame[i+onemovementint][WIDTH-PADDLE_SPACING-x] = 1
                frame[i+twomovementint][PADDLE_SPACING+x] = 1

    ball[2] += ball[4]*delta*BALL_SPEED
    ball[3] += ball[5]*delta*BALL_SPEED
    if(ball[2] > WIDTH):
        ball[4] = -1
    if(ball[3] > WIDTH):
        ball[5] = -1

    if(ball[2] < PADDLE_WIDTH/2):
        ball[4] = 1
    if(ball[3] < PADDLE_WIDTH/2):
        two += 1
        ball = [0,0,randint(0,WIDTH-1),int(WIDTH/2),choice(POSSIBILITIES),choice(POSSIBILITIES)]
        continue

    if(ball[2] < WIDTH and ball[2] > 0 and ball[3] > 0):
        ball[0] = int(ball[2])
        ball[1] = int(ball[3])

    if(ball[3] > WIDTH):
        one += 1
        ball = [0,0,randint(0,WIDTH-1),int(WIDTH/2),choice(POSSIBILITIES),choice(POSSIBILITIES)]
        continue

    for y in range(PADDLE_WIDTH):
        for x in range(PADDLE_WIDTH):
            if(ball[0]+x-PADDLE_WIDTH > 0):
                if(frame[ball[0]+x-PADDLE_WIDTH][ball[1]+y-PADDLE_WIDTH] > 0.5 and collision == False):
                    collision = True
                    if(ball[5] > 0.5):
                        ball[5] = -1
                    else:
                        ball[5] = 1
                else:
                    frame[ball[0]+x-PADDLE_WIDTH][ball[1]+y-PADDLE_WIDTH] = 1

    for i in range(WIDTH):
        if(i % 16 < 8):
            frame[i][int(WIDTH/2)] = 1

    frame = putText(frame, str(one), org=(FONT1_POSX,FONT_POSY), fontScale=FONT_SCALE, color=(255,255,255), fontFace=FONT_HERSHEY_SIMPLEX, thickness=FONT_WIDTH)
    frame = putText(frame, str(two), org=(FONT2_POSX,FONT_POSY), fontScale=FONT_SCALE, color=(255,255,255), fontFace=FONT_HERSHEY_SIMPLEX, thickness=FONT_WIDTH)

    imshow('Pong', frame)
    waitKey(1)
    delta = time() - end