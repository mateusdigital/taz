#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        splash_scene.py                           ##
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
from scene      import Scene;
from scene      import Sprite;
from clock      import BasicClock;
from game       import Director;
from menu_scene import MenuScene;

class SplashScene(Scene):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);

        #Init the Sprite....
        self.sprite = Sprite();
        self.sprite.load_image("../resources/Sprite_AmazingCowLogo.png");
        self.sprite.set_position(100, 100);

        #Init the Timer..
        self.timer = BasicClock(50);
        self.timer.set_callback(self.on_timer_tick);
        self.timer.start();

        self.timer_ticks_to_sprite_disapear = 4;

    ############################################################################
    ## Time Callback                                                          ##
    ############################################################################
    def on_timer_tick(self):
        if(self.sprite not in self):
            self.add(self.sprite);
        else:
            self.timer_ticks_to_sprite_disapear -= 1;
            if(self.timer_ticks_to_sprite_disapear == 0):
                self.remove(self.sprite);
                self.timer.stop();
                self.change_scene();

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def update(self, dt):
        self.timer.update(dt);

    def draw(self, surface):
        Scene.draw(self,surface);

    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def change_scene(self):
        Director.instance().change_scene(MenuScene());
