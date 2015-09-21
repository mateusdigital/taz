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

## Imports ##
#Pygame
import pygame;
#Project
from clock                import BasicClock;
from game_field_constants import GameFieldConstants;
from resources            import Sprites;
from scene                import Sprite;

class Taz(Sprite):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    INITIAL_TRACK_INDEX  = 3;
    INITIAL_POSITION_X   = 200;

    SCALE_FACTOR     = 1.5;
    HORIZONTAL_SPEED = 500;

    TIME_TO_CHANGE_TRACK     = 70;
    TIME_TO_NORMAL_ANIMATION = 150;
    TIME_TO_DEATH_ANIMATION  = 1400;

    STATE_ALIVE = 0;
    STATE_DEAD  = 1;

    CONTROL_UP    = 0;
    CONTROL_DOWN  = 1;
    CONTROL_LEFT  = 2;
    CONTROL_RIGHT = 3;

    MAX_LIVES = 3

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, death_animation_callback):
        Sprite.__init__(self);

        ## iVars ##
        self.__death_animation_callback = death_animation_callback;
        self.__state                    = Taz.STATE_ALIVE;
        self.__lives                    = Taz.MAX_LIVES;
        self.__controls                 = [False, False, False, False];
        self.__eat_count                = 0;

        #Set the Sprite vars.
        self.__frames = [pygame.image.load(Sprites.Game_TazFrame0),
                         pygame.image.load(Sprites.Game_TazFrame1)];
        self.__current_frame = 0;
        self.update_image(self.__frames[0]);

        #Set the Track vars.
        self.__current_track    = GameFieldConstants.TAZ_INITIAL_TRACK_INDEX;
        self.__can_change_track = True;

        #Set the Initial Position.
        self.reset_position();

        #Initialize the Track Change timer.
        self.__change_track_timer = BasicClock(Taz.TIME_TO_CHANGE_TRACK);
        self.__change_track_timer.set_callback(self.__on_change_track_timer_tick);

        #Initialize the Normal Animation timer.
        self.__normal_animation_timer = BasicClock(Taz.TIME_TO_NORMAL_ANIMATION);
        self.__normal_animation_timer.set_callback(self.__on_normal_animation_timer_tick);

        #Initialize the Death Animation Timer.
        self.__death_animation_timer = BasicClock(Taz.TIME_TO_DEATH_ANIMATION);
        self.__death_animation_timer.set_callback(self.__on_death_animation_timer_tick);

        #Start the Normal animation timer.
        self.__normal_animation_timer.start();


    ############################################################################
    ## Public Functions                                                       ##
    ############################################################################
    def set_controls(self, control_index, control_state):
        self.__controls[control_index] = control_state;

    def increment_eat_count(self):
        self.__eat_count += 1;

    def get_eat_count(self):
        return self.__eat_count;

    def get_lives(self):
        return self.__lives;

    def get_state(self):
        return self.__state;

    def set_dead(self):
        self.__change_state_to_dead();

    def reset_position(self):
        self.set_position(GameFieldConstants.TAZ_INITIAL_POSITION_X,
                          GameFieldConstants.TAZ_INITIAL_POSITION_Y);

    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        #Update the timers...
        self.__change_track_timer.update(dt);
        self.__normal_animation_timer.update(dt);
        self.__death_animation_timer.update(dt);

        #If dead do not move.
        if(self.__state == Taz.STATE_DEAD):
            return;

        #Vertical Movement.
        if(self.__can_change_track):
            if(self.__controls[Taz.CONTROL_DOWN]): self.__change_track(+1);
            if(self.__controls[Taz.CONTROL_UP  ]): self.__change_track(-1);

        #Horizontal Movement.
        if(self.__controls[Taz.CONTROL_LEFT ]): self.__move_horizontal(-1, dt);
        if(self.__controls[Taz.CONTROL_RIGHT]): self.__move_horizontal(+1, dt);


    ############################################################################
    ## Time Callbacks                                                         ##
    ############################################################################
    def __on_change_track_timer_tick(self):
        self.__can_change_track = True;
        self.__change_track_timer.stop();

    def __on_normal_animation_timer_tick(self):
        curr_frame_img = self.__frames[self.__current_frame];

        #If Taz is dead we will stretch it a little bit.
        #Otherwise just update the frame.
        if(self.__state == Taz.STATE_DEAD):
            scalled_w  = int(self.get_size_w() * Taz.SCALE_FACTOR);
            self.image = pygame.transform.scale(curr_frame_img,
                                                (scalled_w,
                                                 self.get_size_h()));
        else:
            self.image = curr_frame_img;

        self.__current_frame = (self.__current_frame + 1) % 2;

    def __on_death_animation_timer_tick(self):
        self.__death_animation_callback();
        self.__change_state_to_alive();


    ############################################################################
    ## Movement Functions                                                     ##
    ############################################################################
    def __change_track(self, delta):
        #Change the track, set that Taz cannot change track for
        #a while start the timer to make Taz change track again.
        self.__current_track   += delta;
        self.__can_change_track = False;
        self.__change_track_timer.start();

        #Keep Taz inside the Track bounds.
        if(self.__current_track < 0):
            self.__current_track = 0;

        elif(self.__current_track >= GameFieldConstants.FIELD_TRACKS_LEN):
            self.__current_track = GameFieldConstants.FIELD_TRACKS_LEN -1;

        #Finally set the Y position to the track.
        self.set_position_y(GameFieldConstants.FIELD_TRACKS_Y[self.__current_track]);

    def __move_horizontal(self, dir, dt):
        #Move.
        speed = Taz.HORIZONTAL_SPEED * dir;
        self.move_x(speed * (dt / 1000.0));

        #Constraint to field bounds...
        x = self.get_position_x();

        if(x <= GameFieldConstants.FIELD_SOFT_LEFT):
            x = GameFieldConstants.FIELD_SOFT_LEFT;

        elif(x + self.get_size_w() >= GameFieldConstants.FIELD_SOFT_RIGHT):
            x = GameFieldConstants.FIELD_SOFT_RIGHT - self.get_size_w();

        self.set_position_x(x);


    ############################################################################
    ## State Functions                                                        ##
    ############################################################################
    def __change_state_to_alive(self):
        self.__death_animation_timer.stop();
        self.__state = Taz.STATE_ALIVE;

    def __change_state_to_dead(self):
        self.__death_animation_timer.start();
        self.__state = Taz.STATE_DEAD;
        self.__lives -= 1;

