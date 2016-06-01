#-------------------------------------------------------------------------------
# Name:        Snake Classic Multiplayer
# Purpose:     Main script to handle everything regaurding the snake
#
# Author:      patkinso9822
#
# Created:     09/05/2016
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-----------------------------IMPORT--------------------------------------------
#-------------------------------------------------------------------------------
import pygame
import random
import numpy #Used to save player score
import operator #Used to sort array of dictinarys by key
#-------------------------------------------------------------------------------
#-----------------------------CLASSES//FUNCTIONS--------------------------------
#-------------------------------------------------------------------------------

def IsInMap(pos):
    '''
    IsInMap(pos -> [x,y]) -> bool(True) or bool(False)
    Returns true if the defined location is within the grid
    '''
    try:
        SnakeMap["X" + str(pos[0]) + "Y" + str(pos[1])]
    except:
        return False
    return True

def GetState(pos):
    '''
    GetState(pos -> [x,y]) -> str(State)
    Returns the current state of the position on the grid
    States = ["Air","Point","Snake"."Wall"]
    '''
    if IsInMap(pos):
        return SnakeMap["X" + str(pos[0]) + "Y" + str(pos[1])]
    else:
        return State4

def SetState(pos,State):
    '''
    SetState(pos -> [x,y],State -> State(1-4)) -> str(Wall) or None
    Returns "Wall" if the position is out of the grid
    '''
    if IsInMap(pos):
        SnakeMap["X" + str(pos[0]) + "Y" + str(pos[1])] = State
    else:
        return State4

def ResetSnakeMap(x,y):
    '''
    ResetSnakeMap(x,y) -> None
    Used to reset the grid back to State "Air"
    '''
    for y in range(0,SnakeMapSizeY):
        for x in range(0,SnakeMapSizeY):
            SnakeMap["X" + str(x) + "Y" + str(y)] = State1

def RemovePoint(snake):
    '''
    RemovePoint(snakeObject) -> None
    Searches for a Point object inside the snake defined and removes it
    '''
    spritelist = snake.Container.sprites()

    largest = None
    for i in range(len(spritelist)):
        if spritelist[i].UID == 1000000:
            largest = spritelist[i]
    if not largest: return
    SetState(largest.Position,State1)
    snake.Container.remove(largest)
    snake.Container.update()

def AddPoint(snake):
    '''
    AddPoint(snakeObject) -> None
    Adds a Point object inside the snake defined
    '''
    RemovePoint(snake)
    pos = [random.randint(2,47),random.randint(2,47)]
    while GetState(pos) == State3 or GetState(pos) == State2:
        pos = [random.randint(2,47),random.randint(2,47)]
    SetState(pos,State2)
    point = Block(Point,pos)

    snake.Container.add(point)
    snake.Container.update()

