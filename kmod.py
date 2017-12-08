## Using Modifier Keys
## ~~~~~~~~~~~~~~~~~~~
## e.mod gives a single integer that tells us about all of the modifer
## keys that are currently pressed (shift, alt, ctrl ....) 
## Pygame name     value       value as binary
## KMOD_NONE       0           000000000000000
## KMOD_LSHIFT     1           000000000000001
## KMOD_RSHIFT     2           000000000000010
## KMOD_SHIFT      3           000000000000011
## KMOD_LCTRL     64           000000001000000
## KMOD_RCTRL    128           000000010000000
## KMOD_CTRL     192           000000011000000
## KMOD_LALT     256           000000100000000
## KMOD_RALT     512           000001000000000
## KMOD_ALT      768           000001100000000
## KMOD_LMETA   1024           000010000000000
## KMOD_RMETA   2048           000100000000000
## KMOD_META    3072           000110000000000
## KMOD_NUM     4096           001000000000000
## KMOD_CAPS    8192           010000000000000
## KMOD_MODE   16384           100000000000000
##
## To figure out what is pressed we use a bitwise or (|).
## e.g. 12 | 10 == 14    We do an or operation on each bit.
## 12 = 1100             0 | 0 = 0
## 10 = 1010 or          0 | 1 = 1 
##      ----             1 | 0 = 1
## 14 = 1110             1 | 1 = 1
##
## When you run this program and hold down the left control and the left
## shift as you press any key you will see that the mod value is either 4161 
## or 65. If you have num lock on you will get 4161.
## KMOD_LSHIFT = 1, KMOD_LCTRL = 64, KMOD_NUM = 4096
## 1+64 = 65      1+64+4096 = 4161
## To just check if the Control key is pressed we do an or with KMOD_CTRL.
## e.g.
## 001000001000001
## 000000011000000 or
## ---------------
## 000000001000000

from pygame import *
from random import *

def show(fnt,message,x,y):
    screen.fill(0)
    txtPic = fnt.render(message,True,(255,255,0))
    screen.blit(txtPic,(x,y))

screen = display.set_mode((800,600))
font.init()
fName = choice(font.get_fonts())
fnt = font.SysFont(fName, 40)

running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
           print(e.unicode,e.key,e.mod)
           if e.mod & KMOD_CTRL > 0:
               if e.key == K_z:
                   show(fnt,"Control Z",200,260)
               if e.key == K_x:
                   show(fnt,"Control X",200,260)
               if e.key == K_c:
                   show(fnt,"Control C",200,260)

    display.flip()

quit()
