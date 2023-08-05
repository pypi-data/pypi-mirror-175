/*
 * Copyright (c) 2016-2021 Arm Limited.
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
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#ifndef ARM_COMPUTE_NEBITWISEAND_H
#define ARM_COMPUTE_NEBITWISEAND_H

#include "arm_compute/runtime/NEON/INESimpleFunctionNoBorder.h"

namespace arm_compute
{
class ITensor;

/** Basic function to run @ref NEBitwiseAndKernel */
class NEBitwiseAnd : public INESimpleFunctionNoBorder
{
public:
    /** Constructor */
    NEBitwiseAnd() = default;
    /** Prevent instances of this class from being copied (As this class contains pointers) */
    NEBitwiseAnd(const NEBitwiseAnd &) = delete;
    /** Prevent instances of this class from being copied (As this class contains pointers) */
    NEBitwiseAnd &operator=(const NEBitwiseAnd &) = delete;
    /** Prevent instances of this class from being moved (As this class contains non movable objects) */
    NEBitwiseAnd(NEBitwiseAnd &&) = delete;
    /** Prevent instances of this class from being moved (As this class contains non movable objects) */
    NEBitwiseAnd &operator=(NEBitwiseAnd &&) = delete;
    /** Default destructor */
    ~NEBitwiseAnd() = default;
    /** Initialise the kernel's inputs and output
     *
     * Valid data layouts:
     * - All
     *
     * Valid data type configurations:
     * |src            |dst            |
     * |:--------------|:--------------|
     * |U8             |U8             |
     *
     * @param[in]  input1 First tensor input. Data type supported: U8.
     * @param[in]  input2 Second tensor input. Data type supported: U8.
     * @param[out] output Output tensor. Data type supported: U8.
     */
    void configure(const ITensor *input1, const ITensor *input2, ITensor *output);
};
} // namespace arm_compute
#endif /* ARM_COMPUTE_NEBITWISEAND_H */