class Sprite(pygame.sprite.Sprite):
    '''
    Creates a Sprite object with a image,position and a tag
    '''
    def __init__(self,img,pos,tag =None):
        pygame.sprite.Sprite.__init__(self)
        self.Tag = tag
        self.image = img
        self.image.set_colorkey((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]



class Snake(pygame.sprite.Sprite):
    '''
    Creates a snake object which moves each time Move() is called
    '''
    def __init__(self,Screen,pos,direction = [1,0]):
        pygame.sprite.Sprite.__init__(self)
        self.Screen = Screen
        self.Size = 10
        self.Previous = None
        self.Current = None
        self.PreviousPosition = pos
        self.Position = pos
        self.Direction = direction
        self.PreviousDirection = self.Direction
        self.Container = pygame.sprite.RenderPlain()
        self.UID = 0

    def GetNextPosition(self):
        '''
        GetNextPosition() -> array(x,y)
        Returns the position it will be in next frame
        '''
        return [self.Position[0]+self.Direction[0],self.Position[1]+self.Direction[1]]

    def SetSecondPiece(self,prevDirection,newDirection):
        '''
        SetSecondPiece(prevDirection,newDirection) -> None
        Sets the piece behind the head to the correct image to resemble a snake
        '''
        Down = [0,1]
        Up = [0,-1]
        Left = [-1,0]
        Right = [1,0]
        Chosen = None
        if not self.Previous:
            pass
        else:
            if not prevDirection == newDirection:
                if (prevDirection == Down and newDirection == Right) or (prevDirection == Left and newDirection == Up):
                    Chosen = Turn1
                elif (prevDirection == Left and newDirection == Down) or (prevDirection == Up and newDirection == Right):
                    Chosen = Turn2
                elif (prevDirection == Right and newDirection == Down) or (prevDirection == Up and newDirection == Left):
                    Chosen = Turn3
                else:
                    Chosen = Turn4
            else:
                if newDirection == Up or newDirection == Down:
                    Chosen = StraightUp
                else:
                    Chosen = StraightRight
            objData = {"UID":self.Previous.UID,"Pos":self.Previous.Position}
            self.Container.remove(self.Previous)
            a = Block(Chosen,objData["Pos"],objData["UID"])
            self.Container.add(a)
            self.Container.update()


    def GetFace(self,Direction):
        '''
        GetFace(Direction) -> obj(Image)
        Finds the image based on the direction given
        '''
        if Direction == [-1,0]:
            return FaceLeft
        elif Direction == [1,0]:
            return FaceRight
        elif Direction == [0,-1]:
            return FaceUp
        elif Direction == [0,1]:
            return FaceDown


    def Move(self):
        '''
        Move() -> None
        Updates the snake position with the current direction and draws a new snake piece
        '''
        self.UID = self.UID + 1

        a = Block(self.GetFace(self.Direction),self.GetNextPosition(),self.UID)
        self.Previous = self.Current
        self.Current = a
        self.SetSecondPiece(self.PreviousDirection,self.Direction)
        self.PreviousPosition = self.Position
        self.Position = [self.Position[0]+self.Direction[0],self.Position[1]+self.Direction[1]]
        self.PreviousDirection = self.Direction
        self.Container.add(a)
        if (len(self.Container) >= self.Size ):
            spritelist = self.Container.sprites()
            largest = spritelist[0]
            for i in range(len(spritelist)):
                if spritelist[i].UID < largest.UID:
                    largest = spritelist[i]
            SetState(largest.Position,State1)
            self.Container.remove(largest)
        self.Container.update()



class Block(pygame.sprite.Sprite):
    '''
    Creates a object for the snake piece
    '''
    def __init__(self,img,pos,UID = 1000000):
        self.Position = pos
        self.UID = UID
        if img == Point:
            SetState(pos,State2)
        else:
            SetState(pos,State3)
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*10
        self.rect.y = pos[1]*10

def DrawDisplay():
    '''
    DrawDisplay() -> None
    Draws the scoreboard
    '''
    GameFont = pygame.font.SysFont("Comic Sans MS", 20,True)
    background = pygame.draw.rect(Screen,(0,0,0),[0,500,500,20])
    scoreText = GameFont.render("Score: " + str(Score),2,(255,255,255))
    Screen.blit(scoreText,[0,495])
    PauseButtonContainer.update()
    PauseButtonContainer.draw(Screen)

def DrawMenu():
    '''
    DrawMenu() -> str(selected)
    Returns the selected button with the tag name
    '''
    Menu = pygame.sprite.RenderPlain()
    dropLogo = Sprite(Logo,[40,0])
    playButton = Sprite(Play,[25,520],"Play")
    quitButton = Sprite(Quit,[25,520],"Quit")
    multiButton = Sprite(Multiplayer,[275,520],"MultiPlayer")
    highscoreButton = Sprite(Highscore,[275,520],"HighScore")
    Menu.add(dropLogo)
    Menu.add(playButton)
    Menu.add(quitButton)
    Menu.add(multiButton)
    Menu.add(highscoreButton)
    Menu.update()
    Selected = None
    for i in range(1,255):
        Screen.fill(( 255-i, 255-i, 255))
        clock.delay(4)
        pygame.display.flip()
    for i in range(1,185):
        dropLogo.rect.y = i-165
        Screen.fill(( 0, 0, 255))
        Menu.draw(Screen)
        pygame.display.flip()
        clock.delay(5)

    for i in range(1,120):
        playButton.rect.y = 540-i
        quitButton.rect.y = 480-i
        highscoreButton.rect.y = 480-i
        multiButton.rect.y = 540-i
        Screen.fill(( 0, 0, 255))
        Menu.draw(Screen)
        pygame.display.flip()
        clock.delay(3)

    while not Selected:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in Menu.sprites():
                        if box.rect.collidepoint(pygame.mouse.get_pos()):
                            if box.Tag != None:
                                Selected = box
    return Selected.Tag


def DrawHighscores():
    '''
    DrawHighscores() -> None
    Draws the Highscores with the numpy save file
    '''
    Screen.fill(( 0, 0, 255))
    ExitHighscores = False
    arr = numpy.load("SaveFile.npy").tolist()
    arr.sort(key=operator.itemgetter('Score'))
    arr.reverse()

    HSExit = pygame.sprite.RenderPlain()
    HSHolder = pygame.sprite.RenderPlain()

    HSHolder.add(Sprite(HSBack,[0,0]))
    HSExit.add(Sprite(Exit,[50,470],"Exit"))
    HSHolder.draw(Screen)
    HSExit.draw(Screen)
    GameFont = pygame.font.SysFont("Courier", 39,True)
    for i in range(0,10):
        try:
            stat = arr[i]
            highscoreText = GameFont.render('{0:12}{1:>4}'.format(stat["Name"],stat["Score"]),2,(255,255,255))
            Screen.blit(highscoreText,[60,54 + (i*39)])
        except: pass

    pygame.display.flip()
    while not ExitHighscores:
        for event in pygame.event.get():
            if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1 and HSExit.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()):
                ExitHighscores = True

