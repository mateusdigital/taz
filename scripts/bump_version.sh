#!/usr/bin/env bash
##~---------------------------------------------------------------------------##
##                        _      _                 _   _                      ##
##                    ___| |_ __| |_ __ ___   __ _| |_| |_                    ##
##                   / __| __/ _` | '_ ` _ \ / _` | __| __|                   ##
##                   \__ \ || (_| | | | | | | (_| | |_| |_                    ##
##                   |___/\__\__,_|_| |_| |_|\__,_|\__|\__|                   ##
##                                                                            ##
##  File      : bump_version.sh                                               ##
##  Project   : taz                                                           ##
##  Date      : Mar 30, 2020                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : stdmatt <stdmatt@pixelwizards.io>                             ##
##  Copyright : stdmatt 2020                                                  ##
##                                                                            ##
##  Description :                                                             ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
source /usr/local/src/stdmatt/shellscript_utils/main.sh


##----------------------------------------------------------------------------##
## Variables                                                                  ##
##----------------------------------------------------------------------------##
## Dirs
SCRIPT_DIR="$(pw_get_script_dir)";
PROJECT_ROOT=$(pw_abspath "$SCRIPT_DIR/..");
SRC_FILE="${PROJECT_ROOT}/src/constants.py"


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
BUMP_THE_VERSION="$(pw_get_program_path "bump-the-version")";
if [ -z "$BUMP_THE_VERSION" ]; then
    pw_log_fatal "Coundn't find (bump-the-version) program - Aborting...";
fi;

"${BUMP_THE_VERSION}" "${SRC_FILE}" "GAME_VERSION =" bump "$1";
