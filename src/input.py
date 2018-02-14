# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        input.py                                  ##
##            █ █        █ █        Game_Taz                                  ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

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
