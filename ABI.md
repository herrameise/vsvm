# Application Binary Interface (ABI)

This document desribes the **ABI** (also called the **calling convention**) for VSVM programs.

## Stack Growth

The stack starts at a higher memory address and grows **down**. When a value is "pushed" onto the stack with the `push` instruction, the value of `SP` (the stack pointer) *decreases*. When a value is "popped" from the stack with the `pop` instruction, the value of `SP` *increases*.

## Return Address

Once a function has completed, execution should pick up where it left off before the function was called. To achieve this, the return address (the address of the instruction directly *after* the `call` instruction) is saved **on the stack**. This happens transparently as a part of the `call` instruction. After the function executes, the `ret` instruction will "pop" the return address into the `IP` register and execution will continue.

## Register Saving

General-purpose registers are **callee-saved** (saved by the function being called, as opposed to *caller-saved*). This means that the function must `push` all of these register values onto the stack (before it thrashes these registers) and then `pop` them before the function returns.

## Return Value

The return value (if used) is saved in register `R0`.
