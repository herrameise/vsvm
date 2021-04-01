#include "Names.h"



const char* REG_NAMES[NUM_REGS] =
{
    "R0",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7",
    "BP",
    "SP",
    "IP",
    "FL"
};

const char* OP_NAMES[NUM_OPS] =
{
    "RESERVED",
    "mov",
    "add",
    "sub",
    "mul",
    "div",
    "mod",
    "and",
    "or",
    "xor",
    "not",
    "shl",
    "shr",
    "ld1",
    "ld2",
    "str1",
    "str2",
    "push",
    "pop",
    "jmp",
    "cmp",
    "je",
    "jne",
    "jl",
    "jle",
    "jg",
    "jge",
    "call",
    "ret",
    "sys",
    "hlt",
    "nop"
};

const char* OP_NAMES_SPACES[NUM_OPS] =
{
    "", // reserved
    "     ", // mov
    "     ", // add
    "     ", // sub
    "     ", // mul
    "     ", // div
    "     ", // mod
    "     ", // and
    "      ", // or
    "     ", // xor
    "     ", // not
    "     ", // shl
    "     ", // shr
    "     ", // ld1
    "     ", // ld2
    "    ", // str1
    "    ", // str2
    "    ", // push
    "     ", // pop
    "     ", // jmp
    "     ", // cmp
    "      ", // je
    "     ", // jne
    "      ", // jl
    "     ", // jle
    "      ", // jg
    "     ", // jge
    "    ", // call
    "     ", // ret
    "     ", // sys
    "     ", // hlt
    "     "  // nop
};
