##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : input.py                                                      ##
##  Project   : Game_Taz                                                      ##
##  Date      : Jun 30, 2016                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2016 - 2018                                      ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
## Pygame ##
import pygame;


##----------------------------------------------------------------------------##
## Constants                                                                  ##
##----------------------------------------------------------------------------##
KEY_SELECTION = (
    pygame.locals.K_RETURN,
    pygame.locals.K_SPACE
);

KEY_CANCEL = (
    pygame.locals.K_ESCAPE
);

KEY_MOVEMENT_UP = (
    pygame.locals.K_UP,
    pygame.locals.K_w,
);

KEY_MOVEMENT_DOWN = (
    pygame.locals.K_DOWN,
    pygame.locals.K_s,
);

KEY_MOVEMENT_LEFT = (
    pygame.locals.K_LEFT,
    pygame.locals.K_a,
);

KEY_MOVEMENT_RIGHT = (
    pygame.locals.K_RIGHT,
    pygame.locals.K_d,
);

KEY_PAUSE = (
    pygame.locals.K_p,
);




##----------------------------------------------------------------------------##
## Global vars                                                                ##
##----------------------------------------------------------------------------##
_prev_keys = None;
_curr_keys = None;


##----------------------------------------------------------------------------##
## Init                                                                       ##
##----------------------------------------------------------------------------##
def init():
    global _prev_keys;
    global _curr_keys;

    _prev_keys = pygame.key.get_pressed();
    _curr_keys = pygame.key.get_pressed();


##----------------------------------------------------------------------------##
## Update                                                                     ##
##----------------------------------------------------------------------------##
def update():
    global _prev_keys;
    global _curr_keys;

    _prev_keys = _curr_keys;
    _curr_keys = pygame.key.get_pressed();

def get_state_value(keys_states, keys):
    for k in keys:
        if(isinstance(k, tuple)):
            if(get_state_value(keys_states, k)):
                return True;
        elif(keys_states[k]):
            return True;

    return False;

##----------------------------------------------------------------------------##
## Key Methods                                                                ##
##----------------------------------------------------------------------------##
def is_down(*keys):
    if(get_state_value(_curr_keys, keys)):
        return True;

    return False;

def was_up(*keys):
    if(not is_down(*keys)):                return False;
    if(get_state_value(_prev_keys, keys)): return False;

    return True;

def is_click(*keys):
    return is_down(*keys) and was_up(*keys);
