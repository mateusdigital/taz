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

################################################################################
## Imports                                                                    ##
################################################################################
## Python ##
import random;
## Pygame ##
import pygame;
import pygame.locals;
## Game_Taz ##
import sound;
import assets;
from constants     import *;
from splash_scene  import *;
from menu_scene    import *;
from credits_scene import *;
from game_scene    import *;

class _Globals:
    surface       = None;
    clear_color   = COLOR_WHITE;
    current_scene = None
    running       = False;


################################################################################
## Init / Run / Clean                                                         ##
################################################################################
def init():
    ## Pre inits
    sound.pre_init ();
    assets.pre_init();

    pygame.init();

    ## Init the Window.
    _Globals.surface = pygame.display.set_mode(GAME_WIN_SIZE);
    pygame.display.set_caption(GAME_WIN_CAPTION);

    ## Init Input
    input.init();

    ## Change the scene.
    go_to_splash();

    _Globals.running = True;


def run():
    frame_start = pygame.time.get_ticks();
    frame_time  = 0;

    while(_Globals.running):
        frame_start = pygame.time.get_ticks();

        ## Handle window events...
        for event in pygame.event.get():
            if(event.type == pygame.locals.QUIT):
                _Globals.running = False;


        ## Updates
        input.update();
        _update(GAME_FRAME_SEC);

        ## Keep the framerate tidy...
        frame_time = (pygame.time.get_ticks() - frame_start);
        if(frame_time < GAME_FRAME_MS):
            while(1):
                frame_time = (pygame.time.get_ticks() - frame_start);
                if(frame_time >= GAME_FRAME_MS):
                    break;
        else:
            print "MISS FRAME";

        ## Game Draw
        _draw();


def quit():
    pygame.quit();



################################################################################
## Utilities                                                                  ##
################################################################################
def get_draw_surface():
    return _Globals.surface;

def set_clear_color(color):
    _Globals.clear_color = color;


def randint(min, max):
    return random.randint(min, max);

def randbool():
    return bool(random.getrandbits(1));

def randfloat(min, max):
    return random.uniform(min, max);


################################################################################
## Scene Management                                                           ##
################################################################################
def go_to_splash():
    _Globals.current_scene = SplashScene();
def go_to_menu():
    _Globals.current_scene = MenuScene();
def go_to_credits():
    _Globals.current_scene = CreditsScene();
def go_to_game():
    _Globals.current_scene = GameScene();



################################################################################
## Update / Draw / Handle Events                                              ##
################################################################################
def _update(dt):
    _Globals.current_scene.update(dt);


def _draw():
    _Globals.surface.fill(_Globals.clear_color);   #Clear.
    _Globals.current_scene.draw(_Globals.surface); #Blit.
    pygame.display.update();                       #Present.


def _handle_events():
    for event in pygame.event.get():
        #If user wants to quit, just quit.
        if(event.type == pygame.locals.QUIT):
            _Globals.running = False;
            return;
