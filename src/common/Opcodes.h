#ifndef __VSVM_OPCODES_H__
#define __VSVM_OPCODES_H__

#include <cstdint>



//==============//
//  OPERATIONS  //
//==============//

#define     NUM_OPS     32

// reserved
#define     OP_RES      0x00

// data movement
#define     OP_MOV      0x01

// arithmetic operations
#define     OP_ADD      0x02
#define     OP_SUB      0x03
#define     OP_MUL      0x04
#define     OP_DIV      0x05
#define     OP_MOD      0x06

// bitwise operations
#define     OP_AND      0x07
#define     OP_OR       0x08
#define     OP_XOR      0x09
#define     OP_NOT      0x0A
#define     OP_SHL      0x0B
#define     OP_SHR      0x0C

// memory access
#define     OP_LD1      0x0D
#define     OP_LD2      0x0E
#define     OP_STR1     0x0F
#define     OP_STR2     0x10
#define     OP_PUSH     0x11
#define     OP_POP      0x12

// low-level control flow
#define     OP_JMP      0x13
#define     OP_CMP      0x14
#define     OP_JE       0x15
#define     OP_JNE      0x16
#define     OP_JL       0x17
#define     OP_JLE      0x18
#define     OP_JG       0x19
#define     OP_JGE      0x1A

// high-level control flow
#define     OP_CALL     0x1B
#define     OP_RET      0x1C

// special instructions
#define     OP_SYS      0x1D
#define     OP_HLT      0x1E
#define     OP_NOP      0x1F



//===================//
//  OPERAND FORMATS  //
//===================//

#define     NUM_OP_FMTS     8

#define     OP_FMT_O        0x0
#define     OP_FMT_OR       0x1
#define     OP_FMT_ORR      0x2
#define     OP_FMT_ORM      0x3
#define     OP_FMT_OMR      0x4
#define     OP_FMT_OI       0x5
#define     OP_FMT_ORI      0x6
#define     OP_FMT_OMI      0x7

extern const bool VALID_OP_FMTS[][NUM_OP_FMTS];



#endif // __VSVM_OPCODES_H__