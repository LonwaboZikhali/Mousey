import pygame
pygame.init()
import random


#background
fullscreen = (1366,710)
displaysurface = pygame.display.set_mode(fullscreen,pygame.RESIZABLE)
color = (222,222,0)
pygame.display.set_caption('NwablesGame')
Icon = pygame.image.load('share_card.png')
pygame.display.set_icon(Icon) 

#what is mousey doing
# 1. load the image then remove its background
# 2. resized image
# 3. goes hand in hand with convert alpha to remove background

def fetchimage(imagename,size):
    image = (pygame.image.load(imagename).convert_alpha())
    imageresized = pygame.transform.rotozoom(image,0,size)
    imageresized.set_colorkey("white")
    
    return imageresized

mouseup = fetchimage('Mouseup.png',0.25)
mousedown = fetchimage('Mousedown.png',0.25)
mouseleft = fetchimage('Mouseleft.png',0.25)
mouseright = fetchimage('Mouseright.png',0.25)
mousedead = fetchimage('Mousedead.png',0.25)
mousestop = fetchimage('Mousestop.png',0.25)
cheese = fetchimage('cheese.png',0.15)
instruction = fetchimage('feedthemouse.png',0.7)

# white background 

pygame.time.delay(1500)
pygame.Surface.fill(displaysurface,"white")
pygame.display.flip()

# add instruction

'''pygame.time.delay(1500)
displaysurface.blit(instruction,(0,0))
pygame.display.flip()

#back to white background

pygame.time.delay(1500)
pygame.Surface.fill(displaysurface,"white")
pygame.display.flip()'''

#make a subscreen
borderwidth = 3
paddingleft = 30
paddingright = 300
paddingabove = 30
paddingbelow = 60

arena = pygame.draw.rect(displaysurface,"black",pygame.Rect(paddingleft,paddingabove,(fullscreen[0]-paddingright),(fullscreen[1]-paddingbelow)),borderwidth)
pygame.display.flip() 

#starts here, ends here
parameters = {
    'horizontal':((paddingleft + borderwidth),(paddingleft + borderwidth + arena.width)), 
    'vertical':((paddingabove+borderwidth),(paddingabove + borderwidth + arena.height))
    
}

cheeseparameters = {
    'horizontal':((paddingleft + borderwidth + cheese.get_width() + 5),(paddingleft + borderwidth + arena.width - cheese.get_width() - 5)), 
    'vertical':((paddingabove+borderwidth + cheese.get_height() + 5),(paddingabove + borderwidth + arena.height - cheese.get_height() - 5))
    }


#cheese changes position

def elusivecheese():
    pygame.time.delay(80)
    displaysurface.fill("white")
    arena = pygame.draw.rect(displaysurface,"black",pygame.Rect(paddingleft,paddingabove,(fullscreen[0]-paddingright),(fullscreen[1]-paddingbelow)),borderwidth)
    pygame.display.flip()

    global a,b

    a = random.randrange(cheeseparameters['horizontal'][0],cheeseparameters['horizontal'][1])
    b = random.randrange(cheeseparameters['vertical'][0],cheeseparameters['vertical'][1])



a,b = (cheeseparameters['horizontal'][1] - cheese.get_width()),(paddingabove + 10)
x,y = 30,30

move_x,move_y = 0,0
img = mousestop
speed = 0.7

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move_x,move_y = 0,0
    img = mousestop

    if keys[pygame.K_UP]:
        img = mouseup
        move_y = -speed

    elif keys[pygame.K_DOWN]:
        img = mousedown
        move_y = +speed

    elif keys[pygame.K_RIGHT]:
        img = mouseright
        move_x = +speed

    elif keys[pygame.K_LEFT]:
        img = mouseleft
        move_x = -speed

    else:
        img = mousestop
        move_x = 0

    if keys[pygame.K_ESCAPE]:
        running = False    

    x += move_x
    y += move_y

# there is conflict between the parameters and where
#you are saying you want to be, and the parameters win

    x = max(parameters['horizontal'][0], min(x,parameters['horizontal'][1] - img.get_width()))
    y = max(parameters['vertical'][0], min(y,parameters['vertical'][1] - img.get_height()))


    displaysurface.fill("white")
    arena = pygame.draw.rect(displaysurface,"black",pygame.Rect(paddingleft,paddingabove,(fullscreen[0]-paddingright),(fullscreen[1]-paddingbelow)),borderwidth)
    mymouse = displaysurface.blit(img,(x,y))
    
    mycheese = displaysurface.blit(cheese,(a,b))
    pygame.display.flip()

       #Mouse eats cheese

    mouserect = pygame.Rect(x,y,img.get_width(),img.get_height())
    cheeserect = pygame.Rect(a,b,cheese.get_width(),cheese.get_height())

    def collision():
        return mouserect.colliderect(cheeserect)

    if collision():
        elusivecheese()
        
        #also add a points increase function
pygame.quit()