# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        splash_scene.py                           ##
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
import random;
## Pygame ##
import pygame;
## Game_RamIt ##
import assets;
import sound;
import director;
from constants     import *;
from cowclock      import *;
from color_surface import *;
from text          import *;


class SplashScene:
    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self):
        director.set_clear_color(COLOR_WHITE);

        ## Logo
        self._logo     = assets.load_image("AmazingCow_Logo_Big.png");
        logo_size      = self._logo.get_size();
        self._logo_pos = (GAME_WIN_CENTER_X - logo_size[0] * 0.5,
                          GAME_WIN_CENTER_Y - logo_size[1]); ## A bit above center

        ## Text
        self._text = Text(FONT_NAME, FONT_SIZE + 15,
                         -1, -1,  ## Dummy values.
                         "amazing cow labs", COLOR_BLACK);
        text_size = self._text.get_size();
        self._text.set_position(
            GAME_WIN_WIDTH  * 0.5 - text_size[0] * 0.5,
            self._logo_pos[1] + logo_size[1] + 20,
        );

        ## Timer
        self._timer = CowClock(0.4, 5, self._on_timer_tick, self._on_timer_done);
        self._timer.start();

        ## Others
        self._curr_rgb = list(COLOR_WHITE);
        self._dst_rgb  = (random.randint(0, 255),
                          random.randint(0, 255),
                          random.randint(0, 255));

        self._update_colors = False;


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        self._timer.update(dt);

        if(not self._update_colors):
            return;

        curr_r, curr_g, curr_b = self._curr_rgb;
        dst_r, dst_g, dst_b    = self._dst_rgb;
        step = 5;

        ## Red
        if  (curr_r > dst_r): curr_r -= step;
        elif(curr_r < dst_r): curr_r += step;
        ## Blue
        if  (curr_g > dst_g): curr_g -= step;
        elif(curr_g < dst_g): curr_g += step;
        ## Green
        if  (curr_b > dst_b): curr_b -= step;
        elif(curr_b < dst_b): curr_b += step;

        self._curr_rgb = curr_r, curr_b, curr_g;
        color_surface(self._logo, curr_r, curr_g, curr_b);


    def draw(self, surface):
        if(self._update_colors):
            surface.blit(self._logo, self._logo_pos);
            self._text.draw(surface);


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def _on_timer_tick(self):
        if(self._update_colors == False):
            sound.play_intro();
            self._update_colors = True;

    def _on_timer_done(self):
        director.go_to_menu();
