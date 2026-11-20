cmake_minimum_required(VERSION 3.24)
project(phrase_picker LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(phrase_picker main.cpp)
target_compile_options(phrase_picker PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(phrase_picker)
easyvrui_deploy_runtime(phrase_picker "${EASYVRUI_API_LINK_SHARED}")