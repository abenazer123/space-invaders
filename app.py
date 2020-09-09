"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Abenazer Mekete agm246
12/6/2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    """

    def start(self):
        """
        Initializes the application.

        """
        # IMPLEMENT ME

        self._state = STATE_INACTIVE
        self.lastkeys = 0
        self.completeText1 = None
        self._completeText2 = None
        self.drawend = None
        if self._state == STATE_INACTIVE:
            self._wave = None
        elif self._state == STATE_ACTIVE:
            self._text = None

        self._text = GLabel(text = 'Press P to start',font_size = 52, x = GAME_WIDTH/2, y = GAME_HEIGHT/2, halign = 'center',
                    valign = 'middle', font_name = 'Arcade.ttf')
        self._pauseText = GLabel(text = 'Press C to Continue', x = GAME_WIDTH / 2, y = GAME_HEIGHT / 2, halign = 'center', valign = 'middle',
                            font_size = 50, font_name = 'Arcade.ttf')
        self._completeText1 = GLabel(text = 'WIN', x = GAME_WIDTH / 2, y = GAME_HEIGHT / 2, halign = 'center', valign = 'middle',
                            font_size = 50, font_name = 'Arcade.ttf')
        self._completeText2 = GLabel(text = 'You Lose', x = GAME_WIDTH / 2, y = GAME_HEIGHT / 2, halign = 'center', valign = 'middle',
                            font_size = 50, font_name = 'Arcade.ttf')

        isinstance(self.view, GView)
        isinstance(self.input, GInput)
        isinstance(self._wave, Wave)
        isinstance(self._text, GLabel)
    def update(self,dt):
        """
        Animates a single frame in the game.

        """
        # IMPLEMENT ME

        # self._changeState()
        # keyCount = self._input.key_count
        # change = keyCount > 0 and self.lastkeys == 0

        # self.lastkeys = keyCount
        self._changeStateNewave()
        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        elif self._state == STATE_ACTIVE and self._wave.getAliens() != None:
            self._wave.update2(self.input,dt)
            self.changeStateCompPaused()
        elif self._state == STATE_PAUSED:
            self.checkPauseState()
        elif self._state == STATE_COMPLETE:
            if self._wave.getComplete() == 1:
                self._completeText1.draw(self.view)
            elif self._wave.getComplete() == 2:
                self._completeText2.draw(self.view)
            # elif self._wave.getComplete() == 2:
            #     self._completeText2.draw(self.view)
    def draw(self):
        """
        Draws the game objects to the view.

        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
        elif self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE:
            self._wave.draw2(self.view)
        elif self._state == STATE_PAUSED:
            self._wave.draw2(self.view)
            self._pauseText.draw(self.view)
        # elif self._state == STATE_COMPLETE:




    # HELPER METHODS FOR THE STATES GO HERE
    def _changeStateNewave(self):
        """
        changes the state when the user wants to start the game
        """
        if self.input.is_key_down('p'):
            self._state = STATE_NEWWAVE

    def changeStateCompPaused(self):
        """
        changes the state when the game is complete or when the user is out of Lives
        """
        if self._wave.getComplete() == 1:
            self._state = STATE_COMPLETE
        if self._wave.getComplete() == 2:
            self._state = STATE_COMPLETE
        if self._wave.getPaused() == True:
            self._wave.setLives(self._wave.getLives() - 1)
            if self._wave.getLives() < 1:
                # self._state = STATE_COMPLETE
                self._wave.complete = 2
            else:
                self._state = STATE_PAUSED

    def checkPauseState(self):
        """
        changes the state when the user wants to resume game
        """

        if self.input.is_key_down('c'):
            self._wave.setPaused(False)
            self._state = STATE_ACTIVE
