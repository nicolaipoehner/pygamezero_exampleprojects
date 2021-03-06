import random

# width and height of the world
WIDTH = 800
HEIGHT = 768

# the recell
car = Actor('car_red')
car.pos = WIDTH/2, HEIGHT/2

# barriers
barriers = []

# obstacles
cones = [] # when toching cones, they are pushed aside
oil = [] # when touching oil, the car spins
rocks = [] # when toching rocks, the game stops 

# speeds and chances of obstacles
# speeds
SPEED_CAR = 3
SPEED_CONES = 3
SPEED_OIL = 3
SPEED_ROCKS = 3
# chances
CHANCE_CONES = 1
CHANCE_OIL = 1
CHANCE_ROCKS = 1

# running variable and game over and countdown text
running = True
gameover = ""
countdown = 60.0

# draws the current frame 
def draw():
    screen.blit('road',(0,0))
    for b in barriers:
        b.draw()
    for c in cones:
        c.draw()
    for o in oil:
        o.draw()
    for r in rocks:
        r.draw()
    setupBarriers()
    car.draw()
    screen.draw.text(gameover, (WIDTH/2 - 150, HEIGHT/2), color="white", fontsize=50, align="center")
    screen.draw.text(str(countdown), (WIDTH/2 - 50, 25), color="white", fontsize=50, align="center")

# updates inbetween frames 
def update():
    if (running):    
        car.y += 1
        checkKeyboard()
        createAndUpdateCones()
        createAndUpdateOil()
        createAndUpdateRocks()
    else:
        clock.unschedule(resetCountdown)
       
# checks keyboard input 
def checkKeyboard():
    # check for clicks on keyboard to move the car
    if keyboard.left:
        car.angle = +5
        car.x -= SPEED_CAR
    elif keyboard.right:
        car.angle = -5
        car.x += SPEED_CAR
    elif keyboard.up:
        car.y -= SPEED_CAR
    elif keyboard.down:
        car.y += SPEED_CAR
    else:
        car.angle = 0
        
# initialises the barrier of the race track
def setupBarriers():
    for i in range(0, 6):
        barriers.append(Actor('barrier', (60, 64 + (i * 128))))
        barriers.append(Actor('barrier', (730, 64 + (i * 128))))
    
# create a update cones
def createAndUpdateCones():
    # create new cone 
    if(random.randint(0, 100) < CHANCE_CONES): # using a 1% chance
        x = random.randint(0, 400)
        cones.append(Actor('cone', (200 + x, 0)))
    # move the cones     
    for c in cones:
        c.y += SPEED_CONES
        # check for collision of the car and cones
        if(car.colliderect(c)):
            if(car.x > c.x):
                c.x -= 100
            else:
                c.x += 100
                
# create a update oil
def createAndUpdateOil():
    # create new cone 
    if(random.randint(0, 100) < CHANCE_OIL): # using a 1% chance
        x = random.randint(0, 400)
        oil.append(Actor('oil', (200 + x, 0)))
    # move the oil     
    for o in oil:
        o.y += SPEED_OIL
        # check for collision of the car and oil
        if(car.colliderect(o)):
            spin()
            
# makes the car spin
def spin():
    car.y -= 10
    car.angle -= random.randint(-180, 180)
    
# create and update rocks
def createAndUpdateRocks():
    global running, gameover
    # create new rock 
    if(random.randint(0, 100) < CHANCE_ROCKS): # using a 1% chance
        x = random.randint(0, 400)
        rocks.append(Actor('rock', (200 + x, 0)))
    # move the rocks     
    for r in rocks:
        r.y += SPEED_ROCKS
        # check for collision of the car and rocks
        if(car.colliderect(r)):
            # stop game
            gameover = "Game over! \n You hit a rock!"
            running = False
            
# reset the countdown text on the display each second
def resetCountdown():
    global countdown, gameover, running
    if(countdown > 0.0):
        countdown -= 1.0
    else:
        countdown = 0.0
        gameover = "Game over! \n You won!"
        running = False

# use the pgzero clock to call the resetCountdown() regulary each second 
clock.schedule_interval(resetCountdown, 1.0)
