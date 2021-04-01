import enum
import sys

from Code import *
from Data import *
from General import *



class TokenLineType(enum.Enum):
    CODE_LABEL = 0
    DATA_LABEL = 1
    ID_LABEL = 2
    INSN = 3
    ALLOC = 4

class TokenType(enum.Enum):
    CODE_LABEL = 0          # CODE:
    DATA_LABEL = 1          # DATA:
    OP_INSN = 2             # mov, add, push, hlt
    OP_ALLOC = 3            # B1, B2
    REG = 4                 # R1, R3, R4
    REG_MEM = 5             # [R5], [R0]
    IMM = 6                 # 12, 0xA400
    IMM_ARRAY = 7           # {1,1,0xFACE,'A',5,8}
    STRING = 8              # "Long John Silver"
    ID = 9                  # loop_top, values, ctr, crc16
    ID_LABEL = 10           # loop_top:
    ID_ARRAY = 11           # values[64], fib[6], results[0x20], ids[3]

class Token:
    def __init__(self, token_type, s):
        self.token_type = token_type
        self.s = s


################
#  CODE_LABEL  #
################

def IsTokenCodeLabel(s):
    if s == "CODE:":
        return Token(TokenType.CODE_LABEL, s)
    return None


################
#  DATA_LABEL  #
################

def IsTokenDataLabel(s):
    if s == "DATA:":
        return Token(TokenType.DATA_LABEL, s)
    return None


#############
#  OP_INSN  #
#############

class TokenOpInsn:
    def __init__(self, s, op):
        Token.__init__(self, TokenType.OP_INSN, s)
        self.op = op

def IsTokenOpInsn(s):
    if IsOpInsn(s):
        return TokenOpInsn(s, op_insns_d[s])
    return None


##############
#  OP_ALLOC  #
##############

class TokenOpAlloc:
    def __init__(self, s, op):
        Token.__init__(self, TokenType.OP_ALLOC, s)
        self.op = op

def IsTokenOpAlloc(s):
    if IsOpAlloc(s):
        return TokenOpAlloc(s, op_allocs_d[s])
    return None


#########
#  REG  #
#########

class TokenReg:
    def __init__(self, s, reg):
        Token.__init__(self, TokenType.REG, s)
        self.reg = reg

def IsTokenReg(s):
    if IsRegister(s):
        return TokenReg(s, regsd[s])
    return None


#############
#  REG_MEM  #
#############

class TokenRegMem:
    def __init__(self, s, reg):
        Token.__init__(self, TokenType.REG_MEM, s)
        self.reg = reg

def IsTokenRegMem(s):
    if IsRegisterMemory(s):
        return TokenRegMem(s, regsd[s[1:-1]])
    return None


#########
#  IMM  #
#########

class TokenImm:
    def __init__(self, s, imm):
        Token.__init__(self, TokenType.IMM, s)
        self.imm = imm

def IsTokenImm(s):
    if IsImmDec(s):
        return TokenImm(s, int(s,10))
    elif IsImmHex(s):
        return TokenImm(s, int(s[2:],16))
    elif IsImmAscii(s):
        return TokenImm(s, ord(s[1]))
    return None


###############
#  IMM_ARRAY  #
###############

class TokenImmArray:
    def __init__(self, s, elements):
        Token.__init__(self, TokenType.IMM_ARRAY, s)
        self.elements = elements

def IsTokenImmArray(s):
    if len(s) >= 3:
        if s[0] == '{' and s[-1] == '}':
            elements = []
            elem_toks = s[1:-1].split(',')
            for s in elem_toks:
                if IsImmDec(s):
                    elements.append(int(s,10))
                elif IsImmHex(s):
                    elements.append(int(s[2:],16))
                elif IsImmAscii(s):
                    elements.append(ord(s[1]))
                else:
                    return None
            return TokenImmArray(s, elements)
    return None


############
#  STRING  #
############

class TokenString:
    def __init__(self, s, the_string):
        Token.__init__(self, TokenType.STRING, s)
        self.the_string = the_string

