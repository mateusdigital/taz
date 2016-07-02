# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        hud.py                                    ##
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
## Pygame ##
import pygame;
## Game_RamIt ##
from constants import *;
from text      import *;
from taz       import *;


class Hud:
    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self, min_bounds, max_bounds):
        ## Score Text
        self._score_text = Text(FONT_NAME, FONT_SIZE, -1, -1);
        self.set_score(0);

        score_size = self._score_text.get_size();
        score_pos  = [min_bounds[0], GAME_WIN_HEIGHT - score_size[1] - 25];
        self._score_text.set_position(score_pos[0], score_pos[1]);


        ## Lives
        self._current_lives = Taz.MAX_LIVES;
        self._lives = [];
        for i in xrange(0, Taz.MAX_LIVES):
            taz = Taz(
                    min_bounds   = [0,0], #Dummy values...
                    max_bounds   = [0,0], #Dummy values...
                    tracks_count = 0,     #Dummy values...
                    track_offset = 0,     #Dummy values...
                    is_playable  = False
                  );

            #COWTODO: Center the taz into the score text y.
            taz_size = taz.get_size();
            taz.set_position(
                max_bounds[0] - ((10 + taz_size[0]) * i),
                score_pos [1]
            );
            self._lives.append(taz);


    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def set_score(self, score):
        self._score_text.set_contents("Score: %05d" %(score));

    def add_live(self):
        self._lives[self._current_lives].set_state(Taz.STATE_ALIVE);
        self._current_lives += 1;

    def remove_live(self):
        self._current_lives -= 1;
        self._lives[self._current_lives].set_state(Taz.STATE_DEAD);


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        for taz in self._lives:
            taz.update(dt);

    def draw(self, surface):
        self._score_text.draw(surface);

        for taz in self._lives:
            taz.draw(surface);



