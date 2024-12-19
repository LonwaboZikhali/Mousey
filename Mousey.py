import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

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
thecat = fetchimage('assets/thecat.png',0.15)
gameover = fetchimage('assets/gameover.png',0.72)

Icon = fetchimage('assets/Mousestop.png',1)
pygame.display.set_icon(Icon)

# white background 

pygame.time.delay(700)
pygame.Surface.fill(displaysurface,"white")
displaysurface.blit(instruction,(0,-55))
pygame.display.flip()

# onto the game

pygame.time.delay(1000)
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

# score area space parameters

rsleft = paddingleft + arenawidth + 45
rsright = fullscreen[0]
rstop = paddingabove
rsbottom = fullscreen[1]
rsmiddle = (fullscreen[0] - paddingright) + (paddingright/2)

#create points block

score = 0

def createpointsystem():

    gap = 10
    
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

    def scoring_system():
        
        global score

        with open("assets/highscore.txt","r",errors="ignore") as file:
            highscore = file.read()

        if score > int(highscore)  or highscore == '':
            with open("assets/highscore.txt","w",errors="ignore") as file:
                file.write(str(score))

        if score > int(highscore)  or highscore == '':
            with open("assets/highscore.txt","w",errors="ignore") as file:
                file.write(str(score))
        else:
            pass

        return highscore

    scoring_system()

    scoreboard = str(score)
    scoreboard2 = str((scoring_system()))

# the score and its block

    scores('MYSCORE',rstop)
    scoreblocks((rstop + 50 + gap),scoreboard)
    scores('HIGHSCORE', (rstop + 260 + 6*gap))
    scoreblocks(( rstop + 310 + 7*gap),scoreboard2)

def addtoscore():
    
    global score

    score += 5
    return score


pygame.display.flip() 

#starts here, ends here
# parameters for mousey to stay in 

parameters = {
    'horizontal':((paddingleft  + borderwidth),(paddingleft + borderwidth + arenawidth)), 
    'vertical':((paddingabove+borderwidth),(paddingabove + borderwidth + arenaheight))
    
}

cheeseparameters = {
    'horizontal':((paddingleft + borderwidth + cheese.get_width() + 5),(paddingleft + borderwidth + arenawidth - cheese.get_width() - 5)), 
    'vertical':((paddingabove + borderwidth + cheese.get_height() + 5),(paddingabove + borderwidth + arenaheight - cheese.get_height() - 5))
    }

# down for now

def startmenu():
    pygame.Surface.fill(displaysurface,"white")
    pygame.draw.rect(displaysurface,"pink",pygame.Rect(0,0,fullscreen[0],fullscreen[1]))
    pygame.display.flip()
    pygame.time.delay(8000)

def main():

    x,y = 30,30
    a,b = (cheeseparameters['horizontal'][1] - cheese.get_width()),(paddingabove + 10)
    t,v = 30,((parameters['vertical'][1]) - thecat.get_height())

    move_x,move_y = 0,0
    img = mousestop
    xyspeed = 3

    # music
    pygame.mixer.music.load("assets/A Desktop Homepage Theme.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.07)
    bing = pygame.mixer.Sound("assets/BING.mp3")
    wrong = pygame.mixer.Sound("assets/wrong.mp3")

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
            move_y = -xyspeed

        elif keys[pygame.K_DOWN]:
            img = mousedown
            move_y = +xyspeed

        elif keys[pygame.K_RIGHT]:
            img = mouseright
            move_x = +xyspeed

        elif keys[pygame.K_LEFT]:
            img = mouseleft
            move_x = -xyspeed

        else:
            img = mousestop
            move_x = 0

        if keys[pygame.K_ESCAPE]:
            running = False    

        x += move_x
        y += move_y
         

    # there is conflict between the parameters and where
    # you are saying you want to be, and the parameters win (keeping within the parameters)

        x = max(parameters['horizontal'][0], min(x,parameters['horizontal'][1] - img.get_width()))
        y = max(parameters['vertical'][0], min(y,parameters['vertical'][1] - img.get_height()))
 

        displaysurface.fill(pygame.Color('#ADD8E6'))
        arena = createarena()
        pointsblock = createpointsystem()

        mymouse = displaysurface.blit(img,(x,y))
        mycat = displaysurface.blit(thecat,(t,v))
        mycheese = displaysurface.blit(cheese,(a,b))

        pygame.display.flip()

        #Mouse eats cheese
        #cheese changes position
        
        def the_cat_follows(x,y,t,v): 

            tvspeed = 0.7

            distance_between_x = x - t
            distance_between_y = y - v

            if distance_between_x > 0:
                t += tvspeed
            elif distance_between_x < 0:
                t -= tvspeed
            else:
                pass
            if distance_between_y > 0:
                v += tvspeed
            elif distance_between_y < 0:
                v -= tvspeed
            else:
                pass

            return t,v

        t,v = the_cat_follows(x,y,t,v)

        def elusivecheese():
            """cheese moves to a new random location"""

            pygame.time.delay(80)
            pygame.display.flip()

            global a,b

            a = random.randrange(cheeseparameters['horizontal'][0],cheeseparameters['horizontal'][1])
            b = random.randrange(cheeseparameters['vertical'][0],cheeseparameters['vertical'][1])      

            return a,b      

        def mousecheesecollision():
            """returns a boolean that tells us whether the cheese and mouse are colliding."""

            mouserect = pygame.Rect(x,y,img.get_width(),img.get_height())
            cheeserect = pygame.Rect(a,b,cheese.get_width(),cheese.get_height())
            
            return mouserect.colliderect(cheeserect)

        def mousecatcollision():
            catrect = pygame.Rect(t,v,thecat.get_width(),thecat.get_height())
            mouserect = pygame.Rect(x,y,img.get_width(),img.get_height())

            return catrect.colliderect(mouserect)

        if mousecheesecollision():
            bing.play()
            a,b = elusivecheese()
            addtoscore()
        else:
            pass
    
        if mousecatcollision():
            wrong.play()
            displaysurface.blit(gameover,(0,-20))
            pygame.display.flip()
            pygame.time.delay(1000)
            running = False

    pygame.quit()

if __name__ == "__main__":

    # startmenu()
    main()