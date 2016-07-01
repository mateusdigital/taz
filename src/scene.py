#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        scene.py                                  ##
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
#COWTODO: Download the music :~) #bass4 the hacker

################################################################################
## Scene                                                                      ##
################################################################################
# class Scene(pygame.sprite.Group):
# class Scene(pygame.sprite.OrderedUpdates):
class Scene(pygame.sprite.LayeredUpdates):
    def __init__(self):
        # pygame.sprite.OrderedUpdates.__init__(self);
        # pygame.sprite.Group.__init__(self);
        pygame.sprite.LayeredUpdates.__init__(self);
    def handle_events(self, event):
        pass;

################################################################################
## Sprite                                                                     ##
################################################################################
class Sprite(pygame.sprite.Sprite):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, surface = None):
        pygame.sprite.Sprite.__init__(self);
        self.rect = pygame.rect.Rect(0,0,0,0);
        if(surface is not None):
            self.update_image(surface);

    ############################################################################
    ## Image Methods                                                          ##
    ############################################################################
    def load_image(self, filename):
        surface = pygame.image.load(filename);
        self.update_image(surface);

    def update_image(self, surface):
        self.image   = surface;
        self.rect[2] = self.image.get_width();
        self.rect[3] = self.image.get_height();

    ############################################################################
    ## Positions Setter/Getters                                               ##
    ############################################################################
    def set_position(self, x, y):
        self.rect[0] = x;
        self.rect[1] = y;
    def set_position_x(self, x):
        self.rect[0] = x;
    def set_position_y(self, y):
        self.rect[1] = y;

    def get_position(self):
        return self.rect[0], self.rect[1];
    def get_position_x(self):
        return self.rect[0];
    def get_position_y(self):
        return self.rect[1];

    ############################################################################
    ## Size Setter/Getters                                                    ##
    ############################################################################
    def get_size(self):
        return self.rect[2], self.rect[3];
    def get_size_w(self):
        return self.rect[2];
    def get_size_h(self):
        return self.rect[3];

    ############################################################################
    ## Movement Functions                                                     ##
    ############################################################################
    def move(self, x, y):
        self.rect.move_ip(x, y);
    def move_x(self, x):
        self.move(x, 0);
    def move_y(self, y):
        self.move(0, y);
