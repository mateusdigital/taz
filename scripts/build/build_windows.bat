@echo off

echo "-- build_windows.bat --"

REM ----------------------------------------------------------------------------
REM -- Variables
set "original_cwd=%cd%";
set "src_path=..\src";

REM ----------------------------------------------------------------------------
REM -- setup.py needs to run on the src directory.
echo "Changing to src directory...";
CHDIR "%src_path%"
echo "CWD: %cd%";

REM ----------------------------------------------------------------------------
REM -- Run the setup.py
echo "Running setup.py...";
python setup.py build
