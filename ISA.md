# Instruction Set Architecture

VSVM uses a **variable-width** instruction set, with instruction sizes ranging from 8-32 bits (1-4 bytes).

The first byte of the instruction is the **opcode**. This byte is further divided into the **operation** (bits 0-4) and the **operand format** (bits 5-7). The subsequent zero, one, two, or three bytes depend on the opcode.

## Operand Format

There are eight types of operand formats supported in the VSVM ISA:

Format | Value | Bytes | Template | Example
------ | ----- | ----- | -------- | -------
`O` | `0x0` | 1 | `op` | `sys`
`OR` | `0x1` | 2 | `op REGA` | `pop     R5`
`ORR` | `0x2` | 2 | `op REGA, REGB` | `xor     R1, R7`
`ORM` | `0x3` | 2 | `op REGA, [REGB]` | `ld2     R4, [R5]`
`OMR` | `0x4` | 2 | `op [REGA], REGB` | `str1    [R0], R6`
`OI` | `0x5` | 3 | `op IMM` | `push    34`
`ORI` | `0x6` | 4 | `op REGA, IMM` | `shl     R3, 8`
`OMI` | `0x7` | 4 | `op [REGA], IMM` | `str2    [R7], 5280`

![encoding](/images/encoding.png)

## Addressing

There are many different ways to encode memory addresses in instructions (see the [Wikipedia page](https://en.wikipedia.org/wiki/Addressing_mode) for more info). When a memory address is *hard-coded in an instruction*, VSVM uses "PC-relative addressing." When an address is loaded *from a register*, VSVM uses "direct addressing."
