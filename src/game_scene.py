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
#Python
import pdb; # :~)
import random;
#Pygame
import pygame;
#Project
from   clock                import BasicClock;
from   game                 import Constants;
from   game                 import Director;
from   game_field_constants import GameFieldConstants;
from   movable_object       import Food;
from   movable_object       import MovableObject;
from   resources            import Sprites;
from   scene                import Scene;
from   scene                import Sprite;
from   taz                  import Taz;
import menu_scene; #To avoid circular imports;

class GameScene(Scene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __EAT_THRESHOLD          = [30, 60, 90, 150, 200, 250,350, 450, 600];
    __SPEED_FACTOR_INCREMENT = 0.2;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);
        ## iVars ##
        self.__speed_factor = 1;

        #GameField.
        self.__game_field = Sprite();
        self.__game_field.load_image(Sprites.GameField);
        self.__game_field.set_position(8, 30);
        self.add(self.__game_field);

        #AmazingCowLogo.
        self.__cow_logo = Sprite();
        self.__cow_logo.load_image(Sprites.AmazingCowGameLogo);
        self.__cow_logo.set_position(9, 345);
        self.add(self.__cow_logo);

        #Bombs/Foods
        self.__movable_objects = [None] * GameFieldConstants.FIELD_TRACKS_LEN;
        for _ in xrange(0, GameFieldConstants.FIELD_TRACKS_LEN):
            self.__create_movable_object();

        #Taz.
        self.__taz = Taz(self.__on_taz_death);
        self.add(self.__taz, layer=1);


    ############################################################################
    ## Movable Objects Management                                             ##
    ############################################################################
    def __create_movable_object(self):
        #Direction.
        direction = MovableObject.DIRECTION_RIGHT;
        if(random.randint(0, 1) % 2 == 0):
            direction = MovableObject.DIRECTION_LEFT;

        #Track Index.
        track_index = -1;
        while(True):
            index = random.randint(0, GameFieldConstants.FIELD_TRACKS_LEN -1);
            if(self.__movable_objects[index] is None):
                track_index = index;
                break;

        type_index  = random.randint(0, 1);
        mobject = Food(track_index,
                       direction,
                       self.__speed_factor,
                       self.__on_movable_object_out_of_field,
                       self.__on_food_eat,
                       self.__on_food_death);

        self.add(mobject, layer=0);
        self.__movable_objects[track_index] = mobject;

    def __remove_movable_object(self, movable_object):
        self.__movable_objects[movable_object.get_track_index()] = None;
        self.remove(movable_object);
        self.__create_movable_object();


    ############################################################################
    ## Object Callbacks                                                       ##
    ############################################################################
    def __on_taz_death(self):
        print "TAZ DEATH";

    def __on_food_death(self, food):
        self.__remove_movable_object(food);

    def __on_movable_object_out_of_field(self, movable_object):
       self.__remove_movable_object(movable_object);

    def __on_food_eat(self, food):
        self.__taz.increment_eat_count();
        print self.__taz.get_eat_count();
        if(self.__taz.get_eat_count() in GameScene.__EAT_THRESHOLD):
            self.__speed_factor += GameScene.__SPEED_FACTOR_INCREMENT;


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def draw(self, surface):
        surface.fill(Constants.COLOR_BLACK);
        Scene.draw(self, surface);

    def update(self, dt):
        #Get the state of keyboard.
        keys = pygame.key.get_pressed();

        #Set the Taz Controls.
        self.__taz.set_controls(Taz.CONTROL_LEFT,  keys[pygame.locals.K_LEFT]);
        self.__taz.set_controls(Taz.CONTROL_RIGHT, keys[pygame.locals.K_RIGHT]);
        self.__taz.set_controls(Taz.CONTROL_DOWN,  keys[pygame.locals.K_DOWN]);
        self.__taz.set_controls(Taz.CONTROL_UP,    keys[pygame.locals.K_UP]);

        #Update the Taz and the MovableObjects.
        self.__taz.update(dt);

        for obj in self.__movable_objects:
            if(obj is not None):
                obj.update(dt);

        #Check the collisions.
        for obj in self.__movable_objects:
            if(obj is not None):
                obj.collide_with_taz(self.__taz);

    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type != pygame.locals.KEYDOWN):
            return;

        key = event.key;
        #Up and Down change the option.
        if(key == pygame.locals.K_ESCAPE):
            self.__change_to_menu_scene();


    ############################################################################
    ## Ohter Functions                                                        ##
    ############################################################################
    def __change_to_menu_scene(self):
        Director.instance().change_scene(menu_scene.MenuScene());
