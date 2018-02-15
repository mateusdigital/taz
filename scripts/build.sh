##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : build.sh                                                      ##
##  Project   : Taz                                                           ##
##  Date      : Fev 14, 2018                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2018                                             ##
##                                                                            ##
##  Description :                                                             ##
##    - Builds and packages the game for multiple platforms.                  ##
##    - This script depends on Amazing Cow's acow_shellscript_utils           ##
##      installed on its default place.                                       ##
##    - Windows builds needs to be done on an actual Windows machine          ##
##      this is the requirement of cx_Freeze, but GNU/Linux can be built      ##
##      using Windows Subsystem for Linux (WSL).                              ##
##    - To learn how use this script just type on shell:                      ##
##        $ build.sh --help                                                   ##
##                                                                            ##
##      Have fun ;D                                                           ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
source /usr/local/src/acow_shellscript_utils.sh


##----------------------------------------------------------------------------##
## Vars                                                                       ##
##----------------------------------------------------------------------------##
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";

PLATFORM="gnu_linux";  ## Default value.
VERSION="";            ## Default value.
MAKE_ZIP="false";      ## Default value.
BUILD_ENABLED="false"; ## false will disable the build phase.


##----------------------------------------------------------------------------##
## Functions                                                                  ##
##----------------------------------------------------------------------------##
show_help()
{
    cat << END_TEXT
    build.sh
      -h | --help                                  - Show this info.
      -p | --platform <*gnu_linux | web | windows> - Target platform.
      -v | --version  <major.minor.release>        - The version number of package.
      -z | --zip                                   - Generate the release zip file.

    Options marked with * is assumed to be the default if none is given.

    [Windows] builds requires that the VsDevCmd.bat path be correctly set.
END_TEXT

    exit $1
}

parse_cmd_line()
{
    for FLAG in $@; do
        shift;
        case $FLAG in
            -h | --help     ) show_help 0;     ;;
            -m | --mode     ) MODE="$1";       ;;
            -p | --platform ) PLATFORM="$1";   ;;
            -z | --zip      ) MAKE_ZIP="true"; ;;
            -v | --version  ) VERSION="$1"     ;;
        esac
    done;
}


validate_options()
{
    ##--------------------------------------------------------------------------
    ## Check if platform is valid.
    PLATFORM=$(to_lower $PLATFORM);

    test "$PLATFORM" == "gnu_linux"     || \
    test "$PLATFORM" == "windows"       || \
        fatal "Invalid platform: ($PLATFORM)";

    ##--------------------------------------------------------------------------
    ## Check if version number is valid.
    if [ "$MAKE_ZIP" == "true" ]; then
        local GREP_RESULT=$(  \
            echo "$VERSION" | \
            grep "^[[:digit:]]\.[[:digit:]]\.[[:digit:]]$" \
        );

        test -z "$GREP_RESULT" && fatal "Version number is invalid: ($VERSION)";
    fi;
}


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
parse_cmd_line "$@";
validate_options;

cd $SCRIPT_DIR;


##----------------------------------------------------------------------------##
## Log                                                                        ##
##----------------------------------------------------------------------------##
echo $(center_text "Game Taz");
echo "Build Script directory: ($SCRIPT_DIR)";
echo "Target platform       : ($PLATFORM)";
echo "Generate release zip  : ($MAKE_ZIP)";
echo $(center_text "");


##----------------------------------------------------------------------------##
## Build                                                                      ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
## GNU/Linux
if [ "$PLATFORM" == "gnu_linux" ]; then
    ## Just call the correct build script...
    test "$BUILD_ENABLED" == "true" && ./build/build_gnu_linux.sh

##------------------------------------------------------------------------------
## Windows.
elif [ "$PLATFORM" == "windows" ]; then
    ## We need this awful hack because the cmd.exe refuses to run the script
    ## if we only pass the relative path. Don't blame me...
    CURR_WINDOWS_PATH=$(                                                       \
        powershell.exe -Command \& \{                                          \
            [io.path]::combine\(                                               \
                [environment]::CurrentDirectory,                               \
                \"build/build_windows.bat\"                                    \
             \)                                                                \
        \}
    );
    CURR_WINDOWS_PATH=$(echo "$CURR_WINDOWS_PATH" | sed s@\\\\@/@g);
    test "$BUILD_ENABLED" == "true" && cmd.exe /C ${CURR_WINDOWS_PATH}
fi;


##----------------------------------------------------------------------------##
## Make zip                                                                   ##
##----------------------------------------------------------------------------##
if [ "$MAKE_ZIP" == "true" ]; then
    ##--------------------------------------------------------------------------
    ## Create the target directory.
    ZIP_NAME="${PLATFORM}_v${VERSION}";
    TARGET_PATH="../$ZIP_NAME";

    rm -rf "$TARGET_PATH"; ## Clean
    mkdir  "$TARGET_PATH"; ## Create new.

    ##--------------------------------------------------------------------------
    ## Copy the files.
    FILES_TO_ZIP=$(./files_to_zip.sh "$PLATFORM");
    echo $FILES_TO_ZIP;
    for ITEM in $FILES_TO_ZIP; do
        ##----------------------------------------------------------------------
        ## Directory - Copy its contents.
        if [ -d "$ITEM" ]; then
            for I in $(ls $ITEM); do
                CP_PATH="$ITEM/$I";
                echo "Copying ($CP_PATH) -> ($TARGET_PATH)";
                cp -R $CP_PATH  $TARGET_PATH;
            done;
        ##----------------------------------------------------------------------
        ## Regular file - Just copy it.
        else
            echo "Copying ($CP_PATH) -> ($TARGET_PATH)";
            cp  $ITEM $TARGET_PATH;
        fi;
    done;

    ##--------------------------------------------------------------------------
    ## Make the zip.
    cd "${TARGET_PATH}";            ## Need to make the contents more nicer.
    zip -rv "${ZIP_NAME}.zip" ".";  ## Zip everything on this folder.
    mv "${ZIP_NAME}.zip" "../";     ## Put the .zip on the right place.
    cd - > /dev/null                ## Go back...
fi;
