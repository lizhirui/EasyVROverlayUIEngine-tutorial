cmake_minimum_required(VERSION 3.24)
project(tutorial_panel LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(tutorial_panel main.cpp)
target_compile_options(tutorial_panel PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(tutorial_panel)
easyvrui_deploy_runtime(tutorial_panel "${EASYVRUI_API_LINK_SHARED}")
