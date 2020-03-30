##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        Makefile                                  ##
##            █ █        █ █        Game_Taz                                  ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2016                        ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

##COWTODO: We hard code the paths in assets.py      \
##         While this matches the paths in Makefile \
##         it's fragile and we must change to       \
##         a more robust approach soon as possible.

################################################################################
## Public Vars                                                                ##
################################################################################
HOST=`uname -s`_`uname -m`


################################################################################
## Private Vars                                                               ##
################################################################################
_GAME_SAFE_NAME=taz
_GAME_NAME=taz
_DESKTOP_FILENAME=$(_GAME_SAFE_NAME).desktop

_INSTALL_DIR_BIN=/usr/local/bin
_INSTALL_DIR_SHARE=/usr/local/share/amazingcow_game_$(_GAME_SAFE_NAME)
_INSTALL_DIR_DESKTOP=/usr/share/applications

_PROJECT_DIR=./project
_PROJECT_DIR_BIN=$(_PROJECT_DIR)/bin
_PROJECT_DIR_OBJ=$(_PROJECT_DIR)/obj


_GIT_TAG=`git describe --tags --abbrev=0 | tr . _`
_CC=g++ -Ofast
_XBUILD=xbuild /p:Configuration=Release

SILENT=@

all: dev-build

################################################################################
## End user                                                                   ##
################################################################################
install:
	$(SILENT) echo "---> Installing..."

	$(SILENT) ## Deleting old stuff...
	$(SILENT) rm -rf $(_INSTALL_DIR_SHARE)
	$(SILENT) rm -rf $(_INSTALL_DIR_BIN)/$(_GAME_NAME)
	$(SILENT) rm -rf $(_INSTALL_DIR_DESKTOP/$(_DESKTOP_FILENAME)

	$(SILENT) ## Create the dir if it doesn't exists...
	$(SILENT) mkdir -p $(_INSTALL_DIR_SHARE)

	$(SILENT) ## Copy the files to the share
	$(SILENT) cp -rf ./build/* $(_INSTALL_DIR_SHARE)

	$(SILENT) ## Link the bootstrap (Notice that is symbolic link)
	$(SILENT) ## and make it executable.
	$(SILENT) ln -fs $(_INSTALL_DIR_SHARE)/main.py $(_INSTALL_DIR_BIN)/$(_GAME_NAME)
	$(SILENT) chmod 755 $(_INSTALL_DIR_BIN)/$(_GAME_NAME)

	$(SILENT) ## Copy the desktop entry.
	$(SILENT) cp -f $(_DESKTOP_FILENAME) $(_INSTALL_DIR_DESKTOP)


	$(SILENT) echo "---> Done... We **really** hope that you have fun :D"


################################################################################
## Release                                                                    ##
################################################################################
gen-binary:
	rm -rf build     \
	       dist      \
	       bin       \
	       $(_GAME_SAFE_NAME).spec

	pyinstaller -F --windowed   \
	            --name=$(_GAME_SAFE_NAME) \
	            ./src/main.py

	mkdir -p ./bin/game_$(_GAME_SAFE_NAME)
	cp -r ./assets/      			 ./bin/game_$(_GAME_SAFE_NAME)/assets
	cp    ./dist/$(_GAME_SAFE_NAME)  ./bin/game_$(_GAME_SAFE_NAME)/$(_GAME_SAFE_NAME)
	cp AUTHORS.txt   \
	   CHANGELOG.txt \
	   COPYING.txt   \
	   README.md     \
	   TODO.txt      \

	   ./bin/game_$(_GAME_SAFE_NAME)

	cd ./bin && zip -r ./$(HOST)_$(_GIT_TAG).zip ./game_$(_GAME_SAFE_NAME)
	rm -rf ./bin/game_$(_GAME_SAFE_NAME)


gen-archive:
	mkdir -p ./archives

	git archive --output ./archives/source_game_$(_GAME_SAFE_NAME)_$(_GIT_TAG).zip    master
	git archive --output ./archives/source_game_$(_GAME_SAFE_NAME)_$(_GIT_TAG).tar.gz master


################################################################################
## Dev                                                                        ##
################################################################################
dev-build:
	rm -rf ./build
	mkdir -p ./build

	cp -rf ./src/*.py ./build
	cp -rf ./assets   ./build


################################################################################
## Clean                                                                      ##
################################################################################
clean:
	## Archives
	rm -rf archives

	## Bin
	rm -rf bin
	rm -rf dist
	rm -f $(_GAME_SAFE_NAME).spec

	## Build
	rm -rf build
