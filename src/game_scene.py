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
from   movable_object       import MovableObject;
from   food                 import Food;
from   bomb                 import Bomb;
from   resources            import Sprites;
from   resources            import Fonts;
from   scene                import Scene;
from   scene                import Sprite;
from   taz                  import Taz;
import menu_scene; #To avoid circular imports;

class GameScene(Scene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __EAT_THRESHOLD          = [30, 60, 90, 150, 200, 250,350, 450, 600];
    __SPEED_FACTOR_INCREMENT = 0.1;

    __STATE_GAME_OVER = 0;
    __STATE_NEW_TURN  = 1;
    __STATE_END_TURN  = 2;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);
        ## iVars ##
        self.__speed_factor   = 1;
        self.__game_state     = None;
        self.__new_turn_timer = BasicClock(500, self.__on_new_turn_timer_tick);

        self.__movable_object_func = [
            self.__create_food,
            self.__create_bomb
        ];

        self.__score_font = pygame.font.Font(Fonts.SourcePro, 20);

        #GameField.
        self.__game_field = Sprite();
        self.__game_field.load_image(Sprites.Game_GameField);
        self.__game_field.set_position(8, 30);
        self.add(self.__game_field);

        #Taz lives.
        self.__taz_lives = [];
        for i in xrange(0, Taz.MAX_LIVES):
            live = Taz(None);
            live.set_position(36 * (i + 1), 338);
            self.add(live);
            self.__taz_lives.append(live);

        #Taz.
        self.__taz = Taz(self.__on_taz_death_animation_completed);
        self.add(self.__taz, layer=1);

        #Movable Objects.
        self.__movable_objects = [None] * GameFieldConstants.FIELD_TRACKS_LEN;

        #Score Sprite.
        self.__score_sprite = Sprite();
        self.add(self.__score_sprite);
        self.__update_score();

        self.__change_state_to_new_turn();


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def draw(self, surface):
        surface.fill(Constants.COLOR_BLACK);
        Scene.draw(self, surface);

    def update(self, dt):
        self.__new_turn_timer.update(dt);

        #Get the state of keyboard.
        keys = pygame.key.get_pressed();

        #Set the Taz Controls.
        self.__taz.set_controls(Taz.CONTROL_LEFT,  keys[pygame.locals.K_LEFT]);
        self.__taz.set_controls(Taz.CONTROL_RIGHT, keys[pygame.locals.K_RIGHT]);
        self.__taz.set_controls(Taz.CONTROL_DOWN,  keys[pygame.locals.K_DOWN]);
        self.__taz.set_controls(Taz.CONTROL_UP,    keys[pygame.locals.K_UP]);

        #Update the lives.
        for live in self.__taz_lives:
            live.update(dt);

        #Update the Taz and the MovableObjects.
        self.__taz.update(dt);

        #Only update the MovableObjects if Taz is alive.
        if(self.__taz.get_state() != Taz.STATE_ALIVE):
            return;

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

        if(key == pygame.locals.K_k):
            self.__taz.set_dead();


    ############################################################################
    ## Object Callbacks                                                       ##
    ############################################################################
    def __on_taz_death_animation_completed(self):
        #Check game over.
        if(self.__taz.get_lives() == 0):
            self.__change_state_to_game_over();
        else:
            self.__change_state_to_end_turn();

    def __on_bomb_collision(self, bomb):
        self.__taz.set_dead();

        #Remove the Taz live from Scene.
        live = self.__taz_lives.pop();
        self.remove(live);

    def __on_food_collision(self, food):
        #Increment the Taz eat count, update the score
        #and finally check if enough foods were ate to increment
        #the difficulty.
        self.__taz.increment_eat_count();
        self.__update_score();
        if(self.__taz.get_eat_count() in GameScene.__EAT_THRESHOLD):
            self.__speed_factor += GameScene.__SPEED_FACTOR_INCREMENT;


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def __on_new_turn_timer_tick(self):
        self.__new_turn_timer.stop();
        self.__change_state_to_new_turn();

    def __change_state_to_new_turn(self):
        for mobj in self.__movable_objects:
            self.__create_movable_object();

        self.__game_state = GameScene.__STATE_NEW_TURN;

    def __change_state_to_end_turn(self):
        for mobj in self.__movable_objects:
            self.__remove_movable_object(mobj);

        self.__game_state = GameScene.__STATE_END_TURN;
        self.__new_turn_timer.start();

    def __change_state_to_game_over(self):
        self.__game_state = GameScene.__STATE_GAME_OVER;
        self.__change_to_menu_scene();


    ############################################################################
    ## Movable Objects Management                                             ##
    ############################################################################
    def __create_movable_object(self):
        #Direction.
        direction = MovableObject.DIRECTION_RIGHT;
        if(random.randint(0, 1) % 2 == 0):
            direction = MovableObject.DIRECTION_LEFT;

        #Track Index.
        track_index = self.__get_empty_track_index();

        #Type
        type_index  = random.randint(0, 1);
        mobj = self.__movable_object_func[type_index](track_index, direction);

        self.add(mobj, layer=0);
        self.__movable_objects[track_index] = mobj;

    def __remove_movable_object(self, movable_object):
        if(movable_object is None): return;

        self.__movable_objects[movable_object.get_track_index()] = None;
        self.remove(movable_object);

    def __remove_and_create_movable_object(self, movable_object):
        self.__remove_movable_object(movable_object);
        self.__create_movable_object();


    ############################################################################
    ## Ohter Functions                                                        ##
    ############################################################################
    def __update_score(self):
        surface = self.__score_font.render(str(self.__taz.get_eat_count()),
                                     False,
                                     (187, 187, 53));

        self.__score_sprite.update_image(surface);
        self.__score_sprite.set_position(413, 342);

    def __get_empty_track_index(self):
        while(True):
            index = random.randint(0, GameFieldConstants.FIELD_TRACKS_LEN -1);
            if(self.__movable_objects[index] is None):
                return index;

    def __create_food(self, track_index, direction):
        return Food(track_index, direction,
                    self.__speed_factor,
                    self.__remove_and_create_movable_object,
                    self.__on_food_collision,
                    self.__remove_and_create_movable_object);

    def __create_bomb(self, track_index, direction):
        return Bomb(track_index, direction,
                    self.__speed_factor,
                    self.__remove_and_create_movable_object,
                    self.__on_bomb_collision);


    def __change_to_menu_scene(self):
        Director.instance().change_scene(menu_scene.MenuScene());
