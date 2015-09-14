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
import random;
#Pygame
import pygame;
#Project
from game       import Director;
from scene      import Scene;
from scene      import Sprite;
from clock      import BasicClock;
from resources  import Sprites;
import menu_scene; #To avoid circular imports;

import pdb; # :~)

################################################################################
## MovableObject                                                              ##
################################################################################
class MovableObject(Sprite):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    DIRECTION_LEFT   = -1;
    DIRECTION_RIGHT  = +1;
    HORIZONTAL_SPEED = 200;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction,
                speed_factor, out_of_field_callback):

        Sprite.__init__(self);

        ## iVars ##
        self.__track_index           = track_index;
        self.__direction             = direction;
        self.__speed_factor          = speed_factor;
        self.__target_position_x     = 0;
        self.__out_of_field_callback = out_of_field_callback;


        #Set the position.
        y = GameScene.FIELD_TRACKS_Y[track_index];
        x = GameScene.FIELD_HARD_LEFT;
        if(direction == MovableObject.DIRECTION_LEFT):
            x = GameScene.FIELD_HARD_RIGHT;

        self.set_position(x, y);

        #Set target position.
        self.__target_position_x = GameScene.FIELD_HARD_RIGHT;
        if(direction == MovableObject.DIRECTION_LEFT):
            self.__target_position_x = GameScene.FIELD_HARD_LEFT;

    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def get_track_index(self):
        return self.__track_index;

    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        pos_x  = self.get_position_x();
        size_w = self.get_size_w();

        #Moving to right.
        if(self.__direction == MovableObject.DIRECTION_RIGHT):
            if(pos_x > self.__target_position_x):
                self.__out_of_field_callback(self);
        #Moving to left.
        elif(self.__direction == MovableObject.DIRECTION_LEFT):
            if(pos_x + size_w < self.__target_position_x):
                self.__out_of_field_callback(self);

        speed = MovableObject.HORIZONTAL_SPEED * self.__direction * self.__speed_factor;
        self.move_x(speed * (dt / 1000.0));


################################################################################
## Food                                                                       ##
################################################################################
class Food(MovableObject):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, track_index, direction,
                 speed_factor, out_of_field_callback, eat_callback):

        #Call baseclass CTOR.
        MovableObject.__init__(self, track_index,
                               direction, speed_factor, out_of_field_callback);

        ## iVars ##
        self.__eat_callback = eat_callback;

        #Load the Sprites.
        self.load_image(Sprites.Food);

    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        # print self.get_position_x();
        MovableObject.update(self, dt);



