import enum
import sys


################
#  OPERATIONS  #
################

class OpInsn(enum.IntEnum):
    RESERVED = 0x00,
    MOV = 0x01
    ADD = 0x02
    SUB = 0x03
    MUL = 0x04
    DIV = 0x05
    MOD = 0x06
    AND = 0x07
    OR = 0x08
    XOR = 0x09
    NOT = 0x0A
    SHL = 0x0B
    SHR = 0x0C
    LD1 = 0x0D
    LD2 = 0x0E
    STR1 = 0x0F
    STR2 = 0x10
    PUSH = 0x11
    POP = 0x12
    JMP = 0x13
    CMP = 0x14
    JE = 0x15
    JNE = 0x16
    JL = 0x17
    JLE = 0x18
    JG = 0x19
    JGE = 0x1A
    CALL = 0x1B
    RET = 0x1C
    SYS = 0x1D,
    HLT = 0x1E,
    NOP = 0x1F

op_insns = ["reserved","mov","add","sub","mul","div","mod","and","or","xor","not","shl","shr","ld1","ld2","str1","str2","push","pop","jmp","cmp","je","jne","jl","jle","jg","jge","call","ret","sys","hlt","nop"]
op_insns_d = {}
for i in range(len(op_insns)):
    op_insns_d[op_insns[i]] = i

def IsOpInsn(s):
    if s in op_insns:
        return True
    return False


###############
#  REGISTERS  #
###############

regs = ["R0","R1","R2","R3","R4","R5","R6","R7","BP","SP","IP","FL"]
regsd = {}
for i in range(len(regs)):
    regsd[regs[i]] = i
    
def IsRegister(s):
    if s in regs:
        return True
    return False

def IsRegisterMemory(s):
    if len(s) > 2:
        if s[0] == '[' and s[-1] == ']':
            reg = s[1:-1]
            if reg in regs:
                return True
    return False


#####################
#  OPERAND FORMATS  #
#####################

class OperandFormat(enum.IntEnum):
    O = 0
    OR = 1
    ORR = 2
    ORM = 3
    OMR = 4
    OI = 5
    ORI = 6
    OMI = 7

operand_format_sizes = {}
operand_format_sizes[OperandFormat.O] = 1
operand_format_sizes[OperandFormat.OR] = 2
operand_format_sizes[OperandFormat.ORR] = 2
operand_format_sizes[OperandFormat.ORM] = 2
operand_format_sizes[OperandFormat.OMR] = 2
operand_format_sizes[OperandFormat.OI] = 3
operand_format_sizes[OperandFormat.ORI] = 4
operand_format_sizes[OperandFormat.OMI] = 4

valid_formats = []
valid_formats.append([ False, False, False, False, False, False, False, False ]) # reserved
valid_formats.append([ False, False, True , False, False, False, True , False ]) # mov
valid_formats.append([ False, False, True , False, False, False, True , False ]) # add
valid_formats.append([ False, False, True , False, False, False, True , False ]) # sub
valid_formats.append([ False, False, True , False, False, False, True , False ]) # mul
valid_formats.append([ False, False, True , False, False, False, True , False ]) # div
valid_formats.append([ False, False, True , False, False, False, True , False ]) # mod
valid_formats.append([ False, False, True , False, False, False, True , False ]) # and
valid_formats.append([ False, False, True , False, False, False, True , False ]) # or
valid_formats.append([ False, False, True , False, False, False, True , False ]) # xor
valid_formats.append([ False, True , False, False, False, False, False, False ]) # not
valid_formats.append([ False, False, True , False, False, False, True , False ]) # shl
valid_formats.append([ False, False, True , False, False, False, True , False ]) # shr
valid_formats.append([ False, False, False, True , False, False, False, False ]) # ld1
valid_formats.append([ False, False, False, True , False, False, False, False ]) # ld2
valid_formats.append([ False, False, False, False, True , False, False, True  ]) # str1
valid_formats.append([ False, False, False, False, True , False, False, True  ]) # str2
valid_formats.append([ False, True , False, False, False, True , False, False ]) # push
valid_formats.append([ False, True , False, False, False, False, False, False ]) # pop
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jmp
valid_formats.append([ False, True , False, False, False, False, True,  False ]) # cmp
valid_formats.append([ False, True , False, False, False, True , False, False ]) # je
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jne
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jl
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jle
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jg
valid_formats.append([ False, True , False, False, False, True , False, False ]) # jge
valid_formats.append([ False, True , False, False, False, True , False, False ]) # call
valid_formats.append([ True , False, False, False, False, False, False, False ]) # ret
valid_formats.append([ True , False, False, False, False, False, False, False ]) # sys
valid_formats.append([ True , False, False, False, False, False, False, False ]) # hlt
valid_formats.append([ True , False, False, False, False, False, False, False ]) # nop


class Instruction:
    operation = 0x00
    operand_format = 0
    rega = 0x00
    regb = 0x00
    imm = 0x0000
    lbl = ""

    def Serialize(self):

        if valid_formats[self.operation][self.operand_format] != True:
            sys.stderr.write("[!] invalid operand format %s for operation %s\n" % (str(self.operand_format), str(self.operation)))
            return None

        arr = bytearray()
        b0 = self.operation | (self.operand_format << 5)
        arr.append(b0)

        imm0 = (self.imm & 0x00FF)
        imm1 = (self.imm >> 8)

        if self.operand_format == OperandFormat.O:
            pass
        elif self.operand_format == OperandFormat.OR:
            b1 = self.rega
            arr.append(b1)
        elif self.operand_format == OperandFormat.ORR or \
             self.operand_format == OperandFormat.ORM or \
             self.operand_format == OperandFormat.OMR:
            b1 = self.rega | (self.regb << 4)
            arr.append(b1)
        elif self.operand_format == OperandFormat.OI:
            b1 = imm0
            arr.append(b1)
            b2 = imm1
            arr.append(b2)
        elif self.operand_format == OperandFormat.ORI or \
             self.operand_format == OperandFormat.OMI:
            b1 = self.rega | (self.regb << 4)
            arr.append(b1)
            b2 = imm0
            arr.append(b2)
            b3 = imm1
            arr.append(b3)
        else:
            sys.stderr.write("[!] (this should not be possible)\n");
            return None

        return arr