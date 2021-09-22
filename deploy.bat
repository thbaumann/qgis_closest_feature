REM @echo off
REM call "C:\OSGeo4W64\bin\o4w_env.bat"
REM call "C:\OSGeo4W64\bin\qt5_env.bat"
REM call "C:\OSGeo4W64\bin\py3_env.bat"

REM @echo on
REM pyrcc5 -o resources_rc.py resources.qrc
REM pause

@ECHO OFF

set OSGEO4W_ROOT=C:\OSGeo4W64

set PATH=%OSGEO4W_ROOT%\bin;%PATH%
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin

@echo off
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
@echo off
path %OSGEO4W_ROOT%\apps\qgis-dev\bin;%OSGEO4W_ROOT%\apps\grass\grass-7.6.0\lib;%OSGEO4W_ROOT%\apps\grass\grass-7.6.0\bin;%PATH%

cd /d %~dp0

@ECHO ON
::Ui Compilation
#call pyuic5 resources.ui -o resources.py


::Resources
::call pyrcc5 ui\resources.qrc -o gui\generated\resources_rc.py
call pyrcc5 -o resources.py resources.qrc

@ECHO OFF
GOTO END

:ERROR
   echo "Failed!"
   set ERRORLEVEL=%ERRORLEVEL%
   pause

:END
pause
@ECHO ON