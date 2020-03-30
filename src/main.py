#!/usr/bin/python
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : main.py                                                       ##
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
import sys;
## Game_RamIt ##
import assets;
import director;

################################################################################
## Script initialization                                                      ##
################################################################################
if __name__ == '__main__':
    try:
        if(len(sys.argv) > 1):
            assets.set_search_path(sys.argv[1]);

        director.init();
        director.run ();
        director.quit();

    except Exception as e:
        raise e;
        print(
            "Taz - Amazing Cow Labs - Sorry :(",
            "Failed to init game\n Reason: %s" %(str(e))
        );
