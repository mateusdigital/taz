#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        game.py                                   ##
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
import os;
import os.path;
import sys;
import getopt;
#Pygame
import pygame;
import pygame.locals;
#Project
import scene;

################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    pass;

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    GAME_FPS = 60;
    SCREEN_SIZE = (600, 480);
    WINDOW_CAPTION = "Taz - v0.1 - AmazingCow";

################################################################################
## Game                                                                       ##
################################################################################
class Game(object):
    def __init__(self):
        self.__surface       = None;
        self.__clock         = None;
        self.__current_scene = None

        self.__running = False;

    ## Public Methods ##
    def init(self):
        pygame.init();

        #Init the Window. 
        self.__surface = pygame.display.set_mode(Constants.SCREEN_SIZE);
        pygame.display.set_caption(Constants.WINDOW_CAPTION);
        
        #Init the Game clock.
        self.__clock = pygame.time.Clock();

        self.__current_scene = scene.SplashScene();

    def run(self):
        self.__running = True;
        
        while(self.__running):
            dt = self.__clock.tick(Constants.GAME_FPS);

            self.__handle_events();
            self.__update(dt);
            self.__draw();

    def clean(self):
        pygame.quit();

    ## Private Methods ##
    def __handle_events(self):
        for event in pygame.event.get():
            #If user wants to quit, just quit.
            if(event.type == pygame.locals.QUIT):
                self.__running = False;
                return;
            #Pass the event to scene handler.
            self.__current_scene.handle_events(event);

    def __update(self, dt):
        self.__current_scene.update(dt);

    def __draw(self):
        self.__surface.fill((0,0,0));
        self.__current_scene.draw(self.__surface);
        pygame.display.update()

################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    game = Game();
    
    game.init();
    game.run();
    game.clean();

    exit(0);

if __name__ == '__main__':
    main();
