//===- VectorPattern.h - Conversion pattern to the LLVM dialect -*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_CONVERSION_LLVMCOMMON_VECTORPATTERN_H
#define MLIR_CONVERSION_LLVMCOMMON_VECTORPATTERN_H

#include "mlir/Conversion/LLVMCommon/Pattern.h"
#include "mlir/Transforms/DialectConversion.h"

namespace mlir {

namespace LLVM {
namespace detail {
// Helper struct to "unroll" operations on n-D vectors in terms of operations on
// 1-D LLVM vectors.
struct NDVectorTypeInfo {
  // LLVM array struct which encodes n-D vectors.
  Type llvmNDVectorTy;
  // LLVM vector type which encodes the inner 1-D vector type.
  Type llvm1DVectorTy;
  // Multiplicity of llvmNDVectorTy to llvm1DVectorTy.
  SmallVector<int64_t, 4> arraySizes;
};

// For >1-D vector types, extracts the necessary information to iterate over all
// 1-D subvectors in the underlying llrepresentation of the n-D vector
// Iterates on the llvm array type until we hit a non-array type (which is
// asserted to be an llvm vector type).
NDVectorTypeInfo extractNDVectorTypeInfo(VectorType vectorType,
                                         LLVMTypeConverter &converter);

// Express `linearIndex` in terms of coordinates of `basis`.
// Returns the empty vector when linearIndex is out of the range [0, P] where
// P is the product of all the basis coordinates.
//
// Prerequisites:
//   Basis is an array of nonnegative integers (signed type inherited from
//   vector shape type).
SmallVector<int64_t, 4> getCoordinates(ArrayRef<int64_t> basis,
                                       unsigned linearIndex);

// Iterate of linear index, convert to coords space and insert splatted 1-D
// vector in each position.
void nDVectorIterate(const NDVectorTypeInfo &info, OpBuilder &builder,
                     function_ref<void(ArrayRef<int64_t>)> fun);

LogicalResult handleMultidimensionalVectors(
    Operation *op, ValueRange operands, LLVMTypeConverter &typeConverter,
    std::function<Value(Type, ValueRange)> createOperand,
    ConversionPatternRewriter &rewriter);

LogicalResult vectorOneToOneRewrite(Operation *op, StringRef targetOp,
                                    ValueRange operands,
                                    LLVMTypeConverter &typeConverter,
                                    ConversionPatternRewriter &rewriter);
} // namespace detail
} // namespace LLVM

/// Basic lowering implementation to rewrite Ops with just one result to the
/// LLVM Dialect. This supports higher-dimensional vector types.
template <typename SourceOp, typename TargetOp>
class VectorConvertToLLVMPattern : public ConvertOpToLLVMPattern<SourceOp> {
public:
  using ConvertOpToLLVMPattern<SourceOp>::ConvertOpToLLVMPattern;
  using Super = VectorConvertToLLVMPattern<SourceOp, TargetOp>;

  LogicalResult
  matchAndRewrite(SourceOp op, typename SourceOp::Adaptor adaptor,
                  ConversionPatternRewriter &rewriter) const override {
    static_assert(
        std::is_base_of<OpTrait::OneResult<SourceOp>, SourceOp>::value,
        "expected single result op");
    return LLVM::detail::vectorOneToOneRewrite(
        op, TargetOp::getOperationName(), adaptor.getOperands(),
        *this->getTypeConverter(), rewriter);
  }
};
} // namespace mlir

#endif // MLIR_CONVERSION_LLVMCOMMON_VECTORPATTERN_H
