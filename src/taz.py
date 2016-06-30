#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        taz.py                                    ##
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
import pygame.locals;
## NumPy ##
import numpy;
## Project ##
import assets;
import input;
from cowclock import *;



class Taz():
    ############################################################################
    ## Constatns                                                              ##
    ############################################################################
    ## Public ##
    STATE_ALIVE = 0;
    STATE_DYING = 1;
    STATE_DEAD  = 2;
    MAX_LIVES   = 3;

    ## Private ##
    _FRAMES_COUNT          = 2;
    _TRACKS_COUNT          = 8;
    _ANIMATION_INVERVAL    = 0.15;
    _CHANGE_TRACK_INTERVAL = 0.15; #COWTODO: TWEAK
    _DEATH_INTERVAL        = 1.00; #COWTODO: TWEAK
    _TRACK_OFFSET          = 32;
    _SPEED                 = 300; #COWTODO: TWEAK


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self, min_bounds, max_bounds, is_playable):
        ## Housekeeping
        self._state       = Taz.STATE_ALIVE;
        self._lives       = Taz.MAX_LIVES;
        self._eat_count   = 0;
        self._is_playable = is_playable;

        ## Frames / Animation
        self._frames           = [];
        self._animation_timer  = None;
        self._death_timer      = None;
        self._frame_size       = None;

        ## Movement / Bounds
        self._curr_track_index   = 0;
        self._can_change_track   = False;
        self._position           = [min_bounds[0], min_bounds[1]];
        self._min_bounds         = min_bounds;
        self._max_bounds         = max_bounds;
        self._track_change_timer = None;

        ## Complete initialization.
        self._init_frames();
        self._init_timers();


    ############################################################################
    ## Public Functions                                                       ##
    ############################################################################
    ## Eat
    def make_eat(self):
        if(self._state != Taz.STATE_ALIVE):
            return;

        self._eat_count += 1;

    def get_eat_count(self):
        return self._eat_count;

    ## Lives
    def kill(self):
        if(self._state != Taz.STATE_ALIVE):
            return;

        self._state = Taz.STATE_DYING;
        self._death_timer.start();

    def get_lives(self):
        return self._lives;

    ## State
    def get_state(self):
        return self._state;

    ## Position / Size
    def set_position(self, x, y):
        self._position = [x, y];

    def get_size(self):
        return self._frame_size;

    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        ## Timers
        self._animation_timer.update   (dt);
        self._track_change_timer.update(dt);
        self._death_timer.update       (dt);

        ## There's anything to do if Taz is dying or dead
        ## (or if it is not playable)...
        if(self._state != Taz.STATE_ALIVE or not self._is_playable):
            return;

        ## Movement
        ## Vertical - Track Based
        if(input.is_down(pygame.locals.K_DOWN) and self._change_track_is_ok()):
            self._curr_track_index += 1;
        elif(input.is_down(pygame.locals.K_UP) and self._change_track_is_ok()):
            self._curr_track_index -= 1;

        ## Horizontal - Pixel/sec Based
        if(input.is_down(pygame.locals.K_LEFT)):
            self._position[0] -= Taz._SPEED * dt;
        elif(input.is_down(pygame.locals.K_RIGHT)):
            self._position[0] += Taz._SPEED * dt;

        ## Maintain the Taz into GameField
        self._curr_track_index = numpy.clip(self._curr_track_index,
                                            0,
                                            Taz._TRACKS_COUNT -1);

        self._position[0] = numpy.clip(self._position  [0],
                                       self._min_bounds[0],
                                       self._max_bounds[0]);


        ## Update the vertical position based upon which track he is.
        self._position[1] = self._curr_track_index * \
                            Taz._TRACK_OFFSET      + \
                            self._min_bounds[1];



    def draw(self, surface):
        ## Do not draw Taz when he's dead.
        if(self._state == Taz.STATE_DEAD):
            return;

        index       = self._animation_timer.get_tick_count() % Taz._FRAMES_COUNT;
        taz_surface = self._frames[index];

        ## When is dying draw Taz scaled horizontally.
        if(self._state == Taz.STATE_DYING):
            taz_surface = pygame.transform.scale(
                                taz_surface,
                                (self._frame_size[0] * 2, self._frame_size[1])
                          );

        surface.blit(taz_surface, self._position);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    ## Inits ##
    def _init_frames(self):
        for i in xrange(0, Taz._FRAMES_COUNT):
            self._frames.append(assets.load_image("TazFrame%d.png" %(i)));

        self._frame_size     = self._frames[0].get_size();
        self._max_bounds[0] -= self._frame_size[0];
        self._max_bounds[1] -= self._frame_size[1];


    def _init_timers(self):
        ## Animation
        self._animation_timer = CowClock(
                                    time         = Taz._ANIMATION_INVERVAL,
                                    repeat_count = CowClock.REPEAT_FOREVER,
                                );

        self._animation_timer.start();

        ## Track Change
        self._track_change_timer = CowClock(
                                        time         = Taz._CHANGE_TRACK_INTERVAL,
                                        repeat_count = 1
                                   );

        ## Death
        self._death_timer = CowClock(
                                time          = Taz._DEATH_INTERVAL,
                                repeat_count  = 1,
                                done_callback = self._on_death_timer_done
                            );


    ## Movement
    def _change_track_is_ok(self):
        #COWTODO: Comment
        is_ok = not self._track_change_timer.is_enabled();
        if(is_ok):
            self._track_change_timer.start();

        return is_ok;


    ## Timer Callbacks
    def _on_death_timer_done(self):
        self._state = Taz.STATE_DEAD;
        self._lives -= 1;
