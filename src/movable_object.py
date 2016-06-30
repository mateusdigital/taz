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

    STATE_NORMAL       = 1;
    STATE_COLLIDED     = 2;
    STATE_OUT_OF_FIELD = 3;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction, speed_factor,
                 out_of_field_callback,
                 collision_callback):

        Sprite.__init__(self); #Base class CTOR.

        ## iVars ##
        #Private
        self.__track_index           = track_index;
        self.__direction             = direction;
        self.__speed_factor          = speed_factor;
        self.__target_position_x     = 0;

        self.__out_of_field_callback = out_of_field_callback;
        self.__collision_callback    = collision_callback;

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

    def collide_with_taz(self, taz):
        #Check if already collided with taz.
        if(self._state != MovableObject.STATE_NORMAL):
            return;

        #Check if Taz intersects with this object and
        #give a change to object to change the internal state
        #and inform the collision to listener.
        if(pygame.rect.Rect.colliderect(self.rect, taz.rect)):
            self._state = MovableObject.STATE_COLLIDED;
            self._change_state_to_collided();
            self.__collision_callback(self);


    ############################################################################
    ## Abstract State Methods                                                 ##
    ############################################################################
    def _change_state_to_collided(self):
        print "MUST OVERRIDE _change_state_to_collided", self;
        exit(1);

    def _change_state_to_out_of_field(self):
        print "MUST OVERRIDE _change_state_to_out_of_field", self;
        exit(1);

    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        #Only move if state is Normal.
        if(self._state != MovableObject.STATE_NORMAL):
            return ;

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


        #Object is out of field, so give a change to object change
        #the internal state and inform it to listener.
        if(out_of_field):
            self._state = MovableObject.STATE_OUT_OF_FIELD;
            self._change_state_to_out_of_field();
            self.__out_of_field_callback(self);

        #Object is inside of field, keep moving.
        else:
            speed = MovableObject.HORIZONTAL_SPEED * self.__direction * self.__speed_factor;
            print "SPEEEEED: ", speed * (dt / 1000.0);
            self.move_x(speed * (dt / 1000.0));

