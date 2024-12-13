import pygame
import random
import sys

pygame.init()

#background

fullscreen = (1366,710)
displaysurface = pygame.display.set_mode(fullscreen,pygame.RESIZABLE)
color = (222,222,0)
pygame.display.set_caption('Mousey')

# 1. load the image then remove its background
# 2. resized image
# 3. uses convert alpha to remove background

def fetchimage(imagename,size):
    image = (pygame.image.load(imagename).convert_alpha())
    imageresized = pygame.transform.rotozoom(image,0,size)
    imageresized.set_colorkey("white")
    
    return imageresized

#what is mousey doing

mouseup = fetchimage('assets/Mouseup.png',0.25)
mousedown = fetchimage('assets/Mousedown.png',0.25)
mouseleft = fetchimage('assets/Mouseleft.png',0.25)
mouseright = fetchimage('assets/Mouseright.png',0.25)
mousedead = fetchimage('assets/Mousedead.png',0.25) 
mousestop = fetchimage('assets/Mousestop.png',0.25)
cheese = fetchimage('assets/peanutbutter.png',0.35)
instruction = fetchimage('assets/feedthemouse.png',0.75)
catup = fetchimage('assets/catup.png',0.25)
catdown = fetchimage('assets/catdown.png',0.25)
catright = fetchimage('assets/catright.png',0.25)
catleft = fetchimage('assets/catleft.png',0.25)

Icon = fetchimage('assets/Mousestop.png',1)
pygame.display.set_icon(Icon)

# white background 

pygame.time.delay(700)
pygame.Surface.fill(displaysurface,"white")
displaysurface.blit(instruction,(0,-55))
pygame.display.flip()

# onto game

pygame.time.delay(8000)
pygame.Surface.fill(displaysurface,"white")
pygame.display.flip()

#make a subscreen
borderwidth = 3
paddingleft = 30  
paddingright = 300 
paddingabove = 30 
paddingbelow = 60 

#create an arena to play in
def createarena():
    
    arena = pygame.draw.rect(displaysurface,"white",pygame.Rect(paddingleft,paddingabove,(fullscreen[0]-paddingright),(fullscreen[1]-paddingbelow)))
    arena = arena.inflate(borderwidth*2, borderwidth*2)
    pygame.draw.rect(displaysurface, "black", arena, borderwidth)

#arena parameters

arenawidth = fullscreen[0]-paddingright-paddingleft
arenaheight = fullscreen[1]-paddingbelow-paddingabove

#rightspace parameters

rsleft = paddingleft + arenawidth + 45
rsright = fullscreen[0]
rstop = paddingabove
rsbottom = fullscreen[1]
rsmiddle = (fullscreen[0] - paddingright) + (paddingright/2)

#create points block

score = 0

def createpointsystem():

    gap = 10
    
    scoreboard = str(score)
    scoreboard2 = str((score)) #score for now but the maximum!!!!!!!!

    def scores(text,texttop):
    #set font
        fontsize = 50
        sansserif = pygame.font.SysFont('Sans-serif',fontsize)

        scoretext = (sansserif.render(text,True,"black"))
        scorewhere = scoretext.get_rect(center = (rsmiddle,(texttop + fontsize/2)))
        displaysurface.blit(scoretext,scorewhere)

    def scoreblocks(howfardown,whichscore):
        fontsize = 100
        sansserif = pygame.font.SysFont('Sans-serif',fontsize)

        blockwidth = paddingright-60
        blockheight = 210

        theblock = pygame.draw.rect(displaysurface,"gray",pygame.Rect(rsleft,(rstop + howfardown),blockwidth,blockheight))
        theblock = theblock.inflate(borderwidth*2,borderwidth*2)
        pygame.draw.rect(displaysurface, "white", theblock,borderwidth)
        blocktext = (sansserif.render(whichscore,True,"black"))
        blocktextcenter = blocktext.get_rect(center = theblock.center)
        displaysurface.blit(blocktext,blocktextcenter)


    scores('MYSCORE',rstop)
    scoreblocks((rstop + 50 + gap),scoreboard)
    scores('HIGHSCORE', (rstop + gap + gap + gap + 50 + gap + 210 + gap + gap))
    scoreblocks((gap + rstop + 50 + gap + 210 + gap + 50 + gap + gap + gap + gap),scoreboard2)

def addtoscore():
    
    global score

    score += 5
    return score


pygame.display.flip() 

#starts here, ends here
# parameters for mousey to stay in 

parameters = {
    'horizontal':((paddingleft + borderwidth),(paddingleft + borderwidth + arenawidth)), 
    'vertical':((paddingabove+borderwidth),(paddingabove + borderwidth + arenaheight))
    
}

cheeseparameters = {
    'horizontal':((paddingleft + borderwidth + cheese.get_width() + 5),(paddingleft + borderwidth + arenawidth - cheese.get_width() - 5)), 
    'vertical':((paddingabove+borderwidth + cheese.get_height() + 5),(paddingabove + borderwidth + arenaheight - cheese.get_height() - 5))
    }

#cheese changes position


def elusivecheese():
    pygame.time.delay(80)
    displaysurface.fill(pygame.Color('#90D5FF'))
    
    createarena()
    createpointsystem()

    pygame.display.flip()

    a = random.randrange(cheeseparameters['horizontal'][0],cheeseparameters['horizontal'][1])
    b = random.randrange(cheeseparameters['vertical'][0],cheeseparameters['vertical'][1])
    
    return a,b

def main():

    a,b = (cheeseparameters['horizontal'][1] - cheese.get_width()),(paddingabove + 10)

    x,y = 30,30

    move_x,move_y = 0,0
    img = mousestop
    speed = 3


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
    #you are saying you want to be, and the parameters win (keeping within the parameters)

        x = max(parameters['horizontal'][0], min(x,parameters['horizontal'][1] - img.get_width()))
        y = max(parameters['vertical'][0], min(y,parameters['vertical'][1] - img.get_height()))


        displaysurface.fill(pygame.Color('#ADD8E6'))
        arena = createarena()
        pointsblock = createpointsystem()

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
            addtoscore()
            
            #also add a high score remembering function
            #maybe add some music?
    pygame.quit()

if __name__ == "__main__":
    main()