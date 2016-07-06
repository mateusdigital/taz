# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        enemy.py                                  ##
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
## Pygame ##
import pygame;
## Game_Taz ##
import assets;
import director;
from cowclock import *;


class Enemy:
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    _SPEED      = 150;
    _NEXT_SPEED = 150;

    _SURFACES = None;

    _SURFACE_TYPE_FOOD   = 0;
    _SURFACE_TYPE_CAUGHT = 1;
    _SURFACE_TYPE_BOMB   = 2;

    _OUT_OF_BOUNDS_INTERVAL_MIN = 0.4;
    _OUT_OF_BOUNDS_INTERVAL_MAX = 1.0;
    _CAUGHT_INTERVAL            =   1;


    ############################################################################
    ## Static Methods                                                         ##
    ############################################################################
    @staticmethod
    def LoadAssets():
        if(Enemy._SURFACES is None):
            Enemy._SURFACES = [
                assets.load_image("Food.png"  ),
                assets.load_image("Caught.png"),
                assets.load_image("Bomb.png"  )
            ];

    @staticmethod
    def GetSurface(type):
        return Enemy._SURFACES[type];

    @staticmethod
    def Accelerate(ammount):
        Enemy._NEXT_SPEED += ammount;

    @staticmethod
    def GetNextSpeed():
        return Enemy._NEXT_SPEED;


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self,
                 min_bounds, max_bounds,
                 tracks_count, track_offset,
                 track_index):
        ## Pre init
        Enemy.LoadAssets();

        ## Housekeeping
        self._type                      = None;
        self._reset_out_of_bounds_timer = None;
        self._reset_caught_timer        = None;

        ## Surface
        self._surface = None;
        self._visible = False;

        ## Movement / Bounds
        self._position     = [0, 0];
        self._speed        = Enemy.GetNextSpeed();
        self._min_bounds   = min_bounds;
        self._max_bounds   = max_bounds;
        self._tracks_count = tracks_count;
        self._track_offset = track_offset;
        self._track_index  = track_index;

        ## Complete initialization.
        self._init_timers ();
        self.reset();



    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def check_collision(self, other_rect):
        ## We can pass through the caught foods.
        if(self._type == Enemy._SURFACE_TYPE_CAUGHT or \
           self._visible == False):
            return False;

        this_rect = pygame.Rect(self._position, self._surface.get_size());
        collided  = this_rect.colliderect(other_rect);

        ## Collision with the Food.
        ## Make it a Food Caught
        if(collided and self._type == Enemy._SURFACE_TYPE_FOOD):
            self._type = Enemy._SURFACE_TYPE_CAUGHT;
            self._reset_caught_timer.start();

        return collided;


    def is_fatal(self):
        return self._type == Enemy._SURFACE_TYPE_BOMB;


    def reset(self):
        self._visible = False;

        ## Reset the Out of Bounds timer.
        out_time = director.randfloat(
                        Enemy._OUT_OF_BOUNDS_INTERVAL_MIN,
                        Enemy._OUT_OF_BOUNDS_INTERVAL_MAX
                   );

        self._reset_out_of_bounds_timer.stop();
        self._reset_out_of_bounds_timer.set_time(out_time);
        self._reset_out_of_bounds_timer.start();


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        ## Timers
        self._reset_out_of_bounds_timer.update(dt);
        self._reset_caught_timer.update       (dt);

        ## Enemy reset cooldown is active, we don't need to anything more...
        if(self._reset_out_of_bounds_timer.is_enabled() or \
           self._reset_caught_timer.is_enabled()):
            return;

        ## Position
        self._position[0] += (self._speed * dt);

        ## Check Boundaries
        if(self._speed > 0 and self._position[0] > self._max_bounds[0]):
            self.reset();

        elif(self._speed < 0 and self._position[0] < self._min_bounds[0]):
            self.reset();


    def draw(self, surface):
        if(not self._visible):
            return;

        self._surface = Enemy.GetSurface(self._type);
        surface.blit(self._surface, self._position);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    def _init_timers(self):
        self._reset_out_of_bounds_timer = CowClock(
            time          = 0,
            done_callback = self._reset_helper
        );

        ## Caught
        self._reset_caught_timer = CowClock(
            time          = Enemy._CAUGHT_INTERVAL,
            done_callback = self.reset
        );

    def _reset_helper(self):
        self._speed = Enemy.GetNextSpeed();

        self._decide_type     ();
        self._decide_direction();

        self._visible = True;

    def _decide_type(self):
        is_bomb = director.randbool();
        if(is_bomb):
            self._type = Enemy._SURFACE_TYPE_BOMB;
        else:
            self._type = Enemy._SURFACE_TYPE_FOOD;

        self._surface = Enemy.GetSurface(self._type);


    def _decide_direction(self):
        ## Y Position
        self._position[1] = (self._track_index * self._track_offset) \
                            + self._min_bounds[1];

        ## X Position, depends on the direction of movement.
        ## If Enemy is moving to Right it starts on LEFT
        ## If Enemy is moving to Left  it starts on Right
        move_to_right = director.randbool();
        if(move_to_right):
            self._position[0] = self._min_bounds[0];
            self._speed       = abs(self._speed);
        else:
             self._position[0] = self._max_bounds[0];
             self._speed     = -(abs(self._speed));
