##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : game_scene.py                                                 ##
##  Project   : Game_Taz                                                      ##
##  Date      : Sep 07, 2015                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2015 - 2018                                      ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

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
        for i in range(0, GameScene._TRACKS_COUNT):
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
        if(input.is_click(input.KEY_PAUSE)):
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
        if(input.is_click(input.KEY_PAUSE)):
            self._game_state = GameScene._STATE_PLAYING;


    def _update_game_over(self, dt):
        ## Input
        if(input.is_click(input.KEY_SELECTION, input.KEY_PAUSE)):
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
