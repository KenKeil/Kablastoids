# Kenneth Keil
# Space.pygame

# Imports
import pygame
import random
import time
import os
import ast


###################################################################################################
# Set screen placement 
xwin = 0
ywin = 0  
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" %(xwin, ywin)

# Eliminates sound latency
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Variables to store and set dimensions of window
screenWidth = 500
screenHeight = 650
win = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)

# Name of window
pygame.display.set_caption("Space")

# Initialize Clock
clock = pygame.time.Clock()

###################################################################################################               
# Called from Title
# Passes in boolean for One Player or Two Player
# Passes in High Score list, with the top score
# Passes in name to add to high score list            
def play(twoP, highscores, toBeat, name):

    # Set screen placement 
    xwin = 0
    ywin = 0  
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" %(xwin, ywin)

    # Eliminates sound latency
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # Variables to store dimensions of window
    screenWidth = 500
    screenHeight = 650
    win = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)

    # Name of window
    pygame.display.set_caption("Space")

    # Initialize Clock
    clock = pygame.time.Clock()

    # Sets mouse visability off
    pygame.mouse.set_visible(False)

    # Loads images used in game
    bg = pygame.image.load('./Images/Background.png')
    Ship = pygame.image.load('./Images/Player1.png')
    # Different colored ship loaded if two players
    if twoP:
        Ship2 = pygame.image.load('./Images/Player2.png')
    if not twoP:
        Ship2 = pygame.image.load('./Images/no2P.png')
    En = pygame.image.load('./Images/Enemy.png')
    SpecEn = pygame.image.load('./Images/SpecialEn.png')
    Shield1 = pygame.image.load('./Images/Shield1.png')
    Shield2 = pygame.image.load('./Images/Shield2.png')


    # Load Sounds
    highscoreSound  = pygame.mixer.Sound('./Sounds/highscore.wav')
    bulletSound     = pygame.mixer.Sound('./Sounds/pew.wav')
    enBulletSound   = pygame.mixer.Sound('./Sounds/pew2.wav')
    hitSound        = pygame.mixer.Sound('./Sounds/crash.wav')
    gameoverSound   = pygame.mixer.Sound('./Sounds/ohno.wav')
    diffUpSound     = pygame.mixer.Sound('./Sounds/difficultyUp.wav')
    respawnSound    = pygame.mixer.Sound('./Sounds/Respawn.wav')
    camper          = pygame.mixer.Sound('./Sounds/Camper.wav')
    warningSound    = pygame.mixer.Sound('./Sounds/Warning.wav')
    shieldSound     = pygame.mixer.Sound('./Sounds/Shield.wav')
    loseShieldSound = pygame.mixer.Sound('./Sounds/LoseShield.wav')
    specEnSound     = pygame.mixer.Sound('./Sounds/SpecEn.wav')

    #Font Size = 25
    font = pygame.font.SysFont(None, 25)

    # Initalizing Variables
    bulletsP1   = [] # List of fired bullets
    bulletsP2   = []  
    shootLoopP1 = 0  # Prevents firing multiple bullets in one click
    shootLoopP2 = 0
    allowedBulsP1 = 5 # Number of bullets allowed to be fired
    allowedBulsP2 = 5
    score = 0  # Score to be appended to highscore list
    dist = 0   # How far player has traveled
    enShots = 0 # Frequency multiplier for how often enemies shoot
    enemyList = [] # List of enemies
    enBullets = [] # List of enemy bullets
    allowedEns = 2 # Number of enemies allowed to spawn at once
    diff = 7 # Difficulty multiplier that effects variables such as speed
    nextDiff = 500 # Distance required before player levels up
    shootDiff = 1000 # Distance required before enemies begin shooting
    gameover = False # Bool to test if game is over
    allowShots = False # Variable that enables enemies to fire shots
    highScoreCheck = True # Checks if player passes high score. If omitted,
                          # High score noises continually plays every frame after
                          # Setting a new high score. Very annoying.
    run = True # Variable that allows game to run
    moveLeft = False   # Variables to check if player is currently moving in a direction
    moveRight = False
    canBoost = False # Variable that allows player to use speed boost
    canShoot = False # Variable that checks if the player can shoot
    hasMoved1 = True # Variable to check if player 1 has moved recently
    campSafe1 = True # Variable to check if player 1 has stopped moving for a while
    hasMoved2 = True
    campSafe2 = True
   
    ###################################################################################################                
    # Game Over              
    def show_gameover():
        win.blit(bg, (0,0))
        # Draw text, distance and score
        screen_text = font.render("Game Over!", True, (255,255,255)) 
        win.blit(screen_text, (200,250))
        screen_text2 = font.render("Distance: " + str(dist), True, (255,255,255))
        win.blit(screen_text2, (200,300))
        screen_text3 = font.render("Score: " + str(score), True, (255,255,255))
        win.blit(screen_text3, (200,350))
        for enemy in enemyList: # Draw all enemies
            enemy.draw(win)
        if player1.respawn > player2.respawn: # Only draw P1
            player1.draw(win)
        if player1.respawn < player2.respawn: # Only draw P2
            player2.draw(win)
        for bullet in bulletsP1: # Draw all P1 bullets
            bullet.draw(win)
        for bullet in bulletsP2: # Draw all P2 bullets
            bullet.draw(win)
        for bullet in enBullets: # Draw all enemy bullets
            bullet.draw(win)
        # Checks is previous scores have been entered
        if len(highscores) > 0:
            i = 0
            # Checks if high score
            if score > toBeat:
                screen_text4 = font.render("New High Score!", True, (255,255,255))
                win.blit(screen_text4, (200,400))
            else:
                screen_text5 = font.render("Current High Score:", True, (255,255,255))
                win.blit(screen_text5, (200,400))
                nameIndex = highscores[0][1]
                i = 0
                # Prints top score to beat
                for x in highscores:
                    if x[1] > nameIndex:
                        i = highscores.index(x)
                        nameIndex = x[1]
                topScore = highscores[i][0]
                screen_text6 = font.render((topScore + ': ' + str(toBeat)), True, (255,255,255))
                win.blit(screen_text6, (200, 450))
        # Writes top score to file
        f = open('Highscore.txt', 'w+')
        for x in highscores:
            f.write(str(x) + '\n')
        scorewrite = [name, score]
        f.write(str(scorewrite) + '\n')
        f.close()
        pygame.display.update()
        waiting = True
        i = 0
        # Briefly waits before accepting input to return to title screen
        while waiting:
            clock.tick(30)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT and i > 5:
                    pygame.quit()
                if event.type == pygame.KEYUP and i > 5:
                    title()
                i += 1
                
    ###################################################################################################               
    # Function to display text                
    def text(msg,color):
        screen_text = font.render(msg, True, color)
        win.blit(screen_text, (200,10))
        pygame.display.update()
        
    ###################################################################################################   
    # Character Creation
    # Passes in location, size, speed, image, if they're alive or not, if they are boosting,
    # if they can boost, the speed they move at while boosting, and if its P1 or P2
    class player(object):
        def __init__(self, x, y, width, height, vel, img, alive, boost, canBoost, boostVel, name):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = vel
            self.left = False
            self.right = True
            self.hitbox = (self.x, self.y, 42, 40)
            self.img = img
            self.alive = alive
            self.respawn = 0
            self.boost = boost
            self.boostbar = 100
            self.canBoost = canBoost
            self.boostVel = boostVel
            self.name = name
        
        # Draws player to screen
        def draw(self,win):
            win.blit(self.img, (self.x,self.y))
            self.hitbox = (self.x, self.y, 42, 40)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # Used to debug hitbox errors
            # Draws boost bar
            if self.name == 1:
                if self.boost:
                    if self.boostbar > 0:
                        self.boostbar -= 1
                    if self.boostbar <= 0:
                        self.canBoost = False
                        self.boost = False
                        self.vel = diff
                else:
                    if self.boostbar > 100:
                        self.boostbar = 100
                    if self.boostbar < 100:
                        self.boostbar += 1.5
                        self.canBoost = True
                pygame.draw.rect(win, (255,0,0), (10,10, 100, 10))
                pygame.draw.rect(win, (0,0,255), (10,10, self.boostbar, 10))
            if self.name == 2:
                if self.boost:
                    if self.boostbar > 0:
                        self.boostbar -= 1
                    if self.boostbar <= 0:
                        self.canBoost = False
                        self.boost = False
                        self.vel = diff
                else:
                    if self.boostbar > 100:
                        self.boostbar = 100
                    if self.boostbar < 100:
                        self.boostbar += 1.5
                        self.canBoost = True
                pygame.draw.rect(win, (255,0,0), (390,10, 100, 10))
                pygame.draw.rect(win, (0,255,0), (390,10, self.boostbar, 10))       
            pygame.display.update()
            
        # Checks all hitboxes with enemies to detect collision    
        def checkhit(self):
            i = 0
            while i < len(enemyList):
                if (self.y - (self.height /2) < enemyList[i].hitbox[1] + enemyList[i].hitbox[3]/2 and
                    self.y + (self.height /2) > enemyList[i].hitbox[1] - enemyList[i].hitbox[3]/2):
                    if (self.x + (self.width /2) > enemyList[i].hitbox[0] - enemyList[i].hitbox[2]/2 and
                        self.x - (self.width / 2) < enemyList[i].hitbox[0] + enemyList[i].hitbox[2]/2):

                        # Checks if shield was activate or not
                        if self.img == Ship or self.img == Ship2:
                            self.alive = False
                            self.respawn = dist + 500
                            gameoverSound.play()
                            enemyList.pop(enemyList.index(enemyList[i]))
                        if self.img == Shield1:
                            loseShieldSound.play()
                            self.img = Ship
                            enemyList.pop(enemyList.index(enemyList[i]))
                        if self.img == Shield2:
                            loseShieldSound.play()
                            self.img = Ship2
                            enemyList.pop(enemyList.index(enemyList[i]))  
                i += 1
            return True
            
    ###################################################################################################
    # Defines bullets
    # Location, size, color, direction, and velocity are all needed
    class projectile(object):
        def __init__ (self, x, y, radius, color, dir, vel):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.vel = vel
            self.dir = dir
        
        # Draws bullet to screen
        def draw(self,win):
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
            
    ###################################################################################################        
    # Creates enemies
    # Gives them a location, size, horizontal distance for if they Zigzag, speed, 
    # if they can shoot, how frequent they shoot, and if they are a special enemy (grants shield/respawns
    # dead player)
    class enemy(object):
        def __init__(self, x, y, width, height, end, vel, allowShots, enShots, special):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = vel
            self.left = True
            self.right = False
            self.end = end
            # Used if enemy zig zags
            if self.x > self.end:
                self.path = [self.end, self.x]
            else:
                self.path = [self.x, self.end]
            self.hitbox = (self.x, self.y, 42, 40)
            self.allowShots = allowShots
            self.enShots = enShots
            self.special = special
        
        # Draws enemy to screen
        def draw(self,win):
            self.move() # Calls function to move enemy
            self.shoot(self.allowShots, self.enShots) # Calls function for enenmies to shoot
            if self.special: # Checks whether enemy color needs to be changed
                win.blit(SpecEn, (self.x, self.y))
            else:
                win.blit(En, (self.x, self.y))
            self.hitbox = (self.x, self.y, 42, 40)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # Used to debug misplaced hitbox
        
        # Function for enemy shots
        def shoot(self, allowShots, enShots): 
            # Checks if can shoot
            if enShots == 0:
                self.allowShots = False
            # If can shoot, apply multiplier and shoot any time a random number from
            # 100*multipler to 1000 is above 975
            if self.allowShots:
                if enShots < 10:
                    randShot = random.randint(enShots*100,1000)
                    if randShot > 975:
                        enBulletSound.play()
                        enBullets.append(projectile(round(self.x + self.width-2), 
                                                    self.y, 5, (255,0,0), -1, round(diff + 5)))
                else:
                    bulletSound.play()
                    enBullets.append(projectile(round(self.x + self.width-2), 
                                                self.y, 5, (255,0,0), -1, round(diff + 5)))
        # Moves enemy                                  
        def move(self):
            if self.y < screenHeight: # If enemy is still on screen, move it
                self.y += abs(self.vel)
            else: # If enemy is off screen, delete it
                enemyList.pop(enemyList.index(self))
            if self.vel > 0: # Used to zig zag enemy
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    
        # Called when player bullet hits enemy. Deletes enemy             
        def hit(self):
            enemyList.pop(enemyList.index(self))
            
    ###################################################################################################
    # Function to redraw elements on screen       
    def redrawGameWindow():
        win.blit(bg, (0,0))
        text("Score: " + str(score), (255,255,255))
        for enemy in enemyList:
            enemy.draw(win)
        if player1.alive:
            player1.draw(win)
        if player2.alive:
            player2.draw(win)
        for bullet in bulletsP1:
            bullet.draw(win)
        for bullet in bulletsP2:
            bullet.draw(win)    
        for bullet in enBullets:
            bullet.draw(win)
        pygame.display.update()

    # Checks if a USB controller is connected    
    try:
        j = pygame.joystick.Joystick(0)
        pygame.joystick.init()   
        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            joysticks.append(pygame.joystick.Joystick(i))
            # initialize them all (-1 means loop forever)
            joysticks[-1].init()  
    except:
        pass
    ###################################################################################################   

    # Creates players
    player1 = player(0,600, 42, 40, diff, Ship, True, False, True, diff*2, 1)
    # Adds second player if two player mode, adds empty player if not
    if twoP:
        player2 = player(460,600, 42, 40, diff, Ship2, True, False, True, diff*2, 2)
    if not twoP:
        player2 = player(1000,1000, 0, 0, 0, Ship2, False, False, False, 0, 2)
    
    # The run variable updates once a frame, checking and updating the screen
    # run will always be true, unless a condition occurs that causes the game to end
    while run:
        
        # If 1P mode, Player 2 isn't drawn
        if not twoP:
            player2.alive = False
        
        # If both players are dead, end the game
        if player1.alive == False and player2.alive == False:
            show_gameover()
        
        # Respawns player 1 if Player 2 survives long enough
        if (dist > player1.respawn) and player1.alive == False:
            respawnSound.play()
            player1.alive = True
            NoMoveGoal1 += 100
            player1.boostbar = 100
        
        # In two player mode, respawns player 2 if player 1 survives long enough
        if twoP:
            if dist > player2.respawn and player2.alive == False:
                respawnSound.play()
                player2.alive = True
                NoMoveGoal2 += 100
                player2.boostbar = 100
                
        # Checks if the high score is beat. If it is, no need to continue checking,
        # as highscoreSound.play() will play EVERY frame afterwords 
        if highScoreCheck:
            if score > toBeat:
                highscoreSound.play()
                highScoreCheck = False
       
        # Checks if the player 'levels up'
        if dist > nextDiff:
            if name.lower() == "hard": # Naming yourself 'hard' increases the difficulty right away
                allowedEns += 1
                allowShots = True
                diff = diff*1.05
            diffUpSound.play()
            diff = diff * 1.15 # adds to the difficulty multiplier
            nextDiff += 500 # Sets the next level up 500 frames away
            allowedEns += 1 # One more enemy is allowed to spawn
            player1.vel += 1 # Your speed is increased to accomodate for increased difficulty
            player2.vel += 1
            allowedBulsP1 += 1 # Number of shots you can shoot at once is increased to accomodate
            allowedBulsP2 += 1
            if dist > shootDiff: # If your distance meets the requirements, enemies can begin shooting
                enShots += 1
                allowShots = True
                
        # Adds slight variance to the speed enemies move at        
        enVel = (random.randint(round(diff) - 1, round(diff) + 1))
        
        # Checks if max enemies have been spawned
        if len(enemyList) < allowedEns: 
            if random.randint(0,10) >= 9: #10 % chance an enemy will spawn directly above the player
                                          # and not move. Helps counter corner campers
                if player1.alive and player2.alive:
                    if random.randint(1,2) == 1:
                        pointA = player1.x + 7
                        pointB = player1.x + 7
                    else:
                        pointA = player2.x + 7
                        pointB = player2.x + 7
                elif player1.alive:
                    pointA = player1.x + 7
                    pointB = player1.x + 7
                elif player2.alive:
                    pointA = player2.x + 7
                    pointB = player2.x + 7  
            else:   # 90 % chance enemies spawn in random location
                NoWiggle = False
                if random.randint(0,1) == 1:    # 50/50 chance enemies zig zag
                    NoWiggle = True
                
                pointA = random.randint(0,screenWidth-35) # sets two points for enemy to bounce between
                pointB = random.randint(0,screenWidth-35)
                
                if dist < 500: # Enemies can't zig zag in level 1
                    NoWiggle = True
                
                if NoWiggle:
                    pointB = pointA
            
            if random.randint(0,100) > 96:  # 4% chance a special enemy spawns
            # Special enemies grant shield upon destruction, and bring back dead players
                if not (player1.img == Shield1 and (player2.img == Shield2 or player2.img == Ship2)):
                    enemyList.append(enemy(pointA, 0, 24, 44, pointB, enVel, allowShots, enShots, True))
                    specEnSound.play() # Plays sound to notify a special enemy has been spawned
            else:
                enemyList.append(enemy(pointA, 0, 24, 44, pointB, enVel, allowShots, enShots, False))
        
        # 0.05 seconds between updates (20 FPS)
        score += 1
        dist += 1
        clock.tick(30)

        # Shoot loop prevents multiple bullets from accidetnally firing from one input.
        # 3 frames must pass before another bullet may be fired
        if shootLoopP1 > 0:
            shootLoopP1 += 1
        
        if shootLoopP1 > 3:
            shootLoopP1 = 0
            
        if shootLoopP2 > 0:
            shootLoopP2 += 1
        
        if shootLoopP2 > 3:
            shootLoopP2 = 0    
        
        # Get list of all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.JOYAXISMOTION: # Checks joystick movement
                if j.get_axis(0) >= 0.5: # Pressing right
                    moveRight = True
                    moveLeft = False
                if j.get_axis(0) <= -1: # Pressing Left
                    moveLeft = True
                    moveRight = False
                if j.get_axis(0) < 0 and j.get_axis(0) >= -0.5: # No direction
                    moveLeft = False
                    moveRight = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button < 4: # First 4 buttons (A, B, X and Y) shoot
                    canShoot = True
                if event.button == 4 or event.button == 5: # Bumpers boost
                    canBoost = True
            if event.type == pygame.JOYBUTTONUP: # Checks when buttons have been released
                if event.button < 4:
                    canShoot = False
                if event.button == 4 or event.button == 5:
                    canBoost = False

        if player1.alive and name != 'God': # Naming yourself "God" makes you invinsible
            player1.checkhit()
        if twoP:
            if player2.alive:
                player2.checkhit()
        
        # Draws bullets and moves if on screen. Deletes if off screen       
        for bullet in bulletsP1:
            if bullet.y > 0:
                bullet.y -= bullet.vel*bullet.dir
            else:
                bulletsP1.pop(bulletsP1.index(bullet))
                
        for bullet in bulletsP2:
            if bullet.y > 0:
                bullet.y -= bullet.vel*bullet.dir
            else:
                bulletsP2.pop(bulletsP2.index(bullet))            
        
        # Loop that checks all bullets, and checks when they collider with enemy hitboxes
        for bullet in bulletsP1:
            i = 0
            while i < len(enemyList):
                if (bullet.y - bullet.radius < enemyList[i].hitbox[1] + enemyList[i].hitbox[3] and
                    bullet.y + bullet.radius > enemyList[i].hitbox[1]):
                    if (bullet.x + bullet.radius > enemyList[i].hitbox[0] and
                        bullet.x - bullet.radius < enemyList[i].hitbox[0] + enemyList[i].hitbox[2]):
                        hitSound.play()
                        if enemyList[i].special: # Special bonuses applied to special enemy deaths
                            score += 100
                            shieldSound.play()
                            player1.img = Shield1
                            if player1.alive == False or player2.alive == False:
                                respawnSound.play()
                                player1.alive = True
                                if twoP:
                                    player2.alive = True
                                NoMoveGoal1 += 100
                                NoMoveGoal2 += 100
                        enemyList[i].hit()
                        try:
                            bulletsP1.pop(bulletsP1.index(bullet)) 
                        except:
                            pass
                        score += 50
                i += 1
                
        for bullet in bulletsP2:
            i = 0
            while i < len(enemyList):
                if (bullet.y - bullet.radius < enemyList[i].hitbox[1] + enemyList[i].hitbox[3] and
                    bullet.y + bullet.radius > enemyList[i].hitbox[1]):
                    if (bullet.x + bullet.radius > enemyList[i].hitbox[0] and
                        bullet.x - bullet.radius < enemyList[i].hitbox[0] + enemyList[i].hitbox[2]):
                        hitSound.play()
                        if enemyList[i].special:
                            score += 100
                            shieldSound.play()
                            player2.img = Shield2
                            if player1.alive == False or player2.alive == False:
                                respawnSound.play()
                                player1.alive = True
                                if twoP:
                                    player2.alive = True
                        enemyList[i].hit()
                        bulletsP2.pop(bulletsP2.index(bullet)) 
                        score += 50
                i += 1            
        
        # Checks enemy bullets to see if they collider with either player
        for bullet in enBullets:
            if bullet.y < screenHeight:
                bullet.y -= bullet.vel*bullet.dir
            else:
                enBullets.pop(enBullets.index(bullet))    
            
            # Checks collision with P1
            if (bullet.y - bullet.radius < player1.hitbox[1] + player1.hitbox[3] and
                    bullet.y + bullet.radius > player1.hitbox[1] and player1.alive):
                    if (bullet.x + bullet.radius > player1.hitbox[0] and
                        bullet.x - bullet.radius < player1.hitbox[0] + player1.hitbox[2]):
                        hitSound.play()
                        if player1.img == Ship: # Kills enemy if no shield
                            player1.respawn = dist+500
                            player1.alive = False
                        else: # Removes shield if shielded
                            loseShieldSound.play()
                            player1.img = Ship
                        enBullets.pop(enBullets.index(bullet)) 
            
            # Checks collision with P2
            if (bullet.y - bullet.radius < player2.hitbox[1] + player2.hitbox[3] and
                    bullet.y + bullet.radius > player2.hitbox[1] and player2.alive):
                    if (bullet.x + bullet.radius > player2.hitbox[0] and
                        bullet.x - bullet.radius < player2.hitbox[0] + player2.hitbox[2]):
                        hitSound.play()
                        if player2.img == Ship2:
                            player2.respawn = dist+500
                            player2.alive = False 
                        else:
                            loseShieldSound.play()
                            player2.img = Ship2
                        enBullets.pop(enBullets.index(bullet))                     
     
        # Keeps track of inputted keys
        keys = pygame.key.get_pressed()
        
        # Only check inputs if the player is alive
        if player1.alive:
            if ((keys[pygame.K_LEFT] and player1.x > player1.vel) or
                keys[pygame.K_d] or moveRight or moveLeft) and player1.x < screenWidth - player1.width - player1.vel:
                hasMoved1 = True # Variable that states player has recently moved
                campSafe1 = True # Variable that checks whether player isn't camping
                NoMoveGoal1 = dist+300  # Adds 300 units where player can sit still
            
            else:
                if hasMoved1:   # If not moving, variables are updates
                    NoMoveGoal1 = dist+300 # If player continues to not move, they will be punished
                    hasMoved1 = False
            
            if dist > NoMoveGoal1 - 80 and campSafe1:  # 80 units before punishment, player is warned
                campSafe1 = False
                warningSound.play()
                
            if dist > NoMoveGoal1:     # If player has still not moved, they are punished
                camper.play()       # Noise is played to alert player
                NoMoveGoal1 += 1000  # Needed so noise doesn't continually play
                allowedBuls = 0     # Player is no longer permitted to shoot
                allowedEns += 75    # 75 enemies instantly spawn
                allowShots = True   # All 75 enemies can shoot
                enShots += 3        # All 75 enemies shoot more frequently
                diff = diff*1.15    # Difficulty is increased
        
        # NoMoveGoal continues to increase while dead, since you can't move
        if not player1.alive:
            NoMoveGoal1 = dist+300
        
        # Same thing, but for player 2
        if player2.alive:
            if (((keys[pygame.K_LEFT] or moveLeft) and player2.x > player2.vel) or
                 (keys[pygame.K_RIGHT] or moveRight) and player2.x < screenWidth - player2.width - player2.vel):
                hasMoved2 = True
                campSafe2 = True
                NoMoveGoal2 = dist+300    
            
            else:
                if hasMoved2:
                    NoMoveGoal2 = dist+300
                    hasMoved2 = False
            
            if dist > NoMoveGoal2 - 80 and campSafe2:
                campSafe2 = False
                warningSound.play()
                
            if dist > NoMoveGoal2:
                camper.play()
                NoMoveGoal2 += 1000
                allowedBuls = 0
                allowedEns += 75
                allowShots = True
                enShots += 3
                diff = diff*1.15    
                
        if not player2.alive:
            NoMoveGoal2 = dist+300
        
        # Q or Start on the controller both end the game
        if(keys[pygame.K_q]) or (event.type == pygame.JOYBUTTONDOWN and event.button == 9):
            gameoverSound.play()
            show_gameover()
        
        # Space and W both shoot for P1 (Shoot loop must be 0 to prevent multiple bullets firing from 1 input)
        if(keys[pygame.K_SPACE] or keys[pygame.K_w]) and shootLoopP1 == 0 and player1.alive:
            shootLoopP1 = 1
            if len(bulletsP1) < allowedBulsP1: # Checks number of bullets currently on screen with max
                bulletSound.play()
                bulletsP1.append(projectile(round(player1.x + player1.width //2), 
                                          player1.y, 3, (255,255,255), 1, 15))      

        # Enter key, or Up arrow all shoot for P2. CanShoot is used for USB Controller                                    
        if(keys[pygame.K_RETURN] or keys[pygame.K_UP] or canShoot) and shootLoopP2 == 0 and player2.alive:
            shootLoopP2 = 1
            if len(bulletsP2) < allowedBulsP2:
                bulletSound.play()
                bulletsP2.append(projectile(round(player2.x + player2.width //2), 
                                            player2.y, 3, (255,255,255), 1, 15))                                        
            
        # If the player is holding a boost button, and a direction, and their boost bar isn't empty, speed is doubled
        if player2.alive:
            if(((keys[pygame.K_RCTRL] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]))
                or (canBoost and (moveLeft or moveRight))):
                player2.boost = True
                if player2.canBoost:
                    player2.vel = diff*2
            else:
                if player2.vel != diff*2:
                    player2.vel = diff
                player2.vel = diff
                player2.boost = False
            if (keys[pygame.K_LEFT] or moveLeft) and player2.x > player2.vel:
                player2.x -= player2.vel
                player2.left = True
                player2.right = False
            elif (keys[pygame.K_RIGHT] or moveRight) and player2.x < screenWidth - player2.width - player2.vel:
                player2.x += player2.vel 
                player2.right = True
                player2.left = False
        
        if player1.alive and twoP == True:   
            if keys[pygame.K_LSHIFT] and (keys[pygame.K_a] or keys[pygame.K_d]) :
                player1.boost = True
                if player1.canBoost:
                    player1.vel = diff*2          
            else:
                if player1.vel != diff*2:
                    player1.vel = diff
                player1.vel = diff
                player1.boost = False
            if (keys[pygame.K_a]) and player1.x > player1.vel:
                player1.x -= player1.vel
                player1.left = True
                player1.right = False
            elif (keys[pygame.K_d]) and player1.x < screenWidth - player1.width - player1.vel:
                player1.x += player1.vel 
                player1.right = True
                player1.left = False   

        if player1.alive and twoP == False: # Game over if P1 dies
            if(keys[pygame.K_q]) or (event.type == pygame.JOYBUTTONDOWN and event.button == 9):
                gameoverSound.play()
                show_gameover()
    
            # Shooting keys modified if 1 player mode
            if(keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_w]
               or keys[pygame.K_UP] or canShoot) and shootLoopP1 == 0:
                shootLoopP1 = 1
                if len(bulletsP1) < allowedBulsP1:
                    bulletSound.play()
                    bulletsP1.append(projectile(round(player1.x + player1.width //2), 
                                              player1.y, 3, (255,255,255), 1, 15))                              
                
            # Boost controls if 1 player mode
            if(((keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and 
                (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d])) or 
                (canBoost and (moveLeft or moveRight))):
                player1.boost = True
                if player1.canBoost:
                    player1.vel = diff*2
            else:
                if player1.vel != diff*2:
                    player1.vel = diff
                player1.vel = diff
                player1.boost = False
            if ((keys[pygame.K_LEFT] or keys[pygame.K_a] or moveLeft) and player1.x > player1.vel):
                player1.x -= player1.vel
                player1.left = True
                player1.right = False
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d] or moveRight) and player1.x < screenWidth - player1.width - player1.vel:
                player1.x += player1.vel
                player1.right = True
                player1.left = False
                
        # Check collision of player bullets with enemy bullets        
        for bullet in bulletsP1:
            for eBullet in enBullets:
                if (bullet.y - bullet.radius*1.5 < eBullet.y + eBullet.radius*1.5 and
                    bullet.y + bullet.radius*1.5 > eBullet.y - eBullet.radius*1.5):
                    if (bullet.x + bullet.radius*1.5 > eBullet.x - eBullet.radius*1.5 and
                        bullet.x - bullet.radius*1.5 < eBullet.x + eBullet.radius*1.5):
                        try:
                            bulletsP1.pop(bulletsP1.index(bullet)) # Deletes both bullets on impact
                            enBullets.pop(enBullets.index(eBullet))
                        except:
                            pass
                      
        for bullet in bulletsP2:
            for eBullet in enBullets:
                if (bullet.y - bullet.radius*1.5 < eBullet.y + eBullet.radius*1.5 and
                    bullet.y + bullet.radius*1.5 > eBullet.y - eBullet.radius*1.5):
                    if (bullet.x + bullet.radius*1.5 > eBullet.x - eBullet.radius*1.5 and
                        bullet.x - bullet.radius*1.5 < eBullet.x + eBullet.radius*1.5):
                        try:
                            bulletsP2.pop(bulletsP2.index(bullet))
                            enBullets.pop(enBullets.index(eBullet))
                        except:
                            pass

        # Redraws all elements on screen     
        redrawGameWindow()
            
        win.fill((0,0,0))
        

    pygame.quit() # Quits once run is False
   
