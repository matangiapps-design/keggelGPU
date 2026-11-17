#include <cuda_runtime.h>
#include <iostream>
#include <vector>

__global__ void vectorAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    const int n = 1 << 20;
    std::vector<float> h_a(n), h_b(n), h_c(n);

    for (int i = 0; i < n; ++i) {
        h_a[i] = static_cast<float>(i);
        h_b[i] = static_cast<float>(i * 2);
    }

    float *d_a = nullptr;
    float *d_b = nullptr;
    float *d_c = nullptr;

    cudaError_t err;
    err = cudaMalloc(&d_a, n * sizeof(float));
    if (err != cudaSuccess) {
        std::cerr << "cudaMalloc a failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaMalloc(&d_b, n * sizeof(float));
    if (err != cudaSuccess) {
        std::cerr << "cudaMalloc b failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaMalloc(&d_c, n * sizeof(float));
    if (err != cudaSuccess) {
        std::cerr << "cudaMalloc c failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaMemcpy(d_a, h_a.data(), n * sizeof(float), cudaMemcpyHostToDevice);
    if (err != cudaSuccess) {
        std::cerr << "cudaMemcpy h_a failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaMemcpy(d_b, h_b.data(), n * sizeof(float), cudaMemcpyHostToDevice);
    if (err != cudaSuccess) {
        std::cerr << "cudaMemcpy h_b failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);

    err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "Kernel launch failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaMemcpy(h_c.data(), d_c, n * sizeof(float), cudaMemcpyDeviceToHost);
    if (err != cudaSuccess) {
        std::cerr << "cudaMemcpy d_c failed: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    std::cout << "GPU vector add completed successfully. Sample result: "
              << h_c[0] << ", " << h_c[1] << ", " << h_c[2] << std::endl;

    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    return 0;
}
