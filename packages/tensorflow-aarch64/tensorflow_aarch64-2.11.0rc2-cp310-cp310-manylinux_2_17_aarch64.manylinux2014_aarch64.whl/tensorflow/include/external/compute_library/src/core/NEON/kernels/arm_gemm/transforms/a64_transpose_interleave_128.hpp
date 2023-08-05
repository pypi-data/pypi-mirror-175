/*
 * Copyright (c) 2021 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

#pragma once

#ifdef __aarch64__

namespace {

void a64_transpose_interleave_128(uint32_t *out, const uint32_t *in, size_t width, size_t in_stride, size_t height)
{
    size_t out_stride = 32 * height * sizeof(uint32_t);

    __asm__ __volatile__(
      "cmp %x[height], #0x4\n"
      "blt 10f\n"
      "1:"  // Main row loop: Head
      "mov x24, %x[in]\n"
      "mov x23, %x[out]\n"
      "add x22, x24, %x[in_stride]\n"
      "add x21, x22, %x[in_stride]\n"
      "add x20, x21, %x[in_stride]\n"
      "add %x[in], x20, %x[in_stride]\n"
      "sub %x[height], %x[height], #0x4\n"
      "mov x19, %x[width]\n"
      "cmp x19, #0x20\n"
      "blt 3f\n"
      "2:"  // Main row loop: Column loop
      "ldr q15, [x24], #0x10\n"
      "sub x19, x19, #0x20\n"
      "ldr q14, [x22], #0x10\n"
      "cmp x19, #0x20\n"
      "ldr q13, [x21], #0x10\n"
      "ldr q12, [x20], #0x10\n"
      "ldr q11, [x24], #0x10\n"
      "ldr q10, [x22], #0x10\n"
      "ldr q9, [x21], #0x10\n"
      "ldr q8, [x20], #0x10\n"
      "ldr q7, [x24], #0x10\n"
      "ldr q6, [x22], #0x10\n"
      "ldr q5, [x21], #0x10\n"
      "ldr q4, [x20], #0x10\n"
      "ldr q3, [x24], #0x10\n"
      "ldr q2, [x22], #0x10\n"
      "ldr q1, [x21], #0x10\n"
      "ldr q0, [x20], #0x10\n"
      "ldr q31, [x24], #0x10\n"
      "ldr q30, [x22], #0x10\n"
      "ldr q29, [x21], #0x10\n"
      "ldr q28, [x20], #0x10\n"
      "ldr q27, [x24], #0x10\n"
      "ldr q26, [x22], #0x10\n"
      "ldr q25, [x21], #0x10\n"
      "ldr q24, [x20], #0x10\n"
      "ldr q23, [x24], #0x10\n"
      "ldr q22, [x22], #0x10\n"
      "ldr q21, [x21], #0x10\n"
      "ldr q20, [x20], #0x10\n"
      "ldr q19, [x24], #0x10\n"
      "ldr q18, [x22], #0x10\n"
      "ldr q17, [x21], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "str q15, [x23, #0x0]\n"
      "str q11, [x23, #0x10]\n"
      "str q7, [x23, #0x20]\n"
      "str q3, [x23, #0x30]\n"
      "str q31, [x23, #0x40]\n"
      "str q27, [x23, #0x50]\n"
      "str q23, [x23, #0x60]\n"
      "str q19, [x23, #0x70]\n"
      "str q14, [x23, #0x80]\n"
      "str q10, [x23, #0x90]\n"
      "str q6, [x23, #0xa0]\n"
      "str q2, [x23, #0xb0]\n"
      "str q30, [x23, #0xc0]\n"
      "str q26, [x23, #0xd0]\n"
      "str q22, [x23, #0xe0]\n"
      "str q18, [x23, #0xf0]\n"
      "str q13, [x23, #0x100]\n"
      "str q9, [x23, #0x110]\n"
      "str q5, [x23, #0x120]\n"
      "str q1, [x23, #0x130]\n"
      "str q29, [x23, #0x140]\n"
      "str q25, [x23, #0x150]\n"
      "str q21, [x23, #0x160]\n"
      "str q17, [x23, #0x170]\n"
      "str q12, [x23, #0x180]\n"
      "str q8, [x23, #0x190]\n"
      "str q4, [x23, #0x1a0]\n"
      "str q0, [x23, #0x1b0]\n"
      "str q28, [x23, #0x1c0]\n"
      "str q24, [x23, #0x1d0]\n"
      "str q20, [x23, #0x1e0]\n"
      "str q16, [x23, #0x1f0]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 2b\n"
      "3:"  // Main row loop: Column loop skip
      "cmp x19, #0x10\n"
      "blt 5f\n"
      "4:"  // Main row loop: width 16 loop: loop
      "ldr q31, [x24], #0x10\n"
      "sub x19, x19, #0x10\n"
      "ldr q30, [x22], #0x10\n"
      "cmp x19, #0x10\n"
      "ldr q29, [x21], #0x10\n"
      "ldr q28, [x20], #0x10\n"
      "ldr q27, [x24], #0x10\n"
      "ldr q26, [x22], #0x10\n"
      "ldr q25, [x21], #0x10\n"
      "ldr q24, [x20], #0x10\n"
      "ldr q23, [x24], #0x10\n"
      "ldr q22, [x22], #0x10\n"
      "ldr q21, [x21], #0x10\n"
      "ldr q20, [x20], #0x10\n"
      "ldr q19, [x24], #0x10\n"
      "ldr q18, [x22], #0x10\n"
      "ldr q17, [x21], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "str q31, [x23, #0x0]\n"
      "str q27, [x23, #0x10]\n"
      "str q23, [x23, #0x20]\n"
      "str q19, [x23, #0x30]\n"
      "str q30, [x23, #0x80]\n"
      "str q26, [x23, #0x90]\n"
      "str q22, [x23, #0xa0]\n"
      "str q18, [x23, #0xb0]\n"
      "str q29, [x23, #0x100]\n"
      "str q25, [x23, #0x110]\n"
      "str q21, [x23, #0x120]\n"
      "str q17, [x23, #0x130]\n"
      "str q28, [x23, #0x180]\n"
      "str q24, [x23, #0x190]\n"
      "str q20, [x23, #0x1a0]\n"
      "str q16, [x23, #0x1b0]\n"
      "add x23, x23, #0x40\n"
      "bge 4b\n"
      "5:"  // Main row loop: width 16 loop: skip
      "cmp x19, #0x4\n"
      "blt 7f\n"
      "6:"  // Main row loop: width 4 loop: loop
      "ldr q19, [x24], #0x10\n"
      "sub x19, x19, #0x4\n"
      "ldr q18, [x22], #0x10\n"
      "cmp x19, #0x4\n"
      "ldr q17, [x21], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "str q19, [x23, #0x0]\n"
      "str q18, [x23, #0x80]\n"
      "str q17, [x23, #0x100]\n"
      "str q16, [x23, #0x180]\n"
      "add x23, x23, #0x10\n"
      "bge 6b\n"
      "7:"  // Main row loop: width 4 loop: skip
      "cmp x19, #0x1\n"
      "blt 9f\n"
      "8:"  // Main row loop: width 1 loop: loop
      "ldr s19, [x24], #0x4\n"
      "sub x19, x19, #0x1\n"
      "ldr s18, [x22], #0x4\n"
      "cmp x19, #0x1\n"
      "ldr s17, [x21], #0x4\n"
      "ldr s16, [x20], #0x4\n"
      "str s19, [x23, #0x0]\n"
      "str s18, [x23, #0x80]\n"
      "str s17, [x23, #0x100]\n"
      "str s16, [x23, #0x180]\n"
      "add x23, x23, #0x4\n"
      "bge 8b\n"
      "9:"  // Main row loop: width 1 loop: skip
      "add %x[out], %x[out], #0x200\n"
      "cmp %x[height], #0x4\n"
      "bge 1b\n"
      "cbz %x[height], 20f\n"
      "10:"  // Main loop skip

      "11:"  // Tail row loop: Head
      "mov x24, %x[in]\n"
      "mov x23, %x[out]\n"
      "add %x[in], x24, %x[in_stride]\n"
      "sub %x[height], %x[height], #0x1\n"
      "mov x19, %x[width]\n"
      "cmp x19, #0x20\n"
      "blt 13f\n"
      "12:"  // Tail row loop: Column loop
      "ldr q23, [x24], #0x10\n"
      "sub x19, x19, #0x20\n"
      "cmp x19, #0x20\n"
      "ldr q22, [x24], #0x10\n"
      "ldr q21, [x24], #0x10\n"
      "ldr q20, [x24], #0x10\n"
      "ldr q19, [x24], #0x10\n"
      "ldr q18, [x24], #0x10\n"
      "ldr q17, [x24], #0x10\n"
      "ldr q16, [x24], #0x10\n"
      "str q23, [x23, #0x0]\n"
      "str q22, [x23, #0x10]\n"
      "str q21, [x23, #0x20]\n"
      "str q20, [x23, #0x30]\n"
      "str q19, [x23, #0x40]\n"
      "str q18, [x23, #0x50]\n"
      "str q17, [x23, #0x60]\n"
      "str q16, [x23, #0x70]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 12b\n"
      "13:"  // Tail row loop: Column loop skip
      "cmp x19, #0x10\n"
      "blt 15f\n"
      "14:"  // Tail row loop: width 16 loop: loop
      "ldr q19, [x24], #0x10\n"
      "sub x19, x19, #0x10\n"
      "cmp x19, #0x10\n"
      "ldr q18, [x24], #0x10\n"
      "ldr q17, [x24], #0x10\n"
      "ldr q16, [x24], #0x10\n"
      "str q19, [x23, #0x0]\n"
      "str q18, [x23, #0x10]\n"
      "str q17, [x23, #0x20]\n"
      "str q16, [x23, #0x30]\n"
      "add x23, x23, #0x40\n"
      "bge 14b\n"
      "15:"  // Tail row loop: width 16 loop: skip
      "cmp x19, #0x4\n"
      "blt 17f\n"
      "16:"  // Tail row loop: width 4 loop: loop
      "ldr q16, [x24], #0x10\n"
      "sub x19, x19, #0x4\n"
      "cmp x19, #0x4\n"
      "str q16, [x23, #0x0]\n"
      "add x23, x23, #0x10\n"
      "bge 16b\n"
      "17:"  // Tail row loop: width 4 loop: skip
      "cmp x19, #0x1\n"
      "blt 19f\n"
      "18:"  // Tail row loop: width 1 loop: loop
      "ldr s16, [x24], #0x4\n"
      "sub x19, x19, #0x1\n"
      "cmp x19, #0x1\n"
      "str s16, [x23, #0x0]\n"
      "add x23, x23, #0x4\n"
      "bge 18b\n"
      "19:"  // Tail row loop: width 1 loop: skip
      "add %x[out], %x[out], #0x80\n"
      "cmp %x[height], #0x1\n"
      "bge 11b\n"
      "20:"  // Done

      : [height] "+&r" (height), [in] "+&r" (in), [out] "+&r" (out)
      : [in_stride] "r" (in_stride), [out_stride] "r" (out_stride), [width] "r" (width)
      : "cc", "memory", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "x19", "x20", "x21", "x22", "x23", "x24"
    );
}

} // anonymous namespace

template<>
void Transform<32, 1, true, VLType::None>(
    float *out, const float *in, int stride, int x0, int xmax, int k0, int kmax)
{
    a64_transpose_interleave_128(
        reinterpret_cast<uint32_t *>(out),
        reinterpret_cast<const uint32_t *>(in + k0 * stride + x0),
        (xmax-x0) * sizeof(float) / 4,
        stride * sizeof(float),
        (kmax-k0)
    );
}

#endif
