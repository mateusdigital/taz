# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        sound.py                                  ##
##            █ █        █ █        Game_RamIt                                ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2016                        ##
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
################################################################################
## Imports                                                                    ##
################################################################################
## Pygame ##
import pygame;
## Game_RamIt ##
import assets;
from constants import *;


PRE_INIT_FREQUENCY = 22050;
PRE_INIT_SIZE      =   -16;
PRE_INIT_CHANNELS  =     1;
PRE_INIT_BUFFER    =  1024;

################################################################################
## Init                                                                       ##
################################################################################
def pre_init():
    pygame.mixer.pre_init(PRE_INIT_FREQUENCY,
                          PRE_INIT_SIZE,
                          PRE_INIT_CHANNELS,
                          PRE_INIT_BUFFER);

################################################################################
## Sounds                                                                     ##
################################################################################
def play_intro():
    pygame.mixer.Sound(assets.build_path("amazing_intro.wav")).play();

def play_eat():
    pygame.mixer.Sound(assets.build_path("eat.wav")).play();

def play_bomb():
    pygame.mixer.Sound(assets.build_path("bomb.wav")).play();
