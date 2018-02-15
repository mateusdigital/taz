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
##  File      : install.sh                                                    ##
##  Project   : Game_Taz                                                      ##
##  Date      : Feb 15, 2018                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2018                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Vars                                                                       ##
##----------------------------------------------------------------------------##
INSTALL_PATH="/opt/amazingcowlabs_game_taz";


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
## Show Message.
cat << EOF
-- Game Taz Installer! --
Amazing Cow Labs - 2018 - www.amazingcow.com
Thank you for playing ;D

We gonna install the game on ($INSTALL_PATH).
A menu entry will be added on your desktop menu so to
play we can just click it or type "taz" on terminal.

Do you want to continue?[Y/n];
EOF

##------------------------------------------------------------------------------
## Get the answer.
read ANSWER;
ANSWER="${ANSWER:0:1}"; ## Only the first letter that we want.

##------------------------------------------------------------------------------
## Not install.
if [ "$ANSWER" == "n" ] || [ "$ANSWER" == "N" ]; then
    echo "Ok then... we don't install anything!"
    echo "To install run the script again ;D";
    exit;
fi;

##------------------------------------------------------------------------------
## Install ;D
mkdir -vp $INSTALL_PATH;

for ITEM in $(ls -1 .); do
    echo "Copying ($ITEM) -> ($INSTALL_PATH)";
    if [ -d "$ITEM" ]; then
        cp -r $ITEM $INSTALL_PATH;
    else
        cp $ITEM $INSTALL_PATH;
    fi;
done;

echo "";
echo "Done... Enjoy playing Taz.";