def IsTokenString(s):
    if len(s) >= 2:
        if s[0] == '"' and s[-1] == '"':
            the_string = s[1:-1]
            for c in the_string:
                if c not in string.printable:
                    return False
                return TokenString(s, the_string)
    return None


########
#  ID  #
########

class TokenId:
    def __init__(self, s, id):
        Token.__init__(self, TokenType.ID, s)
        self.id = id

def IsTokenId(s):
    if IsId(s):
        return TokenId(s, s)
    return None


##############
#  ID_LABEL  #
##############

class TokenIdLabel:
    def __init__(self, s, id):
        Token.__init__(self, TokenType.ID_LABEL, s)
        self.id = id

def IsTokenIdLabel(s):
    if len(s) >= 2 and s[-1] == ':':
        if IsId(s[:-1]):
            return TokenIdLabel(s, s[:-1])
    return None


##############
#  ID_ARRAY  #
##############

class TokenIdArray:
    def __init__(self, s, id, num_elements):
        Token.__init__(self, TokenType.ID_ARRAY, s)
        self.id = id
        self.num_elements = num_elements

def IsTokenIdArray(s):
    if len(s) >= 4  and s[-1] == ']':
        split_s = s[:-1].split('[')
        if len(split_s) == 2:
            id = ""
            num_elements = 0
            if IsId(split_s[0]):
                id = split_s[0]
                if IsImmDec(split_s[1]):
                    num_elements = int(split_s[1],10)
                elif IsImmHex(split_s[1]):
                    num_elements = int(split_s[1][2:],16)
                else:
                    return None
                return TokenIdArray(s, id, num_elements)
    return None


##############################
#  tokenize a single string  #
##############################

def TokenizeString(s):

    token = IsTokenCodeLabel(s)
    if token:
        return token

    token = IsTokenDataLabel(s)
    if token:
        return token

    token = IsTokenOpInsn(s)
    if token:
        return token

    token = IsTokenOpAlloc(s)
    if token:
        return token

    token = IsTokenReg(s)
    if token:
        return token

    token = IsTokenRegMem(s)
    if token:
        return token

    token = IsTokenImm(s)
    if token:
        return token

    token = IsTokenImmArray(s)
    if token:
        return token

    token = IsTokenString(s)
    if token:
        return token

    token = IsTokenId(s)
    if token:
        return token

    token = IsTokenIdLabel(s)
    if token:
        return token

    token = IsTokenIdArray(s)
    if token:
        return token

    # no token match
    return None


###########################
#  tokenize a whole line  #
###########################

class TokenizedLine:
    line = ""
    line_number = 0

    line_type = None

    tokens = []

    insn = Instruction()
    alloc = Allocation()

    size = 0
    pos = 0

def TokenizeLine(line, line_number):

    delims = []
    delims.extend(string.whitespace)
    delims.append(',')
    
    s = ""
    strings = []
    building_normal = False
    building_string_literal = False

    for c in line:

        if building_string_literal:
            s += c
            if c == '"':
                strings.append(s)
                s = ""
                building_string_literal = False

        elif building_normal:
            if c not in delims:
                s += c
            else:
                strings.append(s)
                s = ""
                building_normal = False

        else: # in-between
            if c == '"':
                building_string_literal = True
                s += c
            elif c not in delims:
                building_normal = True
                s += c
            else:
                pass
    
    # append last token
    if building_normal == True:
        strings.append(s)
        s = ""

    # no closing quotation found on string literal
    if building_string_literal == True:
        sys.stderr.write("[!] no terminating quote on string literal\n")
        return None
    
    tokens = []
    for s in strings:
        token = TokenizeString(s)
        if token:
            tokens.append(token)
        else:
            sys.stderr.write("[!] unknown token: %s\n" % s)
            return None

    line_type = None
    if tokens[0].token_type == TokenType.CODE_LABEL:
        line_type = TokenLineType.CODE_LABEL
    elif tokens[0].token_type == TokenType.DATA_LABEL:
        line_type = TokenLineType.DATA_LABEL
    elif tokens[0].token_type == TokenType.ID_LABEL:
        line_type = TokenLineType.ID_LABEL
    elif tokens[0].token_type == TokenType.OP_INSN:
        line_type = TokenLineType.INSN
    elif tokens[0].token_type == TokenType.OP_ALLOC:
        line_type = TokenLineType.ALLOC
    else:
        sys.stderr.write("[!] first token (\"%s\") cannot be %s\n" % (tokens[0].s, str(tokens[0].token_type)))
        sys.stderr.write("[!] line %u:\n" % line_number)
        sys.stderr.write("      %s\n" % line)
        return None

    tokl = TokenizedLine()
    tokl.line = line
    tokl.line_number = line_number
    tokl.line_type = line_type
    tokl.tokens = tokens

    return tokl


