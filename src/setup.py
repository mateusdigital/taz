##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : setup.py                                                      ##
##  Project   : Game_Taz                                                      ##
##  Date      : Feb 14, 2018                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2018                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
import sys;
import cx_Freeze;


##----------------------------------------------------------------------------##
## Vars                                                                       ##
##----------------------------------------------------------------------------##
options_packages      = ["pygame", "numpy"];
options_include_files = ["../assets"];
options_excludes      =  ["tkinter", "tcl", "tk"];

executables = [
    cx_Freeze.Executable(
        script = "main.py",
        icon   = "../assets/icon.ico",
        base   =  "Win32GUI" if sys.platform == "win32" else None
    )
];


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
cx_Freeze.setup(
    name    = "Taz - Amazing Cow Labs",
    options = {
        "build_exe" : {
            "packages"      : options_packages,
            "excludes"      : options_excludes,
            "include_files" : options_include_files
        }
    },
    executables = executables
);