# Method for title screen   
def title():
    # High scores
    ###################################################################################################
    # Open highscores
    f = open('Highscore.txt')
    highscores = []

    # Mouse disabled
    pygame.mouse.set_visible(False)
    # Open to read file
    for line in f:
        highscores.append(ast.literal_eval(line))
    f.close()

    # Game crashes while attempting to get max if highscores is empty
    # To prevent this, add a highscore of 0
    if highscores == []:
        highscores.append(['System',0])

    # Gets number from each highscore element
    highestCheck = []

    # Checks for highscore to beat
    for x in highscores:
        highestCheck.append(x[1])
    toBeat = max(highestCheck)

    # For debugging
    print(highscores)
    
    # atMenu is similar to Run
    atMenu = True
    i = 0
    buttonPress = 1
    # Loads menu sounds
    menuSound = pygame.mixer.Sound('./Sounds/MenuMove.wav')
    menuSelect = pygame.mixer.Sound('./Sounds/MenuSelect.wav')
    while atMenu:
        clock.tick(30)
        # Similar to bullet cool down. Prevents unwanted input by adding delay
        if buttonPress > 0:
           buttonPress += 1
        
        if buttonPress > 5:
            buttonPress = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                atMenu = False
                
        # Loads images used in menu        
        titlescreenP1 = pygame.image.load('./Images/Titlescreen1P.jpg')
        titlescreenP2 = pygame.image.load('./Images/Titlescreen2P.jpg')
        titlescreenHS = pygame.image.load('./Images/TitlescreenHS.jpg')
        # Each of the 3 is the title screen with a box around a different option
        titlescreen = [titlescreenP1, titlescreenP2, titlescreenHS]
        keys = pygame.key.get_pressed()
        
        # Quits game if escape or Q is pressed
        if (keys[pygame.K_q] or keys[pygame.K_ESCAPE]):
           pygame.quit()
           atMenu = False
        
        # Enter and Space both select current choice
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and buttonPress == 0:
            menuSelect.play()
            if i == 0: # First option (one player mode)
                twoP = False
                nameGrab(twoP, highscores, toBeat)
            if i == 1: # Second option (two player mode)
                twoP = True
                nameGrab(twoP, highscores, toBeat)
            if i == 2: # Third option (high score list)
                menuSound.play()
                highscoreMenu(highscores)
                
        # Pressing up changes the menu selection choice       
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and buttonPress == 0:
            menuSound.play()
            buttonPress = 1
            if i == 0: # Since there is no -1 option, loop back to 2
                i = 2
            else:
                i -= 1
        # Pressing down changes the menu selection choice        
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and buttonPress == 0:
            menuSound.play()
            buttonPress = 1
            if i == 2: #Since there is no 3 option, loop back to 0
                i = 0
            else:
                i += 1
                
        # Draw and update the screen 
        # Whatever choice is selected (i), that image is loaded and drawn to the screen
        win.blit(titlescreen[i], (0,0))
        pygame.display.update()    
 
