##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : director.py                                                   ##
##  Project   : Game_Taz                                                      ##
##  Date      : Jun 30, 2016                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2016 - 2018                                      ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

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
     ## Setup the icon and caption.
    rawicon = assets.load_image_no_convert("icon.png");
    pygame.display.set_icon(rawicon);
    pygame.display.set_caption(STR_WIN_CAPTION, STR_WIN_CAPTION_SHORT);

    ## Init the Window.
    _Globals.surface = pygame.display.set_mode(GAME_WIN_SIZE);
    pygame.display.set_caption(STR_WIN_CAPTION);

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
