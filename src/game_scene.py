#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        game_scene.py                             ##
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

################################################################################
## Imports                                                                    ##
################################################################################
## Pygame ##
import pygame;
## Project ##
import director;
import assets;
import sound;
import position_helpers;
from constants import *;
from taz       import *;


class GameScene():
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    _STATE_GAME_OVER = 0;
    _STATE_NEW_TURN  = 1;
    _STATE_END_TURN  = 2;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        director.set_clear_color(COLOR_BLACK);

        self._game_state = None;

        self._game_field     = assets.load_image("GameField.png");
        self._game_field_pos = position_helpers.get_center_on(
                                       self._game_field,
                                       director.get_draw_surface()
                               );
        game_field_size = self._game_field.get_size();

        self._taz = Taz(
            min_bounds = [self._game_field_pos[0] + 28,
                          self._game_field_pos[1] + 32],
            max_bounds = [self._game_field_pos[0] + game_field_size[0] - 28,
                          self._game_field_pos[1] + game_field_size[1] - 32]
        );
        self._enemies = [];



    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def draw(self, surface):
        surface.blit(self._game_field, self._game_field_pos);
        self._taz.draw(surface);

    def update(self, dt):
        self._taz.update(dt);


    ############################################################################
    ## Object Callbacks                                                       ##
    ############################################################################
