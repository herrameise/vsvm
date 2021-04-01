#ifndef __VSVM_REGISTERS_H__
#define __VSVM_REGISTERS_H__



#define     NUM_REGS    12

// general purpose registers
#define     REG_R0      0x00
#define     REG_R1      0x01
#define     REG_R2      0x02
#define     REG_R3      0x03
#define     REG_R4      0x04
#define     REG_R5      0x05
#define     REG_R6      0x06
#define     REG_R7      0x07

// stack/function registers
#define     REG_BP      0x08
#define     REG_SP      0x09

// special registers
#define     REG_IP      0x0A
#define     REG_FL      0x0B



#endif // __VSVM_REGISTERS_H__