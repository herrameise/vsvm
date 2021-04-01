#include "Opcodes.h"



const bool VALID_OP_FMTS[NUM_OPS][NUM_OP_FMTS] =
{
    { false, false, false, false, false, false, false, false }, // reserved
    { false, false, true , false, false, false, true , false }, // mov
    { false, false, true , false, false, false, true , false }, // add
    { false, false, true , false, false, false, true , false }, // sub
    { false, false, true , false, false, false, true , false }, // mul
    { false, false, true , false, false, false, true , false }, // div
    { false, false, true , false, false, false, true , false }, // mod
    { false, false, true , false, false, false, true , false }, // and
    { false, false, true , false, false, false, true , false }, // or
    { false, false, true , false, false, false, true , false }, // xor
    { false, true , false, false, false, false, false, false }, // not
    { false, false, true , false, false, false, true , false }, // shl
    { false, false, true , false, false, false, true , false }, // shr
    { false, false, false, true , false, false, false, false }, // ld1
    { false, false, false, true , false, false, false, false }, // ld2
    { false, false, false, false, true , false, false, true  }, // str1
    { false, false, false, false, true , false, false, true  }, // str2
    { false, true , false, false, false, true , false, false }, // push
    { false, true , false, false, false, false, false, false }, // pop
    { false, true , false, false, false, true , false, false }, // jmp
    { false, true , false, false, false, false, true,  false }, // cmp
    { false, true , false, false, false, true , false, false }, // je
    { false, true , false, false, false, true , false, false }, // jne
    { false, true , false, false, false, true , false, false }, // jl
    { false, true , false, false, false, true , false, false }, // jle
    { false, true , false, false, false, true , false, false }, // jg
    { false, true , false, false, false, true , false, false }, // jge
    { false, true , false, false, false, true , false, false }, // call
    { true , false, false, false, false, false, false, false }, // ret
    { true , false, false, false, false, false, false, false }, // sys
    { true , false, false, false, false, false, false, false }, // hlt
    { true , false, false, false, false, false, false, false }  // nop
};