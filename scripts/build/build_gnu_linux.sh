#!/usr/bin/env sh
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : build_gnu_linux.sh                                            ##
##  Project   : Cosmic Intruders                                              ##
##  Date      : Feb 12, 2018                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2017                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##


##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
source /usr/local/src/acow_shellscript_utils.sh

##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
echo $(center_text "GNU/Linux Build");
SRC_DIR=$(realpath $(get_script_dir)/../../src);

##------------------------------------------------------------------------------
## setup.py needs to run on the src dir.
echo "Changing to source directory..."
cd "$SRC_DIR";
echo "CWD: ($PWD)";

echo "Running the setup.py...";
python setup.py build
echo $(center_text);