#-------------------------------------------------------------------------------
#-----------------------------VARIABLE DEFINING---------------------------------
#-------------------------------------------------------------------------------
SnakeMap = {}
SnakeMapSizeX = 50
SnakeMapSizeY = 50

State1 = "Air"
State2 = "Point"
State3 = "Snake"
State4 = "Wall"


#SnakeMap["X" + Snake.x + "Y" + Snake.y] return State
#        State 1 = "Air" Null(Safe)
#        State 2 = "Point" Increment Snake.Size by 5
#        State 3 = "Snake" Snake Square(Unsafe)
#        State 4 = "Wall" Off of the map results in death

clock=pygame.time
Finished = False
ScreenSize = [500,520]
pygame.init()
Screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption("Snake Game")
PauseButtonContainer = pygame.sprite.RenderPlain()
rawusername = None

#-------------------------------------------------------------------------------
#-----------------------------PRELOAD ASSETS--------------------------------
#-------------------------------------------------------------------------------
Pause           = pygame.image.load("Assets\Interface\Pause.png").convert()
Unpause         = pygame.image.load("Assets\Interface\Unpause.png").convert()
HSBack          = pygame.image.load("Assets\Interface\HSBackground.png").convert()
Logo            = pygame.image.load("Assets\Interface\DropDownLogo.png").convert()


Play            = pygame.image.load("Assets\Buttons\Play.png").convert()
Quit            = pygame.image.load("Assets\Buttons\Quit.png").convert()
Multiplayer     = pygame.image.load("Assets\Buttons\\2-Player.png").convert()
Highscore       = pygame.image.load("Assets\Buttons\Highscores.png").convert()
Exit            = pygame.image.load("Assets\Buttons\ExitButton.png").convert()

Point           = pygame.image.load("Assets\Snake\Point.png").convert()

StraightRight   = pygame.image.load("Assets\Snake\StraightRight.png").convert()
StraightUp      = pygame.image.load("Assets\Snake\StraightUp.png").convert()

