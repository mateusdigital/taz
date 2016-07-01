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
import pygame.locals;
## Project ##
import director;
import assets;
import sound;
import input;
import position_helpers;
from constants import *;
from taz       import *;
from hud       import *;


class GameScene():
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    _STATE_PLAYING   = 0;
    _STATE_PAUSED    = 1;
    _STATE_GAME_OVER = 2;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        director.set_clear_color(COLOR_BLACK);

        ## Housekeeping
        self._game_state = GameScene._STATE_PLAYING;

        ## Game Field
        self._game_field     = assets.load_image("GameField.png");
        game_field_size      = self._game_field.get_size();
        self._game_field_pos = (GAME_WIN_CENTER_X - game_field_size[0] * 0.5,
                                GAME_WIN_CENTER_Y - game_field_size[1] * 0.5);

        game_field_size = self._game_field.get_size();
        game_field_min = [self._game_field_pos[0] + 28,
                          self._game_field_pos[1] + 32];
        game_field_max = [self._game_field_pos[0] + game_field_size[0] - 28,
                          self._game_field_pos[1] + game_field_size[1] - 32];

        ## Taz
        #COWTODO: Remove the magic numbers.
        self._taz = Taz(
            min_bounds  = game_field_min,
            max_bounds  = game_field_max,
            is_playable = True,
            dead_animation_callback = self._on_taz_dead_animation_done
        );

        ## Enemies
        self._enemies = [];


        ## Hud
        self._hud = Hud(game_field_min, game_field_max);


    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        if(self._game_state == GameScene._STATE_PLAYING):
            self._update_playing(dt);
        elif(self._game_state == GameScene._STATE_PAUSED):
            self._update_paused(dt);
        elif(self._game_state == GameScene._STATE_GAME_OVER):
            self._update_game_over(dt);


    def _update_playing(self, dt):
        ## Input
        if(input.is_click(pygame.locals.K_p)):
            self._game_state = GameScene._STATE_PAUSED;
            return;

        ## Updates
        self._taz.update(dt);
        #COWTODO: Enemies...

        self._hud.update(dt);
        ## Collisions
        #COWTODO: Implement...


    def _update_paused(self, dt):
        ## Input
        if(input.is_click(pygame.locals.K_p)):
            self._game_state = GameScene._STATE_PLAYING;


    def _update_game_over(self, dt):
        ## Input
        if(input.is_click(pygame.locals.K_SPACE)):
            director.go_to_menu();


    ############################################################################
    ## Draw                                                                   ##
    ############################################################################
    def draw(self, surface):
        surface.blit(self._game_field, self._game_field_pos);
        self._hud.draw(surface);
        self._taz.draw(surface);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    def _on_taz_dead_animation_done(self):
        self._hud.remove_live();

        ## Check Game State.
        if(self._taz.get_lives() == 0):
            self._game_state = GameScene._STATE_GAME_OVER;
            return;

        #COWTODO: Restart the enemies...
        self._taz.reset();

