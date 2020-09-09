"""
Subcontroller module for Alien Invaders

Mohammed Hussien mah445 Abenazer Mekete agm246
12/6/2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.


    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    Additional Attributes:
        _addX : The number of Steps the wave of aliens have to take in the x direction [int >= 0]
        _addY : The number of Steps the wave of aliens have to take in the y direction [int >= 0]
        _aSpeed : The speed of the aliens [int > 0]
        _isPlayerBolt : Variable that informs if the bolt is shot from the ship or not, used to make sure
                        only one bolt is on  the window [bool]
        _lives : the number of lives the player currentlly has [int>0]
        _paused : Checks if the game is paused [bool]
        _complete : Checks if the game is complete [bool]
        _Abolts : Alien botlts that are shot[list]
        _determinefactor : Determines if the wave of aliens reached the edge and should move down and left/right [bool]
        _bolts : bolts shot from the ship on the window [list]
        _pewSound: the sound for the ship shot [Sound]
        _addX : alien steps in the x-direction [int>0]
        _addY : alien steps in the y-direction [int>0]
        _aSpeed : the alien speed [int>0]
        _displayLife : the number of lives the player has left
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the current in-game life count
        """
        return self._lives

    def getPaused(self):
        """
        Returns: the _paused status of the game
        """
        return self._paused

    def getComplete(self):
        """
        Returns: the _complete status of hte game
        """
        return self._complete

    def setLives (self, live):
        """
        Sets the life the user has at the moment

        Parameter live: life count
        Precondition: life is an int > 0
        """
        self._lives = live

    def setPaused(self, pause):
        """
        Sets the pause status of the game

        Parameter pause : paused status
        Precondition: pause is a bool
        """
        self._paused = pause
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializer that creates the wave controller and assigns values to the initial
        attributes
        """
        # self._ship = Ship()
        self._lives = 3
        self._complete = 0
        self._paused = False
        self.makewavesofaliens()
        self._pewSound = Sound('pew1.wav')
        self._ship = Ship()
        self.makedline()
        self._bolts = []
        self._time = 0
        self._addX = ALIEN_H_WALK
        self._addY = ALIEN_V_WALK
        self._determinefactor = False
        self._aSpeed = ALIEN_SPEED
        self._isPlayerBolt = False
        self._Abolts = []
        self._displayLife = GLabel(text = 'Lives: ' +  str(self._lives), x = GAME_WIDTH - 400, y = GAME_HEIGHT - 25, halign = 'left', valign = 'middle',
                            font_size = 50, font_name = 'Arcade.ttf')
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update2(self, input, dt):
        """
        update2 checks if the game is not over (when the aliens cross the border or the ship is out of lives)
        if not:
            it excecutes the game by creating the ship, aliens, bolts and removing them when they are killed.
        Parameter input : keyboard input
        Precondition: a GInput
        """

        if self._aliens is None:
            self._complete = 1
        if self.borderPatrol() == True or self.killed() == True:
            self._complete = 2
        else:
            self._ship.moveship(input)
            self.create_Bolt(input)
            self.xcoordinates = []
            for alienX in range(ALIENS_IN_ROW):
                for alienY in range(ALIEN_ROWS):
                    if self._aliens[alienX][alienY] != None:
                        self.xcoordinates.append(self._aliens[alienX][alienY].getX())
            self._time += dt
            if self._time > ALIEN_SPEED and self.xcoordinates != None:
                self.moveAliens()
                self.chooseAlien()
            self.removeAlien()
            self.removeShip()
            self.displayLives()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw2(self,view):
        """
        Draws the ship, the defense line, the aliens and the bolts
        """
        self._ship.draw(view)
        self._dline.draw(view)
        if self._lives != 0 and self._lives != None:
            self.displayLives().draw(view)
        if self._aliens != None:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.draw(view)
        for bolt in self._bolts:
            if self._bolts != None:
                self.movetheBolt(bolt,view)
            # bolts.draw(view)
        for Abolts in self._Abolts:
            if self._Abolts != None:
                self.moveAlienBolt(Abolts,view)


    # HELPER METHODS FOR COLLISION DETECTION
    def makewavesofaliens(self):
        """
        Makes a 2d list of Aliens
        """
        self._aliens = []
        xpos = 0
        for alienX in range(ALIENS_IN_ROW):
            xpos = xpos + ALIEN_H_SEP + ALIEN_WIDTH
            newlist = []
            ypos = GAME_HEIGHT - ALIEN_CEILING - (ALIEN_HEIGHT/2)
            for alienY in range(ALIEN_ROWS) :
                m =  alienY%(ALIENS_IN_ROW/2)
                if alienY == 0:
                    ypos = GAME_HEIGHT-ALIEN_CEILING- (ALIEN_HEIGHT/2)
                else:
                    ypos = ypos - (ALIEN_V_SEP +ALIEN_HEIGHT)
                if m == 0 or m == 5:
                    image = 'alien1.png'
                if m == 2 or m == 1:
                    image = 'alien2.png'
                if m == 4 or m == 3:
                    image = 'alien3.png'
                newlist.append(Alien(x = xpos ,y = ypos ,width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = image))
            self._aliens.append(newlist)

        """
        makes the defense line
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,800,DEFENSE_LINE],linewidth=2,linecolor = 'black')


    def moveAliens(self):
        """
        Moves aliens throughout the window.
        """
        if self.xcoordinates != None or self.xcoordinates != []:
            if self._determinefactor == True:
                self.edgeX()
                self._addY = 0
                self._determinefactor = False
            # Y movement at edge:
            elif max(self.xcoordinates) > GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2:
                self.moveY()
            elif min(self.xcoordinates) < ALIEN_H_SEP + ALIEN_WIDTH - ALIEN_WIDTH/2:
                self.moveY()
            #     else:
            else:
                self._addX = self._addX
                self._addY = 0

            for alienX in range(ALIENS_IN_ROW):
                for alienY in range(ALIEN_ROWS):
                    if self._aliens[alienX][alienY] != None:
                        self._aliens[alienX][alienY].x += self._addX
                        self._aliens[alienX][alienY].y += self._addY
            self._time = 0.5


    def edgeX(self):
        """
        adjusts the constansts for the x direction when it reaches both edges
        """
        if self.xcoordinates != None:
            if max(self.xcoordinates) > GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2 :
                self._addX = -ALIEN_H_WALK
            elif min(self.xcoordinates) < ALIEN_H_SEP + ALIEN_WIDTH:
                self._addX = ALIEN_H_WALK
    def moveY(self):
        """
        Moves the aliens in the y direction when it reaches both edges
        """
        self._addX = 0
        self._addY = -ALIEN_V_WALK
        self._determinefactor = True
    def create_Bolt(self, input):
        """
        Creates the Bolt that will be fired from the ship when keyboard input 'spacebar' is pressedself.

        Parameter input : keyboard input
        Precondition: a Ginput
        """
        if input.is_key_down('spacebar'):
            bolt = (Bolt(self._ship.getX(), self._ship.getY() + SHIP_HEIGHT / 2, True ))
            if self.isPlayerBolt(bolt) == False:
                self._pewSound.play()
                self._bolts.append(bolt)
                self._isPlayerBolt = True
    def movetheBolt (self,bolt,view):
        """
        Moves the Bolt that is fired from the ship

        Parameter bolt : the bolt that is shoot
        Precondition: it is a class boltType

        Parameter View : the window
        Precondition : it's a GView
        """
        if bolt.getY() + BOLT_HEIGHT / 2 > GAME_HEIGHT:
            self.deleteBolt(bolt)
            self._isPlayerBolt = False
        else:
            bolt.moveBolt()
            bolt.draw(view)
            self._isPlayerBolt = True

    def moveAlienBolt (self,Abolt,view):
        """
        shoots from alien and deletes bolts when they pass the screen
        """
        if Abolt.getY() + BOLT_HEIGHT/2 < 0:
            del self._Abolts[self._Abolts.index(Abolt)]
        else:
            Abolt.moveABolt()
            Abolt.draw(view)

    def range_aliensAlive(self):
        """
        Finds the columns that have at least one alien
        """
        RangeAlive = []
        list = []
        for x in range(ALIENS_IN_ROW):
            for y in range(ALIEN_ROWS):
                if self._aliens[x][y] != None:
                    list.append(x)
        for x in list:
            if x not in RangeAlive:
                RangeAlive.append(x)
        return RangeAlive

    def chooseAlien(self):
        """
        chooses the alien from a randomcolumn that will shoot the bolt
        """
        randomcolumn = random.choice(self.range_aliensAlive())
        ycords = []
        xcord = 0
        for y in range(ALIEN_ROWS):
            if self._aliens[randomcolumn][y] != None:
                ycord = self._aliens[randomcolumn][y].getY()
                ycords.append(ycord)
                xcord = self._aliens[randomcolumn][y].getX()
        lowesty = min(ycords)

        Abolt = Bolt(xcord, lowesty, False)
        self._Abolts.append(Abolt)

    def deleteBolt (self,bolt):
        """
        Deletes the bolts that go off the screen

        Parameter bolt : the bolt that is shoot
        Precondition: it is a class boltType
        """

        del self._bolts[self._bolts.index(bolt)]
    def isPlayerBolt(self,bolt):
        """
        Checks if the bolt shot is one that is shot from the ship

        Parameter bolt : the bolt that is shoot
        Precondition: it is a class boltType
        """
        if self._isPlayerBolt == False:
           return False
        elif self._isPlayerBolt == True:
            return True
    def removeAlien(self):
        """
        removes alien that is shot by Bolt
        """
        if self._aliens != None:
            for x in range(len(self._aliens)):
                for y in range(len(self._aliens[x])):
                    alien = self._aliens[x][y]
                    for bolt in range(len(self._bolts)):
                        if alien != None:
                            if alien.collidesAlien(self._bolts[bolt]) == True:
                                self._aliens[x][y] = None
                                del self._bolts[bolt]
                                self._isPlayerBolt = False


    def removeShip(self):
        """
        removes the ship when it is shot
        """
        # bolts = self._Abolts
        for bolt in range(len(self._Abolts)):
            ship = self._ship
            if ship.collidesShip(self._Abolts[bolt]) == True:
                del bolt
                self._paused = True
    def borderPatrol(self):
        """
        ends the game when the aliens cross the barrier
        """
        if self._aliens != None:
            y_coordinates = []
            for x in range(len(self._aliens)):
                for y in range(len(self._aliens[x])):
                    if self._aliens[x][y] != None:
                        y_coordinates.append(self._aliens[x][y].getY())
            if y_coordinates != []:
                if min(y_coordinates) < DEFENSE_LINE:
                        return True
    def killed(self):
        """
        checks if the ship is killed
        """
        if self._lives == 0:
            return True
    def getAliens(self):
        """
        returns the list of _aliens
        """
        return self._aliens
    def displayLives(self):
        """
        Keeps track of and displays the number of lives the player has left.
        """
        if self._lives == 3:
            self._displayLife = GLabel(text = 'Lives: 3', x = GAME_WIDTH - 400, y = GAME_HEIGHT - 25, halign = 'left', valign = 'middle',
                                font_size = 50, font_name = 'Arcade.ttf')
            return self._displayLife
        if self._lives == 2:
            self._displayLife = GLabel(text = 'Lives: 2', x = GAME_WIDTH - 400, y = GAME_HEIGHT - 25, halign = 'left', valign = 'middle',
                                font_size = 50, font_name = 'Arcade.ttf')
            return self._displayLife
        if self._lives == 1:
            self._displayLife = GLabel(text = 'Lives: 1', x = GAME_WIDTH - 400, y = GAME_HEIGHT - 25, halign = 'left', valign = 'middle',
                                font_size = 50, font_name = 'Arcade.ttf')
            return self._displayLife
    def makedline(self):
        """
        makes the defense line
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,800,DEFENSE_LINE],linewidth=2,linecolor = 'black')