Turn1           = pygame.image.load("Assets\Snake\Turn1.png").convert()
Turn2           = pygame.image.load("Assets\Snake\Turn2.png").convert()
Turn3           = pygame.image.load("Assets\Snake\Turn3.png").convert()
Turn4           = pygame.image.load("Assets\Snake\Turn4.png").convert()

FaceRight       = pygame.image.load("Assets\Snake\Right.png").convert()
FaceLeft        = pygame.image.load("Assets\Snake\Left.png").convert()
FaceUp          = pygame.image.load("Assets\Snake\Up.png").convert()
FaceDown        = pygame.image.load("Assets\Snake\Down.png").convert()
#-------------------------------------------------------------------------------
#-----------------------------MAIN LOOP-----------------------------------------
#-------------------------------------------------------------------------------

while not Finished:
    Picked = DrawMenu()# Draws the menu and returns the selected image name

#-------------------------------------------------------------------------------
#-----------------------------SOLO MODE-----------------------------------------
#-------------------------------------------------------------------------------

    if Picked == "Play":
        for i in range(1,255):
            Screen.fill(( i, i, 255))
            pygame.display.flip()
            clock.delay(4)
        pygame.display.flip()
        Done = False
        Speed = 15
        ResetSnakeMap(SnakeMapSizeX,SnakeMapSizeY)
        snake = Snake(Screen,[10,25])
        AddPoint(snake)
        Score = 0
        Ready = True
        PauseButtonContainer.empty()
        PauseButtonContainer.add(Sprite(Pause,[480,500],"Pause"))
        while not Done:

            Screen.fill(( 255, 255, 255))
            nextPosition = snake.GetNextPosition()
            if GetState(nextPosition) == State1:
                pass
            elif GetState(nextPosition) == State2:
                snake.Size = snake.Size + 5
                Score = Score + 5
                AddPoint(snake)
            elif GetState(nextPosition) == State3 or GetState(nextPosition) == State4:
                Done = True
                snake.Container.empty()
                CurrentSave = numpy.load("SaveFile.npy")
                try:
                    rawusername = rawusername or raw_input("Enter your name:") #Will only ask for your name once
                    while rawusername == "" or len(rawusername)>10: # prevents blank names or too long names that can't fit
                        rawusername = raw_input(rawusername == "" and "Name too short" or "Name too long")#Chooses between too short or too long
                except:
                    Username = "Anonymous"
                numpy.save("SaveFile",numpy.append(CurrentSave,{"Name": rawusername,"Score":Score})) #it loads your current save file
                                                                                                  #and appends it to the list and saves it
            snake.Move()
            snake.Container.draw(Screen)#Draws the snake to the screen
            DrawDisplay()#Draws the score board
            pygame.display.flip()#Finally draws everything to the screen
            Break = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and not Break:#break variable only lets one of the keys be pressed each frame
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.Direction != [1,0]:
                        snake.Direction = [-1,0]
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.Direction != [-1,0]:
                        snake.Direction = [1,0]
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.Direction != [0,1]:
                        snake.Direction = [0,-1]
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.Direction != [0,-1]:
                        snake.Direction = [0,1]
                    Break = True
                if  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    Speed = 25
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    Speed = 15
                if event.type == pygame.QUIT: Done = True; Finished = True; break
                if event.type == pygame.MOUSEBUTTONDOWN:#checks if pause button was clicked
                    if event.button == 1:
                        if PauseButtonContainer.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()):
                            if PauseButtonContainer.sprites()[0].Tag == "Pause":
                                PauseButtonContainer.empty()
                                PauseButtonContainer.add(Sprite(Unpause,[480,500],"Unpause"))
                                PauseButtonContainer.draw(Screen)
                                pygame.display.flip()
                                Ready = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e: #Pause game event keybinding
                    if PauseButtonContainer.sprites()[0].Tag == "Pause":
                        PauseButtonContainer.empty()
                        PauseButtonContainer.add(Sprite(Unpause,[480,500],"Unpause"))
                        PauseButtonContainer.draw(Screen)
                        pygame.display.flip()
                        Ready = False
            while not Ready:# yields until pause is repressed
                for event in pygame.event.get():
                    if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1 and PauseButtonContainer.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()) or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        Ready = True
                        PauseButtonContainer.empty()
                        PauseButtonContainer.add(Sprite(Pause,[480,500],"Pause"))
            clock.delay(1000/Speed)# Speed is changed when space is held down

