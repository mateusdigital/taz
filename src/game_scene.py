# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        game_scene.py                             ##
##            █ █        █ █        Game_Taz                                  ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
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
## Python ##
import copy;
## Pygame ##
import pygame;
import pygame.locals;
## Project ##
import director;
import assets;
import sound;
import input;
from constants import *;
from taz       import *;
from enemy     import *;
from hud       import *;


class GameScene():
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    ## Private ##
    _STATE_PLAYING   = 0;
    _STATE_PAUSED    = 1;
    _STATE_GAME_OVER = 2;

    _TRACKS_COUNT =  8;
    _TRACK_OFFSET = 32;
    _TAZ_X_OFFSET = 28;

    _SCORE_MULTIPLIER   = 50;
    _SPEED_UPDATE_COUNT =  5;
    _SPEED_ACCELERATION = 15;


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
        self._game_field_pos = [GAME_WIN_CENTER_X - game_field_size[0] * 0.5,
                                GAME_WIN_CENTER_Y - game_field_size[1] * 0.5];

        game_field_size = self._game_field.get_size();

        ## Taz Min
        taz_field_min     = copy.deepcopy(self._game_field_pos);
        taz_field_min[0] += GameScene._TAZ_X_OFFSET;
        taz_field_min[1] += GameScene._TRACK_OFFSET;
        ## Taz Max
        taz_field_max     = copy.deepcopy(self._game_field_pos);
        taz_field_max[0] += (game_field_size[0] - GameScene._TAZ_X_OFFSET);
        taz_field_max[1] += (game_field_size[1] - GameScene._TRACK_OFFSET);

        ## Enemy Min
        enemy_field_min     = copy.deepcopy(self._game_field_pos);
        enemy_field_min[1] += GameScene._TRACK_OFFSET;
        ## Enemy Max
        enemy_field_max     = copy.deepcopy(self._game_field_pos);
        enemy_field_max[0] += (game_field_size[0] - GameScene._TAZ_X_OFFSET);
        enemy_field_max[1] += game_field_size[1];


        ## Taz
        self._taz = Taz(
            min_bounds   = taz_field_min,
            max_bounds   = taz_field_max,
            tracks_count = GameScene._TRACKS_COUNT,
            track_offset = GameScene._TRACK_OFFSET,
            is_playable  = True,
            dead_animation_callback = self._on_taz_dead_animation_done
        );

        ## Enemies
        self._enemies = [];
        for i in xrange(0, GameScene._TRACKS_COUNT):
            self._enemies.append(
                Enemy(
                    min_bounds   = enemy_field_min,
                    max_bounds   = enemy_field_max,
                    tracks_count = GameScene._TRACKS_COUNT,
                    track_offset = GameScene._TRACK_OFFSET,
                    track_index  = i
                )
            );

        ## Hud
        self._hud = Hud(taz_field_min, taz_field_max);


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
        self._hud.update(dt);
        self._taz.update(dt);


        ## Taz is Dying or dead - We don't need
        ## update the Enemies anymore, them will be reseted
        ## when taz animation is done.
        if(self._taz.get_state() != Taz.STATE_ALIVE):
            return;

        taz_hit_box = self._taz.get_hit_box(); ## Need to be calc'ed 1 time...
        for enemy in self._enemies:
            enemy.update(dt);

            ## Doesn't collided...
            if(not enemy.check_collision(taz_hit_box)):
                continue;

            ## Collided
            if(not enemy.is_fatal()):
                sound.play_eat();

                self._taz.make_eat();
                eat_count = self._taz.get_eat_count();
                self._hud.set_score(
                     eat_count * GameScene._SCORE_MULTIPLIER
                );

                ## Ate enough enmies to accelerate them...
                if(eat_count % GameScene._SPEED_UPDATE_COUNT == 0 and \
                    eat_count != 0):
                    Enemy.Accelerate(GameScene._SPEED_ACCELERATION);

            else:
                sound.play_bomb();
                self._taz.kill();


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

        for enemy in self._enemies:
            enemy.draw(surface);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    def _on_taz_dead_animation_done(self):
        self._hud.remove_live();

        ## Check Game State.
        if(self._taz.get_lives() == 0):
            self._game_state = GameScene._STATE_GAME_OVER;
            return;

        for enemy in self._enemies:
            enemy.reset();

        self._taz.reset();

