#!/usr/bin/env bash

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
source /usr/local/src/stdmatt/shellscript_utils/main.sh

##----------------------------------------------------------------------------##
## Constants                                                                  ##
##----------------------------------------------------------------------------##
PROJECT_NAME="taz";


##----------------------------------------------------------------------------##
## Vars                                                                       ##
##----------------------------------------------------------------------------##
## Dirs
SCRIPT_DIR="$(pw_get_script_dir)";
PROJECT_ROOT=$(pw_abspath "$SCRIPT_DIR/..");
BUILD_DIR=$(pw_abspath "$PROJECT_ROOT/build");
DIST_DIR=$(pw_abspath "$PROJECT_ROOT/dist");

## Info
PROJECT_VERSION="$(bump-the-version     \
    "${PROJECT_ROOT}/src/constants.py"  \
    "GAME_VERSION ="                    \
    "show")";

DIST_FILES="                   \
    ${BUILD_DIR}/$PROJECT_NAME \
    ${PROJECT_ROOT}/assets/    \

";


##----------------------------------------------------------------------------##
## Functions                                                                  ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
show_help()
{
    cat << END_TEXT
Usage:
    build.sh
      --help  - Show this info.
      --clean - Cleans the build files.
      --dist  - Generate the release zip file.
END_TEXT

    exit $1
}


##------------------------------------------------------------------------------
clean()
{
    pw_func_log "Cleaning files...";

    pw_func_log "   Build path: $(pw_FC $BUILD_DIR)";
    rm -rf "${BUILD_DIR}";

    pw_func_log "   Dist path: $(pw_FC $DIST_DIR)";
    rm -rf "${DIST_DIR}"
}


##----------------------------------------------------------------------------##
## Script                                                                     ##
##----------------------------------------------------------------------------##
cd "${PROJECT_ROOT}";

##
## Parse the command line arguments.
if [ -n "$(pw_getopt_exists "--clean" "$@")" ]; then
    clean;
    exit 0;
fi;

##
## Build ;D
echo "Bulding (${PROJECT_NAME})";
echo "Build Script directory : $(pw_FC $SCRIPT_DIR     )";
echo "Build directory        : $(pw_FC $BUILD_DIR      )";
echo "Dist  directory        : $(pw_FC $DIST_DIR       )";
echo "Current version        : $(pw_FC $PROJECT_VERSION)";
echo "";

## It's a python project... So just copy the files...
rm    -rf "${BUILD_DIR}";
mkdir -p  "${BUILD_DIR}";

cp -r   ${PROJECT_ROOT}/src/ "${BUILD_DIR}/${PROJECT_NAME}";
rm -rf "${BUILD_DIR}/${PROJECT_NAME}/__pycache__";


##
## Create the distribution file.
if [ -n "$(pw_getopt_exists "--dist" "$@")" ]; then
    PLATFORM=$(pw_os_get_simple_name);
    echo "Packaging (${PROJECT_NAME}) version: (${PROJECT_VERSION})";

    PACKAGE_NAME="${PROJECT_NAME}_${PROJECT_VERSION}";
    PACKAGE_DIR="${DIST_DIR}/${PACKAGE_NAME}";

    ## Clean the directory.
    rm    -rf "${PACKAGE_DIR}";
    mkdir -p  "${PACKAGE_DIR}";

    ## Copy the files to the directory.
    for ITEM in $DIST_FILES; do
        cp -R "$ITEM" "${PACKAGE_DIR}";
    done;

    ## Create the bootstrap files
    echo "#!/usr/bin/env bash"      >> "${PACKAGE_DIR}/run.sh";
    echo "python3 ./ramit/main.py"  >> "${PACKAGE_DIR}/run.sh";
    chmod 777 "${PACKAGE_DIR}/run.sh";

    cd "${DIST_DIR}"
        zip -r "${PACKAGE_NAME}.zip" "./${PACKAGE_NAME}";
    cd -
fi;