##############################
#  valid token combinations  #
##############################

token_combos = []
token_combos.append([TokenType.CODE_LABEL])
token_combos.append([TokenType.DATA_LABEL])
token_combos.append([TokenType.ID_LABEL])
token_combos.append([TokenType.OP_INSN])
token_combos.append([TokenType.OP_INSN, TokenType.REG])
token_combos.append([TokenType.OP_INSN, TokenType.REG, TokenType.REG])
token_combos.append([TokenType.OP_INSN, TokenType.REG, TokenType.REG_MEM])
token_combos.append([TokenType.OP_INSN, TokenType.REG_MEM, TokenType.REG])
token_combos.append([TokenType.OP_INSN, TokenType.IMM])
token_combos.append([TokenType.OP_INSN, TokenType.ID])
token_combos.append([TokenType.OP_INSN, TokenType.REG, TokenType.IMM])
token_combos.append([TokenType.OP_INSN, TokenType.REG, TokenType.ID])
token_combos.append([TokenType.OP_INSN, TokenType.REG_MEM, TokenType.IMM])
token_combos.append([TokenType.OP_ALLOC, TokenType.ID])
token_combos.append([TokenType.OP_ALLOC, TokenType.ID, TokenType.IMM])
token_combos.append([TokenType.OP_ALLOC, TokenType.ID, TokenType.STRING])
token_combos.append([TokenType.OP_ALLOC, TokenType.ID_ARRAY])
token_combos.append([TokenType.OP_ALLOC, TokenType.ID_ARRAY, TokenType.IMM_ARRAY])

def CheckTokenCombo(tokens):

    token_types = []
    for token in tokens:
        token_types.append(token.token_type)

    if token_types in token_combos:
        return True
    else:
        sys.stderr.write("[!] invalid token combination:\n")
        for i in range(len(tokens)):
            sys.stderr.write("      %s (%s)\n" % (tokens[i].s, str(tokens[i].token_type)))
        return False

def TokenComboToOperandFormat(tokens):

    token_types = []
    for token in tokens:
        token_types.append(token.token_type)

    if token_types == [TokenType.OP_INSN]:
        return OperandFormat.O
    elif token_types == [TokenType.OP_INSN, TokenType.REG]:
        return OperandFormat.OR
    elif token_types == [TokenType.OP_INSN, TokenType.REG, TokenType.REG]:
        return OperandFormat.ORR
    elif token_types == [TokenType.OP_INSN, TokenType.REG, TokenType.REG_MEM]:
        return OperandFormat.ORM
    elif token_types == [TokenType.OP_INSN, TokenType.REG_MEM, TokenType.REG]:
        return OperandFormat.OMR
    elif token_types == [TokenType.OP_INSN, TokenType.IMM]:
        return OperandFormat.OI
    elif token_types == [TokenType.OP_INSN, TokenType.ID]:
        return OperandFormat.OI
    elif token_types == [TokenType.OP_INSN, TokenType.REG, TokenType.IMM]:
        return OperandFormat.ORI
    elif token_types == [TokenType.OP_INSN, TokenType.REG, TokenType.ID]:
        return OperandFormat.ORI
    elif token_types == [TokenType.OP_INSN, TokenType.REG_MEM, TokenType.IMM]:
        return OperandFormat.OMI
    else:
        return None