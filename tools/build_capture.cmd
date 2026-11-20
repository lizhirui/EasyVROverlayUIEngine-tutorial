@echo off
setlocal
if "%~6"=="" exit /b 2
set VSCMD_SKIP_SENDTELEMETRY=1
set VSLANG=1033
call "%~1" >nul
if errorlevel 1 exit /b 1
"%~2" -S "%~3" -B "%~4" -G Ninja "-DCMAKE_MAKE_PROGRAM=%~5" -DCMAKE_BUILD_TYPE=Release -DEASYVRUI_BUILD_TESTS=ON -DENGINE_INTERFACE_BUILD_PYTHON_BINDING=OFF "-DCMAKE_PROJECT_easyvrui_INCLUDE=%~dp0capture_project.cmake"
if errorlevel 1 exit /b 1
"%~2" --build "%~4" --config Release --parallel 8 --target %~6
exit /b %errorlevel%
