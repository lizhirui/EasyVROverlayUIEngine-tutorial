@echo off
setlocal EnableExtensions DisableDelayedExpansion
if "%~4"=="" exit /b 2
call "%~1\repo\sdk\engine_interface\cmake\build_component.cmd" --environment
if errorlevel 1 exit /b 1
"%EASYVRUI_CMAKE%" -S "%~1" -B "%~2" -G Ninja "-DCMAKE_MAKE_PROGRAM=%EASYVRUI_NINJA%" -DCMAKE_BUILD_TYPE=Release -DEASYVRUI_BUILD_TESTS=ON -DENGINE_INTERFACE_BUILD_PYTHON_BINDING=OFF "-DCMAKE_PROJECT_easyvrui_INCLUDE=%~3"
if errorlevel 1 exit /b 1
"%EASYVRUI_CMAKE%" --build "%~2" --config Release --parallel 8 --target %~4
exit /b %errorlevel%
