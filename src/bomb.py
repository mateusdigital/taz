#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        bomb.py                                   ##
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
## Bomb                                                                       ##
################################################################################
class Bomb(MovableObject):

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction, speed_factor,
                 out_of_field_callback,
                 collision_callback):

        #Call baseclass CTOR.
        MovableObject.__init__(self, track_index, direction, speed_factor,
                               out_of_field_callback,
                               collision_callback);

        #Load the Sprites.
        self.load_image(Sprites.Game_Bomb);

    ############################################################################
    ## Override State Methods                                                 ##
    ############################################################################
    def _change_state_to_collided(self):
        pass;

    def _change_state_to_out_of_field(self):
        pass;


