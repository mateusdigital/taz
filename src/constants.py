# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        constants.py                              ##
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

################################################################################
## FPS                                                                        ##
################################################################################
GAME_FPS       = 60.0;
GAME_FRAME_MS  = 1000.0 / GAME_FPS;
GAME_FRAME_SEC = 1.0    / GAME_FPS;


################################################################################
## Game Window                                                                ##
################################################################################
GAME_WIN_WIDTH    = 600;
GAME_WIN_HEIGHT   = int(GAME_WIN_WIDTH / 1.3333333);
GAME_WIN_CENTER_X = GAME_WIN_WIDTH  * 0.5;
GAME_WIN_CENTER_Y = GAME_WIN_HEIGHT * 0.5;
GAME_WIN_SIZE     = (GAME_WIN_WIDTH, GAME_WIN_HEIGHT);
GAME_WIN_CAPTION  = "Taz - v0.1 - AmazingCow";


################################################################################
## Playfield                                                                  ##
################################################################################
PLAYFIELD_WIDTH  = 256;
PLAYFIELD_HEIGHT = 157;
PLAYFIELD_SIZE   = (PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT);


################################################################################
## Fonts                                                                      ##
################################################################################
FONT_NAME = "nokiafc22.ttf";
FONT_MENU_SIZE      = 35;
FONT_MENU_LOGO_SIZE = 18;
FONT_SIZE = 20;

################################################################################
## Colors                                                                     ##
################################################################################
COLOR_BLACK = (0, 0, 0);
COLOR_WHITE = (255, 255, 255);
COLOR_BROWN = (155, 82, 15);
