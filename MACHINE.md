# Machine Architecture

Specifications:
*  **Architecture**: von Neumann
*  **Endian-ness**: little
*  **Register Size**: 16 bits
*  **Instruction Size**: variable-width (8, 16, 24, or 32 bits)
*  **Data Bus**: single data bus between memory and processor

## Memory
There is **64 Kb** of memory (a 16-bit address space), ranging from address `0x0000` to address `0xFFFF`.

## Input/Output
Because I/O with other devices (and ultimately the human user) would be an extremely difficult thing to emulate (without an operating system, hardware drivers, etc.), it is "hand-waved" in `VSVM` through the use of the `sys` (syscall) instruction.