# Allows player to set name for current play 
def nameGrab(twoP, highscores, toBeat):
    typing = True # Similar to run, in the method play
    name = ''
    font = pygame.font.SysFont(None, 25)
    win.fill((0,0,0))
    # Text displayed to screen asking for name
    question = font.render('Enter your name:', True, (255,255,255))
    win.blit(question, (200,200))
    pygame.display.update()
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]: # Escape quits the program
                    typine = False
                    pygame.quit()
                elif keys[pygame.K_RETURN]: # Pressing enter confirms your name and begins the game
                    play(twoP, highscores, toBeat, name)
                elif keys[pygame.K_BACKSPACE]: # Pressing backspace messes up the text, so instead
                                               # It just recalls the function, erasing your entire name
                    nameGrab(twoP, highscores, toBeat)
                else:
                    name += event.unicode # Grabs whatever text you type and prints it to the screen
                    screen_text = font.render(name, True, (255,255,255))
                question = font.render('Enter your name:', True, (255,255,255))
                win.blit(question, (200,200))
                win.blit(screen_text, (200,300))
                pygame.display.update() # Updates the display

def highscoreMenu(highscores):
    # Arrays to hold top 5 names and scores
    scoreList = []
    nameList  = []
    font = pygame.font.SysFont(None,25)
    # Loops through high scores and finds top 5 values
    for x in highscores:
        nameList.append(x[0])
        scoreList.append(x[1])
    first = '1: ' + nameList[scoreList.index(max(scoreList))] + ': ' + str(max(scoreList))
    del nameList[scoreList.index(max(scoreList))]
    scoreList.pop(scoreList.index(max(scoreList)))
    second = '2: ' + nameList[scoreList.index(max(scoreList))] + ': ' + str(max(scoreList))
    del nameList[scoreList.index(max(scoreList))]
    scoreList.pop(scoreList.index(max(scoreList)))
    third = '3: ' + nameList[scoreList.index(max(scoreList))] + ': ' + str(max(scoreList))
    del nameList[scoreList.index(max(scoreList))]
    scoreList.pop(scoreList.index(max(scoreList)))
    fourth = '4: ' + nameList[scoreList.index(max(scoreList))] + ': ' + str(max(scoreList))
    del nameList[scoreList.index(max(scoreList))]
    scoreList.pop(scoreList.index(max(scoreList)))
    fifth = '5: ' + nameList[scoreList.index(max(scoreList))] + ': ' + str(max(scoreList))
    del nameList[scoreList.index(max(scoreList))]
    scoreList.pop(scoreList.index(max(scoreList)))
    
    # Prints all scores on screen
    win.fill((0,0,0))
    highscore_text = font.render("Highscores:", True, (255,255,255))
    first_display = font.render(first, True, (255,255,255))
    second_display = font.render(second, True, (255,255,255))
    third_display = font.render(third, True, (255,255,255))
    fourth_display = font.render(fourth, True, (255,255,255))
    fifth_display = font.render(fifth, True, (255,255,255))
    win.blit(highscore_text, (200,50))
    win.blit(first_display, (200,150))
    win.blit(second_display, (200,200))
    win.blit(third_display, (200,250))
    win.blit(fourth_display, (200,300))
    win.blit(fifth_display, (200,350))
    pygame.display.update()
    
    # Pressing any key returns you to the main menu
    atMenu = True
    while atMenu:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    title()
        
                    
title()                       
