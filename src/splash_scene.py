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
from clock      import BasicClock;
from game       import Director;
from menu_scene import MenuScene;
from resources  import Sprites;
from scene      import Scene;
from scene      import Sprite;

class SplashScene(Scene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __TIMER_TIME              = 500;
    __TICKS_TO_LOGO_DISAPPEAR = 4;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Scene.__init__(self);

        #Init the Sprite....
        self.__sprite = Sprite();
        self.__sprite.load_image(Sprites.Splash_AmazingCowLogo);
        self.__sprite.set_position(133, 81);

        #Init the Timer..
        self.__timer = BasicClock(SplashScene.__TIMER_TIME);
        self.__timer.set_callback(self.__on_timer_tick);
        self.__timer.start();

        self.__timer_ticks_to_sprite_disapear = SplashScene.__TICKS_TO_LOGO_DISAPPEAR;

    ############################################################################
    ## Time Callback                                                          ##
    ############################################################################
    def __on_timer_tick(self):
        if(self.__sprite not in self):
            self.add(self.__sprite);
        else:
            self.__timer_ticks_to_sprite_disapear -= 1;
            if(self.__timer_ticks_to_sprite_disapear == 0):
                self.remove(self.__sprite);
                self.__timer.stop();
                self.__change_scene();

    ############################################################################
    ## Update/Draw/Handle Events                                              ##
    ############################################################################
    def update(self, dt):
        self.__timer.update(dt);

    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def __change_scene(self):
        Director.instance().change_scene(MenuScene());
