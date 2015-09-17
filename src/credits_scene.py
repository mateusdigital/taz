#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        credits_scene.py                          ##
##             ████████████         Game Taz                                  ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
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
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##
## Imports ##
#Pygame
import pygame;
#Project
from game       import Director;
from game       import Constants;
from scene      import Scene;
from scene      import Sprite;
from clock      import BasicClock;
from resources  import Fonts;

import menu_scene; # To avoid circular imports;

class CreditsScene(Scene):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);
        self.__create_text(True, 16);

    def __create_text(self, alias, font_size):
        text = ["This remake was made with <3 by Amazing Cow.",
                "We hope that you enjoy this little game (!)",
                "",
                "We have other projects at:",
                "www.amazingcow.com",
                "Take a look :)",
                "",
                "This game is entirely FREE SOFTWARE",
                "This means that you're welcome to",
                "SHARE and HACK IT (!!!)",
                "",
                "You can found the sources at:",
                "opensource.amazingcow.com/game_taz",
                "",
                "Dev and Graphics by N2OMatt",
                "","",
                "THANKS FOR PLAYING..."
                "","","",
                "--- CHECK OUT THE README FILE ---"];


        font = pygame.font.Font(Fonts.SourcePro, font_size);

        initial_y           = 0;
        middle_screen_x     = Constants.SCREEN_SIZE[0] / 2;
        font_line_size      = font.get_linesize();
        half_font_line_size = font_line_size / 2;
        offset              = initial_y;
        normal_color        = Constants.COLOR_BLACK;
        antialias           = alias;

        for i in xrange(0, len(text)):
            line = text[i];

            if(line == ""): offset += half_font_line_size;
            else:           offset += font_line_size;

            normal_surface = font.render(line, antialias, normal_color);

            x = middle_screen_x - normal_surface.get_width() / 2;
            y = offset;

            normal_sprite = Sprite(normal_surface);
            normal_sprite.set_position(x, y);
            self.add(normal_sprite);

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def handle_events(self, event):
        #We're only interested in keydown events.
        if(event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            Director.instance().change_scene(menu_scene.MenuScene());