################################################################################
## Taz                                                                        ##
################################################################################
class Taz(Sprite):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    INITIAL_TRACK_INDEX  = 3;
    INITIAL_POSITION_X   = 200;

    SCALE_FACTOR     = 1.5;
    HORIZONTAL_SPEED = 500;

    TIME_TO_CHANGE_TRACK     = 40;
    TIME_TO_NORMAL_ANIMATION = 150;
    TIME_TO_DEATH_ANIMATION  = 1400;

    STATE_ALIVE = 0;
    STATE_DEAD  = 1;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Sprite.__init__(self);

        self.__state = Taz.STATE_ALIVE;

        #Set the Sprite vars.
        self.__frames = [pygame.image.load(Sprites.TazFrame0),
                         pygame.image.load(Sprites.TazFrame1)];
        self.__current_frame = 0;
        self.update_image(self.__frames[0]);

        #Set the Track vars.
        self.__current_track    = Taz.INITIAL_TRACK_INDEX;
        self.__can_change_track = True;

        #Set the Animation vars.
        self.__sprite_is_flipped = False;

        #Set the Initial Position.
        x = Taz.INITIAL_POSITION_X;
        y = GameScene.FIELD_TRACKS_Y[self.__current_track];
        self.set_position(x, y);

        #Initialize the Track Change timer.
        self.__change_track_timer = BasicClock(Taz.TIME_TO_CHANGE_TRACK);
        self.__change_track_timer.set_callback(self.on_change_track_timer_tick);

        #Initialize the Normal Animation timer.
        self.__normal_animation_timer = BasicClock(Taz.TIME_TO_NORMAL_ANIMATION);
        self.__normal_animation_timer.set_callback(self.on_normal_animation_timer_tick);

        #Initialize the Death Animation Timer.
        self.__death_timer = BasicClock(Taz.TIME_TO_DEATH_ANIMATION);
        self.__death_timer.set_callback(self.on_death_timer_tick);

        #Start the Normal animation timer.
        self.__normal_animation_timer.start();

    ############################################################################
    ## Time Callbacks                                                         ##
    ############################################################################
    def on_change_track_timer_tick(self):
        self.__can_change_track = True;
        self.__change_track_timer.stop();

    def on_normal_animation_timer_tick(self):
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

    def on_death_timer_tick(self):
        self.change_state_to_alive();

    ############################################################################
    ## Movement Functions                                                     ##
    ############################################################################
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
        #Move.
        speed = Taz.HORIZONTAL_SPEED * dir;
        self.move_x(speed * (dt / 1000.0));

        #Constraint to field bounds...
        x = self.get_position_x();
        if(x <= GameScene.FIELD_SOFT_LEFT):
            x = GameScene.FIELD_SOFT_LEFT;
        elif(x + self.get_size_w() >= GameScene.FIELD_SOFT_RIGHT):
            x = GameScene.FIELD_SOFT_RIGHT - self.get_size_w();
        self.set_position_x(x);

    ############################################################################
    ## State Functions                                                        ##
    ############################################################################
    def change_state_to_alive(self):
        print "Taz - Change State to Alive...";
        self.__death_timer.stop();
        self.__state = Taz.STATE_ALIVE;

    def change_state_to_dead(self):
        print "Taz - Change State to Dead...";
        self.__death_timer.start();
        self.__state = Taz.STATE_DEAD;

    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        #Get the state of keyboard.
        keys = pygame.key.get_pressed();

        #Update the timers...
        self.__change_track_timer.update(dt);
        self.__normal_animation_timer.update(dt);
        self.__death_timer.update(dt);

        if(keys[pygame.locals.K_j]):
            self.change_state_to_dead();

        #If dead do not move.
        if(self.__state == Taz.STATE_DEAD):
            return;

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
    FIELD_TRACKS_Y   = [62, 94, 126, 158, 190, 222, 254, 285]; #The field tracks.
    FIELD_HARD_LEFT  = -22; #Right most positions when other stuff can go.
    FIELD_HARD_RIGHT = 500; #Left  most positions when other stuff can go.
    FIELD_SOFT_LEFT  = 33;   #Left  most position that Taz can go.
    FIELD_SOFT_RIGHT = 440;  #Right most position that Taz can go.

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);

        ## iVars ##
        self.__speed_factor = 1;
        self.__track_fill   = [False]  * len(GameScene.FIELD_TRACKS_Y);

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

        #Bombs/Foods
        self.moveable_objects = [];
        for i in xrange(0, len(GameScene.FIELD_TRACKS_Y)):
            self.create_movable_object();

    def create_movable_object(self):
        #Direction.
        direction = MovableObject.DIRECTION_RIGHT;
        if(random.randint(0, 1) % 2 == 0):
            direction = MovableObject.DIRECTION_LEFT;

        #Track Index.
        track_index = -1;
        while(True):
            index = random.randint(0, len(GameScene.FIELD_TRACKS_Y) -1);
            if(self.__track_fill[index] == False):
                track_index = index;
                break;

        type_index  = random.randint(0, 1);

        mobject = Food(track_index,
                       direction,
                       self.__speed_factor,
                       self.on_movable_object_out_of_field,
                       None);
        self.add(mobject);
        self.__track_fill[track_index] = True;

    def on_movable_object_out_of_field(self, movable_object):
        self.__track_fill[movable_object.get_track_index()] = False;

        self.remove(movable_object);
        self.create_movable_object();

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def draw(self, surface):
        surface.fill((0,0,0));
        Scene.draw(self, surface);

    # def update(self, dt):
    #     self.taz.update(dt);

    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type != pygame.locals.KEYDOWN):
            return;

        key = event.key;
        #Up and Down change the option.
        if(key == pygame.locals.K_ESCAPE):
            # exit(0);
            self.change_to_menu_scene();


    def change_to_menu_scene(self):
        Director.instance().change_scene(menu_scene.MenuScene());
