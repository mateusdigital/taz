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
import menu_scene;

class GameScene(Scene):
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


        #.
        self.food = Sprite();
        self.food.load_image(Sprites.Food);
        self.food.set_position(9, 345);
        self.add(self.food);

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def draw(self, surface):
        surface.fill((0,0,0));
        Scene.draw(self,surface);

    def update(self, dt):
        keys = pygame.key.get_pressed();

        speed = [0,0];
        if(keys[pygame.locals.K_UP]):
            speed[1] -= 10;
        if(keys[pygame.locals.K_DOWN]):
            speed[1] += 10;
        if(keys[pygame.locals.K_LEFT]):
            speed[0] -= 10;
        if(keys[pygame.locals.K_RIGHT]):
            speed[0] += 10;

        speed *= dt;

        self.food.move(speed[0], speed[1]);

    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type != pygame.locals.KEYDOWN):
            return;

        key = event.key;
        #Up and Down change the option.
        if(key == pygame.locals.K_ESCAPE):
            self.change_to_menu_scene();

        # key = event.key;
        # #Up and Down change the option.
        # if(key == pygame.locals.K_UP or key == pygame.locals.K_DOWN):
        #     self.change_menu_option();
        # #Enter commit the selection.
        # elif(key == pygame.locals.K_RETURN):
        #     self.change_scene();


    def change_to_menu_scene(self):
        Director.instance().change_scene(menu_scene.MenuScene());
