cmake_minimum_required(VERSION 3.24)
project(tutorial_splitter LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(tutorial_splitter main.cpp)
target_compile_options(tutorial_splitter PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(tutorial_splitter)
easyvrui_deploy_runtime(tutorial_splitter "${EASYVRUI_API_LINK_SHARED}")