#-------------------------------------------------------------------------------
#-----------------------------MULTIPLAYER---------------------------------------
#-------------------------------------------------------------------------------

    elif Picked == "MultiPlayer":
        for i in range(1,255):
            Screen.fill(( i, i, 255))
            pygame.display.flip()
            clock.delay(4)
        ResetSnakeMap(SnakeMapSizeX,SnakeMapSizeY)
        snake1 = Snake(Screen,[10,26],[1,0])
        snake2 = Snake(Screen,[40,26],[-1,0])
        AddPoint(snake1)
        AddPoint(snake2)
        Done = False
        while not Done:
            Screen.fill(( 255, 255, 255))
            nextPosition = snake1.GetNextPosition()
            if GetState(nextPosition) == State1:
                SetState(nextPosition,State3)
            elif GetState(nextPosition) == State2:
                snake1.Size = snake1.Size + 10
                AddPoint(snake1)
                AddPoint(snake2)
            elif GetState(nextPosition) == State3:
                Done = True
                print "Player 1 died"
                snake1.Container.empty()
            elif GetState(nextPosition) == State4:
                Done = True
                print "Player 1 died"
                snake1.Container.empty()

            nextPosition = snake2.GetNextPosition()
            if GetState(nextPosition) == State1:
                SetState(nextPosition,State3)
            elif GetState(nextPosition) == State2:
                snake2.Size = snake2.Size + 10
                AddPoint(snake2)
                AddPoint(snake1)
            elif GetState(nextPosition) == State3:
                Done = True
                print "Player 2 died"
                snake2.Container.empty()
            elif GetState(nextPosition) == State4:
                Done = True
                print "Player 2 died"
                snake2.Container.empty()

            snake1.Move()
            snake2.Move()
            snake1.Container.draw(Screen)
            snake2.Container.draw(Screen)
            Break1 = False
            Break2 = False

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and not Break2 and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    if (event.key == pygame.K_LEFT) and snake2.Direction != [1,0]:
                        snake2.Direction = [-1,0]
                    elif (event.key == pygame.K_RIGHT) and snake2.Direction != [-1,0]:
                        snake2.Direction = [1,0]
                    elif (event.key == pygame.K_UP) and snake2.Direction != [0,1]:
                        snake2.Direction = [0,-1]
                    elif (event.key == pygame.K_DOWN) and snake2.Direction != [0,-1]:
                        snake2.Direction = [0,1]
                    Break2 = True
                if event.type == pygame.KEYDOWN and not Break1 and (event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s):
                    if (event.key == pygame.K_a) and snake1.Direction != [1,0]:
                        snake1.Direction = [-1,0]
                    elif (event.key == pygame.K_d) and snake1.Direction != [-1,0]:
                        snake1.Direction = [1,0]
                    elif (event.key == pygame.K_w) and snake1.Direction != [0,1]:
                        snake1.Direction = [0,-1]
                    elif (event.key == pygame.K_s) and snake1.Direction != [0,-1]:
                        snake1.Direction = [0,1]
                    Break1 = True


            clock.delay(1000/15)

#-------------------------------------------------------------------------------
#-----------------------------HIGHSCORES----------------------------------------
#-------------------------------------------------------------------------------
    elif Picked == "HighScore": DrawHighscores()
#-------------------------------------------------------------------------------
#-----------------------------EXIT----------------------------------------------
#-------------------------------------------------------------------------------
    elif Picked == "Quit": Finished = True #Breaks out of the main loop

pygame.quit()





