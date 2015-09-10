#!/usr/bin/python
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
## Imports ##
#Pygame
import pygame;
#Project
from game       import Director;
from scene      import Scene;
from scene      import Sprite;
from clock      import BasicClock;
from resources  import Sprites;
import menu_scene; #To avoid circular imports;

import pdb;

################################################################################
## MovableObject                                                              ##
################################################################################
class MovableObject(Sprite):
    TYPE_BOMB = 0;
    TYPE_FOOD = 1;

    DIRECTION_LEFT  = +1;
    DIRECTION_RIGHT = -1;

    def __init__(self, type, track_index, direction):
        Sprite.__init__(self);

        ## iVars ##
        self.__type        = type;
        self.__track_index = track_index;
        self.__direction   = direction;

        #Load the correct sprite based upon the type.
        if(self.__type == MovableObject.TYPE_FOOD):
            self.load_image(Sprites.Food);
        else:
            self.load_image(Sprites.Food);

        #Set the position.
        y = GameScene.FIELD_TRACKS_Y[track_index];
        x = GameScene.FIELD_HARD_LEFT;
        if(direction == MovableObject.DIRECTION_LEFT):
            x = GameScene.FIELD_HARD_RIGHT;

        self.set_position(x, y);

    def update(self, dt):
        self.move_x(-200 * self.__direction * (dt / 1000.0));



################################################################################
## Taz                                                                        ##
################################################################################
class Taz(Sprite):
    TIME_TO_CHANGE_TRACK = 30;
    HORIZONTAL_SPEED     = 500;

    def __init__(self):
        Sprite.__init__(self);

        self.load_image(Sprites.Taz);

        x = 200;
        y = GameScene.FIELD_TRACKS_Y[3];
        self.set_position(x, y);

        self.__current_track = 3;
        self.__can_change_track = True;
        self.__change_track_timer = BasicClock(Taz.TIME_TO_CHANGE_TRACK);
        # self.__change_track_timer.set_time();
        self.__change_track_timer.set_callback(self.on_change_track_timer_tick);

    def on_change_track_timer_tick(self):
        self.__can_change_track = True;
        self.__change_track_timer.stop();

    def change_track(self, delta):
        self.__current_track += delta;
        self.__change_track_timer.start();
        self.__can_change_track = False;

        if(self.__current_track < 0):
            self.__current_track = 0;
        elif(self.__current_track >= len(GameScene.FIELD_TRACKS_Y)):
            self.__current_track = len(GameScene.FIELD_TRACKS_Y) -1;

        self.set_position_y(GameScene.FIELD_TRACKS_Y[self.__current_track]);

    def move_horizontal(self, dir, dt):
        speed = Taz.HORIZONTAL_SPEED * dir;
        self.move_x(speed * (dt / 1000.0));

        x = self.get_position_x();
        # print x;
        if(x <= 35): x = 35;
        elif(x >= 409): x = 409;
        self.set_position_x(x);

    def update(self, dt):
        keys = pygame.key.get_pressed();
        speed = 0;

        self.__change_track_timer.update(dt);

        #Vertical Movement.
        if(self.__can_change_track):
            if(keys[pygame.locals.K_DOWN]): self.change_track(+1);
            if(keys[pygame.locals.K_UP  ]): self.change_track(-1);

        #Horizontal Movement.
        if(keys[pygame.locals.K_LEFT ]): self.move_horizontal(-1, dt);
        if(keys[pygame.locals.K_RIGHT]): self.move_horizontal(+1, dt);








################################################################################
## GameScene                                                                  ##
################################################################################
class GameScene(Scene):
    FIELD_TRACKS_Y   = [62, 94, 126, 158, 190, 222, 254, 285];
    FIELD_HARD_LEFT  = -32 + 10;
    FIELD_HARD_RIGHT = 480 - 10;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);

        #GameField.
        self.game_field = Sprite();
        self.game_field.load_image(Sprites.GameField);
        self.game_field.set_position(8, 30);
        self.add(self.game_field);

        #AmazingCowLogo.
        self.cow_logo = Sprite();
        self.cow_logo.load_image(Sprites.AmazingCowGameLogo);
        self.cow_logo.set_position(9, 345);
        self.add(self.cow_logo);

        #Taz.
        self.taz = Taz();
        self.add(self.taz);

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def draw(self, surface):
        surface.fill((0,0,0));
        Scene.draw(self, surface);

    def update(self, dt):
        self.taz.update(dt);

    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type != pygame.locals.KEYDOWN):
            return;

        key = event.key;
        #Up and Down change the option.
        if(key == pygame.locals.K_ESCAPE):
            exit(0);
            # self.change_to_menu_scene();

        # key = event.key;
        # #Up and Down change the option.
        # if(key == pygame.locals.K_UP or key == pygame.locals.K_DOWN):
        #     self.change_menu_option();
        # #Enter commit the selection.
        # elif(key == pygame.locals.K_RETURN):
        #     self.change_scene();


    def change_to_menu_scene(self):
        Director.instance().change_scene(menu_scene.MenuScene());
