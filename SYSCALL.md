# Syscalls

A syscall is the interface between a program and the kernel/operating system. With VSVM, a syscall is performed using the `sys` operation and loading register `R0` with a certain number. The arguments for the syscall function (if any) go in registers `R1`, `R2`, and `R3`. The return value (if any) will be in `R0` as it is for normal functions in the [VSVM ABI](ABI.md).

Function Prototype | `R0` | `R1` | `R2` | `R3`
-------- | ---- | ---- | ---- | ----
`NULL Exit(NUM status)` | 0 | `status` | | |
`NUM Read(PTR buffer, NUM size)` | 1 | `buffer*` | `size` | |
`NUM ReadString(PTR buffer)` | 2 | `buffer*` | | |
`NULL Write(PTR buffer, NUM size)` | 3 | `buffer*` | `size` | |
`NULL WriteString(PTR buffer)` | 4 | `buffer*` | | |
`NUM NumberToString(PTR buffer, NUM number)` | 5 | `buffer*` | `number` | |

Below is an example VSVM program that displays the number `5280` on screen:
```
DATA:
B1      numbuf[64]

CODE:
mov     R2, 5280
mov     R1, numbuf
mov     R0, 5
sys

mov     R0, 4
sys
```
