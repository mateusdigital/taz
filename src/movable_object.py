#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        movable_object.py                         ##
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

################################################################################
## MovableObject                                                              ##
################################################################################
class MovableObject(Sprite):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    DIRECTION_LEFT   = -1;
    DIRECTION_RIGHT  = +1;
    HORIZONTAL_SPEED = 200;

    STATE_NORMAL = 1;
    STATE_DEATH  = 2;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction,
                speed_factor, out_of_field_callback):

        Sprite.__init__(self);

        ## iVars ##
        #Private
        self.__track_index           = track_index;
        self.__direction             = direction;
        self.__speed_factor          = speed_factor;
        self.__target_position_x     = 0;
        self.__out_of_field_callback = out_of_field_callback;
        #Protected.
        self._state                  = MovableObject.STATE_NORMAL;

        #Set the position.
        y = GameFieldConstants.FIELD_TRACKS_Y[track_index];
        x = GameFieldConstants.FIELD_HARD_LEFT;
        if(direction == MovableObject.DIRECTION_LEFT):
            x = GameFieldConstants.FIELD_HARD_RIGHT;

        self.set_position(x, y);

        #Set target position.
        self.__target_position_x = GameFieldConstants.FIELD_HARD_RIGHT;
        if(direction == MovableObject.DIRECTION_LEFT):
            self.__target_position_x = GameFieldConstants.FIELD_HARD_LEFT;


    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def get_track_index(self):
        return self.__track_index;

    def get_state(self):
        return self._state;


    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        pos_x  = self.get_position_x();
        size_w = self.get_size_w();

        out_of_field = False;

        #Moving to right.
        if((self.__direction == MovableObject.DIRECTION_RIGHT) and
           (pos_x > self.__target_position_x)):
                out_of_field = True;

        #Moving to left.
        elif((self.__direction == MovableObject.DIRECTION_LEFT) and
             (pos_x + size_w < self.__target_position_x)):
                out_of_field = True;

        if(out_of_field):
            self._state = MovableObject.STATE_DEATH;
            self.__out_of_field_callback(self);
        else:
            speed = MovableObject.HORIZONTAL_SPEED * self.__direction * self.__speed_factor;
            self.move_x(speed * (dt / 1000.0));



################################################################################
## Food                                                                       ##
################################################################################
class Food(MovableObject):
    ############################################################################
    ## CONSTANTS                                                              ##
    ############################################################################
    STATE_EAT          = 3;
    TIME_TO_KEEP_DEATH = 2000;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction, speed_factor,
                 out_of_field_callback,
                 eat_callback,
                 death_callback):

        #Call baseclass CTOR.
        MovableObject.__init__(self, track_index, direction, speed_factor,
                               out_of_field_callback);

        ## iVars ##
        self.__eat_callback   = eat_callback;
        self.__death_callback = death_callback;

        #Load the Sprites.
        self.load_image(Sprites.Food);

        #Initialize the Eat timer;
        self.__eat_timer = BasicClock(Food.TIME_TO_KEEP_DEATH);
        self.__eat_timer.set_callback(self.__on_eat_timer_tick);


    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def collide_with_taz(self, taz):
        if(self._state != MovableObject.STATE_NORMAL):
            return;

        if(pygame.rect.Rect.colliderect(self.rect, taz.rect)):
            self.__change_state_to_eat();


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def __on_eat_timer_tick(self):
        self.__change_state_to_dead();


    ############################################################################
    ## State Functions                                                        ##
    ############################################################################
    def __change_state_to_eat(self):
        self.image.fill((255, 0, 255));

        self._state = Food.STATE_EAT;
        self.__eat_timer.start();
        self.__eat_callback(self);

    def __change_state_to_dead(self):
        self._state = MovableObject.STATE_DEATH;
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

