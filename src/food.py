#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        food.py                                   ##
##             ████████████         Game Taz                                  ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
#Pygame
import pygame;
#Project
from clock                import BasicClock;
from game_field_constants import GameFieldConstants;
from resources            import Sprites;
from scene                import Sprite;
from movable_object       import MovableObject;


################################################################################
## Food                                                                       ##
################################################################################
class Food(MovableObject):
    ############################################################################
    ## CONSTANTS                                                              ##
    ############################################################################
    STATE_DEATH        = 1000;
    TIME_TO_KEEP_DEATH = 2000;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction, speed_factor,
                 out_of_field_callback,
                 collision_callback,
                 death_callback):

        #Call baseclass CTOR.
        MovableObject.__init__(self, track_index, direction, speed_factor,
                               out_of_field_callback,
                               collision_callback);

        ## iVars ##
        self.__death_callback = death_callback;

        #Load the Sprites.
        self.load_image(Sprites.Game_FoodFrame0);

        #Initialize the Eat timer;
        self.__eat_timer = BasicClock(Food.TIME_TO_KEEP_DEATH);
        self.__eat_timer.set_callback(self.__on_eat_timer_tick);


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def __on_eat_timer_tick(self):
        self.__change_state_to_dead();


    ############################################################################
    ## Override State Methods                                                 ##
    ############################################################################
    def _change_state_to_collided(self):
        self.load_image(Sprites.Game_FoodFrame1);
        self.__eat_timer.start();

    def _change_state_to_out_of_field(self):
        pass;

    def __change_state_to_dead(self):
        self._state = Food.STATE_DEATH;
        self.__eat_timer.stop();
        self.__death_callback(self);


    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        #Update the timer (if Food isn't ate, this timer won't do nothing.)
        self.__eat_timer.update(dt);

        #Call the base class function to keep the movement
        #only if food isn't ate.
        if(self._state == MovableObject.STATE_NORMAL):
            MovableObject.update(self, dt);



