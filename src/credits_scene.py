##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : credits_scene.py                                              ##
##  Project   : Game_Taz                                                      ##
##  Date      : Sep 11, 2015                                                  ##
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
## Pygame ##
import pygame;
import pygame.locals;
## Game_RamIt ##
import assets;
import director;
import input;
from constants     import *;
from text          import *;
from color_surface import *;


class CreditsScene:
    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self):
        ##
        director.set_clear_color(COLOR_WHITE);

        ## Logo
        self.logo     = assets.load_image("AmazingCow_Logo_Small.png");
        logo_size     = self.logo.get_size();
        self.logo_pos = ((GAME_WIN_WIDTH * 0.5) - (logo_size[0] * 0.5), 15);

        color_surface(
            self.logo,
            director.randint(0, 255),
            director.randint(0, 255),
            director.randint(0, 255)
        );


        ## Message
        msg = [
            "This remake was made with <3 by Amazing Cow Labs.",
            "We hope that you enjoy this little game (!)"
            "",
            "We have other projects at:",
            "www.amazingcow.com",
            "",
            "This game is entirely FREE SOFTWARE",
            "This means that you're welcome to",
            "SHARE and HACK IT (!!!)",
            "",
            "You can find the sources at:",
            "opensource.amazingcow.com",
            "",
            "Dev / Graphics / Sound by N2OMatt",
            "",
            "THANKS FOR PLAYING...",
            "",
            "The CCV helps people not commit suicide.",
            "Their work is very, very important.",
            "Why don't you help them?",
            "www.cvv.org.br"
        ];

        self.texts   = [];
        start_offset = self.logo_pos[1] + logo_size[1] + 5;
        line_offset  =  16;

        for i in xrange(0, len(msg)):
            text = Text("SourceCodePro-Regular.ttf", line_offset,
                        -1, -1,
                        msg[i], COLOR_BLACK);
            text_size = text.get_size();

            text.set_position(
                (GAME_WIN_WIDTH * 0.5) - (text_size[0] * 0.5),
                start_offset + (i * line_offset)
            );

            self.texts.append(text);



    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        if(input.is_click(input.KEY_SELECTION, input.KEY_CANCEL)):
            director.go_to_menu();


    def draw(self, surface):
        surface.blit(self.logo, self.logo_pos);
        for text in self.texts:
            text.draw(surface, antialias = True);
