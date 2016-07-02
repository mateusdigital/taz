# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        assets.py                                 ##
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
## Imports                                                                    ##
################################################################################
## Python ##
import os.path;
## Pygame ##
import pygame;


################################################################################
## Global vars                                                                ##
################################################################################
_paths              = ["./assets", "/usr/local/share/amazingcow_game_taz/assets"];
_assets_search_path = None;



################################################################################
## Init                                                                       ##
################################################################################
def pre_init():
    global _paths;
    global _assets_search_path;

    ## Was explicit set.
    if(_assets_search_path is not None):
        _paths.insert(0, _assets_search_path);

    for path in _paths:
        fullpath = os.path.abspath(os.path.expanduser(os.path.join(path)));
        if(os.path.isdir(fullpath)):
            _assets_search_path = fullpath;
            return;

    print "Error - Cannot find the assets folder, aborting...";
    exit(1);


################################################################################
## Search Path Functions                                                      ##
################################################################################
def set_search_path(path):
    global _assets_search_path;
    _assets_search_path = path;

def get_search_path():
    return _assets_search_path;

def build_path(filename):
    return os.path.join(get_search_path(), filename);


################################################################################
## Image Functions                                                            ##
################################################################################
def load_image_no_convert(name):
    return pygame.image.load(build_path(name));

def load_image(name):
    return load_image_no_convert(name).convert_alpha();


################################################################################
## Font Functions                                                             ##
################################################################################
def load_font(name, size):
    return pygame.font.Font(build_path(name), size);
