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
from game      import Director;
from scene     import Scene;
from scene     import Sprite;
from clock     import BasicClock;
from resources import Sprites;

class MenuScene(Scene):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);

        #Init the Sprites....
        #Taz.
        self.taz_logo = Sprite();
        self.taz_logo.load_image(Sprites.TazLogo);
        self.taz_logo.set_position(216, 39);
        self.add(self.taz_logo);

        #Amazing Cow Url.
        self.cow_url = Sprite();
        self.cow_url.load_image(Sprites.AmazingCowUrl);
        self.cow_url.set_position(225, 397);
        self.add(self.cow_url);

        #Menu Options.
        self.menu_options  = [];
        self.current_index = 0;
        #Play.
        self.play_option = Sprite();
        self.play_option.load_image(Sprites.MenuPlay);
        self.play_option.set_position(217, 333);
        #Credits.
        self.credits_option = Sprite();
        self.credits_option.load_image(Sprites.MenuCredits);
        self.credits_option.set_position(217, 333);

        self.menu_options.append(self.play_option);
        self.menu_options.append(self.credits_option);

        self.change_menu_option();


    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def draw(self, surface):
        Scene.draw(self,surface);

    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type != pygame.locals.KEYDOWN):
            return;

        key = event.key;
        #Up and Down change the option.
        if(key == pygame.locals.K_UP or key == pygame.locals.K_DOWN):
            self.change_menu_option();
        #Enter commit the selection.
        elif(key == pygame.locals.K_RETURN):
            self.change_scene();


    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def change_menu_option(self):
        self.remove(self.menu_options[self.current_index]);
        self.current_index = (self.current_index + 1) % 2;
        self.add(self.menu_options[self.current_index]);

    def change_scene(self):
        print "Change_scee", self.current_index;
