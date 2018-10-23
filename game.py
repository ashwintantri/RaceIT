import pygame
import time
import random

pygame.init() #initiate pygame,necessary for every application made with pygame

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

car_width = 73 #location of top left pixel of the car(image)

gameDisplay = pygame.display.set_mode((display_width,display_height)) #canvas for displaying objects
pygame.display.set_caption('RaceIT') #name of the game
clock = pygame.time.Clock() #track time in the game (frames)

carImg = pygame.image.load('racecar.png') #load car image
def quitgame():
    pygame.quit()
    quit()
def things(thingx, thingy, thingw, thingh, color):      #to create obstacles
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):                   #places car on the display
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font): #to create text objects, which give us rectangle for text to diplayed
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2)) #centering display message
    gameDisplay.blit(TextSurf, TextRect) #to show anything on screen,blit is used
    pygame.display.update()

    time.sleep(2)

    game_loop()
    
    

def crash(score):
    message_display('You Crashed!')
    
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() #handle clicks
    print(click) #track clicks in terminal
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #if mouse hovered, change color of button
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h)) 
        if click[0] == 1 and action != None:
            action() #passed in function call,whether to play, or to exit         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h)) #if mouse not hover, create button as it is

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect) #display button on screen
def game_intro(): #like start menu

    intro = True
    red = (200,0,0)
    green = (0,200,0)
    bright_red = (255,0,0)
    bright_green = (0,255,0)


    while intro: 
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT: #show until quit is pressed
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("RaceIT", largeText) #display game name
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        pygame.display.update()
        clock.tick(15)
def game_loop():
    x = (display_width * 0.45) #starting point
    y = (display_height * 0.8)  #starting point

    thingCount = 1

    dodged = 0
    x_change = 0 #controls positon of car object, in x direction

    thing_startx = random.randrange(0, display_width) # generate obstacles randomly in x direction
    thing_starty = -600 # set because player has some time to dodge the obstacle
    thing_speed = 7 #pixels moved per second
    thing_width = 100
    thing_height = 100

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: #when key is pressed
                if event.key == pygame.K_LEFT: #when key pressed is left key
                    x_change = -5
                if event.key == pygame.K_RIGHT: #when key pressed is right key
                    x_change = 5

            if event.type == pygame.KEYUP: #when any key is released 
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change #calculate position of car in x direction
        gameDisplay.fill(white) #set background to white,to be done before drawing the car

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)


        if x > display_width - car_width or x < 0: #1st condition,edge case for extreme right side,2nd for left side 
            crash(thingCount)

        if thing_starty > display_height: #from top to bottom, if greater, create new block
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1 #increase doged obstacle count
            thing_speed+=1 #when dodged increase speed gradually
            thing_width += (dodged*1.2) #to increase difficulty, width of obstacle is increased

        ####
        if y < thing_starty+thing_height: #car's top left has crossed object's bottom left
            print('y crossover')
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash(thingCount)
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()