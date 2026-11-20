@echo off
setlocal EnableExtensions DisableDelayedExpansion
if not defined EASYVRUI_SDK_ROOT set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
if not defined EASYVRUI_NATIVE_DIR set "EASYVRUI_NATIVE_DIR=%EASYVRUI_SDK_ROOT%\api\python"
set "PYTHONPATH=%EASYVRUI_SDK_ROOT%\api\python;%PYTHONPATH%"
python.exe "%~dp0splitter_demo.py" %*
exit /b %errorlevel%
