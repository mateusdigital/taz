##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : menu_scene.py                                                 ##
##  Project   : Game_Taz                                                      ##
##  Date      : Sep 07, 2015                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2015 - 2018                                      ##
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

        ##----------------------------------------------------------------------
        ## Movement.
        if  (input.is_click(input.KEY_MOVEMENT_UP  )): self._update_selection(-1);
        elif(input.is_click(input.KEY_MOVEMENT_DOWN)): self._update_selection(+1);

        ##----------------------------------------------------------------------
        ## Selection.
        elif(input.is_click(input.KEY_SELECTION)):
            if(self._curr_selection == 0): director.go_to_game   ();
            else:                          director.go_to_credits();


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
