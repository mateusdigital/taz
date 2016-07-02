# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        menu_screen.py                            ##
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
## Python ##
import random;
## Pygame ##
import pygame;
import pygame.locals;
## Game_RamIt ##
import assets;
import director;
import input;
import sound;
from constants import *;
from text      import *;


class MenuScene:
    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self):
        director.set_clear_color(COLOR_WHITE);

        wcenter = (GAME_WIN_WIDTH * 0.5);

        ## Logo
        self._logo     = assets.load_image("Taz_Logo.png");
        logo_size      = self._logo.get_size();
        self._logo_pos = (wcenter - (logo_size[0] * 0.5), 20);

        ########################################################################
        ## COWTODO: WE REALLY NEED TO IMPROVE THE INTERFACE                   ##
        ## FOR CREATE AND SETUP TEXTS... IT SUCKS A LOT TODAY...              ##
        ########################################################################
        ## Play
        self._play_text = Text(FONT_NAME, FONT_MENU_SIZE,
                               -1, -1,
                               "Play", COLOR_BROWN);
        play_size = self._play_text.get_size();
        self._play_text.set_position(wcenter - (play_size[0] * 0.5), 300);

        ## Credits
        self._credits_text = Text(FONT_NAME, FONT_MENU_SIZE,
                                  -1, -1,
                                  "Credits", COLOR_BROWN);
        credits_size = self._credits_text.get_size();
        self._credits_text.set_position(wcenter - (credits_size[0] * 0.5), 360);

        ## AmazingCow
        self._amazingcow_text = Text(FONT_NAME, FONT_MENU_LOGO_SIZE,
                                     -1, -1, "amazingcow - 2016",
                                     COLOR_BROWN);
        amazing_size = self._amazingcow_text.get_size();
        self._amazingcow_text.set_position(wcenter - (amazing_size[0] * 0.5),
                                           GAME_WIN_HEIGHT - (amazing_size[1] + 10));

        ## Selection
        self._curr_selection = -1;
        self._update_selection(1, play_sound = False); ## Force the blinking on play...


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        self._play_text.update   (dt);
        self._credits_text.update(dt);

        if(input.is_click(pygame.locals.K_UP)):
            self._update_selection(-1);
        elif(input.is_click(pygame.locals.K_DOWN)):
            self._update_selection(+1);

        elif(input.is_click(pygame.locals.K_SPACE)):
            if(self._curr_selection == 0):
                director.go_to_game();
            else:
                director.go_to_credits();


    def draw(self, surface):
        ## Logo
        surface.blit(self._logo, self._logo_pos);
        ## Texts
        self._play_text.draw      (surface);
        self._credits_text.draw   (surface);
        self._amazingcow_text.draw(surface);


    ############################################################################
    ## Selection                                                              ##
    ############################################################################
    def _update_selection(self, delta, play_sound = True):
        new_selection = self._curr_selection + delta;

        if(new_selection < 0 or new_selection > 1):
            return;
        if(self._curr_selection == new_selection):
            return;

        if(play_sound):
            sound.play_eat();

        self._curr_selection = new_selection;
        self._play_text.set_blinking   (self._curr_selection == 0);
        self._credits_text.set_blinking(self._curr_selection == 1);
