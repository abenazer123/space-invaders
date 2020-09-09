"""
Abenazer Mekete agm246
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        return the x-coordinate of Ship
        """
        return self.x

    def getY(self):
        """
        returns the y-coordinate of Ship
        """
        return self.y
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializes Ship
        """
        super().__init__(x=400, y=SHIP_BOTTOM,width=SHIP_WIDTH,height=SHIP_HEIGHT,source='ship.png')
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    # def moveleft(self):
    #     Ship(x = 400 - SHIP_MOVEMENT, y=SHIP_BOTTOM,width=SHIP_WIDTH,height=SHIP_HEIGHT,source='ship.png')
    # def moveright(self):
    #     Ship(x = 400 + SHIP_MOVEMENT, y=SHIP_BOTTOM,width=SHIP_WIDTH,height=SHIP_HEIGHT,source='ship.png')
    # def moveship(self,x,y,width,height,source):
    #     Ship (x = x ,y=SHIP_BOTTOM,width=SHIP_WIDTH,height=SHIP_HEIGHT,source='ship.png')
    def moveship(self, input):
        """
        moves the ship depending on the arrow that is pressed.
        moves right when 'right' arrow is pressed
        moves left when 'left' arrow is pressed

        Parameter input : the keyboard input
        Precondition: a Ginput
        """
        if input.is_key_down('right') and self.x < GAME_WIDTH - SHIP_WIDTH/2:
            self.x += SHIP_MOVEMENT
        if input.is_key_down('left') and self.x - SHIP_WIDTH/2 > 0:
            self.x -= SHIP_MOVEMENT
        # self._ship = Ship(x = x, y=SHIP_BOTTOM,width=SHIP_WIDTH,height=SHIP_HEIGHT,source='ship.png')
        #print(self._ship)
        # self._ship.draw(view)
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def collidesShip(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        Top_Right = ((bolt.x + (BOLT_WIDTH/2)),(bolt.y + (BOLT_HEIGHT/2)))
        Top_Left = ((bolt.x - (BOLT_WIDTH/2)),(bolt.y + (BOLT_HEIGHT/2)))
        Bottom_Right = ((bolt.x + (BOLT_WIDTH/2)),(bolt.y - (BOLT_HEIGHT/2)))
        Bottom_Left = ((bolt.x - (BOLT_WIDTH/2)),(bolt.y - (BOLT_HEIGHT/2)))
        if self.contains(Top_Right) or self.contains(Top_Left) or self.contains(Bottom_Right) or self.contains(Bottom_Left):
            return True
        else:
            return False
# self.getis_playerBolt() == False and
class Alien(GImage):
    """
    A class to represent a single alien.
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x-coordinate of Alien
        """
        return self.x
    def getY(self):
        """
        Returns the y-coordinate of Alien
        """
        return self.y
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,width,height,source):
        """
        Initializes Alien
        """
        super().__init__(x=x,y=y,width=width,height= height,source=source)
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def collidesAlien(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        Top_Right = ((bolt.x + (BOLT_WIDTH/2)),(bolt.y + (BOLT_HEIGHT/2)))
        Top_Left = ((bolt.x - (BOLT_WIDTH/2)),(bolt.y + (BOLT_HEIGHT/2)))
        Bottom_Right = ((bolt.x + (BOLT_WIDTH/2)),(bolt.y - (BOLT_HEIGHT/2)))
        Bottom_Left = ((bolt.x - (BOLT_WIDTH/2)),(bolt.y - (BOLT_HEIGHT/2)))
        if self.contains(Top_Right) or self.contains(Top_Left) or self.contains(Bottom_Right) or self.contains(Bottom_Left):
            return True
        else:
            return False


# self.getis_playerBolt() == True and
class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x-coordinate of Bolt
        """
        return self.x
    def getY(self):
        """
        Returns the y-coordinate of Bolt
        """
        return self.y
    # def getVelocity(self):
    #     return self.velocity
    def getis_playerBolt(self):
        """
        Returns the attribute is_playerBolt
        """
        return self.is_playerBolt
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y, state):
        """
        initializes Bolt
        """
        super().__init__(x = x, y = y, width = BOLT_WIDTH, height = BOLT_HEIGHT,linecolor = 'red', fillcolor = 'red', velocity = BOLT_SPEED)
        self.is_playerBolt = state
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def moveBolt(self):
        """
        moves the bolt shot from the ship
        """
        self.y += BOLT_SPEED
    def moveABolt(self):
        """
        moves the bolt shot from the aliens
        """
        self.y -= BOLT_SPEED
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
