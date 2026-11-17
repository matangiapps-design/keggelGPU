cmake_minimum_required(VERSION 3.18)
project(keggelGPU LANGUAGES CXX CUDA)

set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CUDA_STANDARD_REQUIRED ON)

add_executable(keggelGPU src/main.cu)

target_compile_features(keggelGPU PRIVATE cxx_std_17)

if(CMAKE_CUDA_COMPILER)
    set_target_properties(keggelGPU PROPERTIES
        CUDA_ARCHITE_TARGETS "75;86"
    )
endif()
