cmake_minimum_required(VERSION 3.24)
project(my_first_vr_window LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(my_first_vr_window main.cpp)
target_compile_options(my_first_vr_window PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(my_first_vr_window)
easyvrui_deploy_runtime(my_first_vr_window "${EASYVRUI_API_LINK_SHARED}")