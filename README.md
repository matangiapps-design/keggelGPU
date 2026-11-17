# CMake build
cmake -S . -B build
cmake --build build

# Run
./build/keggelGPU

# Notes
# This project expects a CUDA-capable GPU and a CUDA toolkit installed on the host machine.
