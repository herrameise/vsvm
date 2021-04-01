# Syntax

This document describes how to write assembly code for VSVM.

## Identifiers

Valid identifiers (**code labels** in the `CODE` section and **memory labels** in the `DATA` section) consist of letters, numbers, and underscores. They **must start with a letter or underscore**! This allows the lexer to differentiate between identifiers and immediate values (numeric constants) more easily.

## Code Section

**Tag**: ``CODE:``

See the `Operand Format` table on the [instruction set architecture](ISA.md) page for how to write assembly instructions for each operand format.

A code label is simply a valid identifier (see above) followed by a colon:
```
mov     R1, 0
loop_start:
add     R1, 1
cmp     R1, 10
jle     loop_start
```

## Data Section

**Tag**: ``DATA:``

A "byte" is an 8-bit value and a "doublebyte" is a 16-bit value.

Data Type                   | Example
--------------------------- | -------
byte                        | `B1       counter`
byte (number)               | `B1       max_items, 12`
byte (ASCII)                | `B1       choice, 'A'`
byte array                  | `B1       values[64]`
byte array (number)         | `B1       fib[6], {1,1,2,3,5,8}`
byte array (ASCII)          | `B1       choices, {'A','B','C','D'}`
byte array (string)         | `B1       name, "Long John Silver"`
doublebyte                  | `B2       crc16`
doublebyte (number)         | `B2       num_circuits, 0xA400`
doublebyte array            | `B2       results[32]`
doublebyte array (number)   | `B2       ids[3], {0x1234, 64, 0xFACE}`

**Note**: For the "string" type of byte array, the assembler will automatically determine the length needed (to include the terminating `0x00` byte). For example, the instruction `B1 name, "Long John Silver"` will reserve 17 bytes in memory to store the string (16 bytes for "Long John Silver" plus the terminating NULL byte).
