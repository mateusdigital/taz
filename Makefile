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

################################################################################
## Vars                                                                       ##
################################################################################
HOST="linux_x64"


################################################################################
## Private Vars                                                               ##
################################################################################
_GAME_NAME=taz

_COW_BIN=/usr/local/bin
_COW_SHARE=/usr/local/share/amazingcow_game_taz
_GIT_TAG=`git describe --tags --abbrev=0 | tr . _`


################################################################################
## End user                                                                   ##
################################################################################
install:
	@ echo "---> Installing...".

	@ ## Deleting old stuff...
	@ rm -rf $(_COW_SHARE)
	@ rm -rf $(_COW_BIN)/$(_GAME_NAME)

	@ ## Install new stuff...
	@ ## Source
	@ cp -rf ./src/ $(_COW_SHARE)
	@ ln -s $(_COW_SHARE)/main.py  $(_COW_BIN)/$(_GAME_NAME)
	@ chmod 755 $(_COW_BIN)/$(_GAME_NAME)

	@ ## Assets
	@ cp -rf ./assets/ $(_COW_SHARE)/assets

	@ echo "---> Done... We **really** hope that you have fun :D"



################################################################################
## Release                                                                    ##
################################################################################
gen-binary:
	## Remove old stuff...
	rm -rf build     \
	       dist      \
	       bin       \
	       $(_GAME_NAME).spec

	## Pyinstaller
	pyinstaller -F --windowed        \
	            --name=$(_GAME_NAME) \
	            ./src/main.py

	## Create a brand new directory and copy the pyinstaller
	## generated binary, assets and infos to it.
	mkdir -p ./bin/game_$(_GAME_NAME)
	cp -r ./assets/             ./bin/game_$(_GAME_NAME)/assets
	cp    ./dist/$(_GAME_NAME)  ./bin/game_$(_GAME_NAME)/$(_GAME_NAME)
	cp AUTHORS.txt   \
	   CHANGELOG.txt \
	   COPYING.txt   \
	   README.md     \
	   TODO.txt      \
	   ./bin/game_$(_GAME_NAME)

	## Genereate the zip...
	cd ./bin && zip -r ./$(HOST)_$(_GIT_TAG).zip ./game_$(_GAME_NAME)
	rm -rf ./bin/game_$(_GAME_NAME)


gen-archive:
	mkdir -p ./archives

	git archive --output ./archives/source_game_$(_GAME_NAME)_$(_GIT_TAG).zip    master
	git archive --output ./archives/source_game_$(_GAME_NAME)_$(_GIT_TAG).tar.gz master


################################################################################
## Dev                                                                        ##
################################################################################
dev-build:
	python ./src/main.py ./assets
	rm ./src/*.pyc
