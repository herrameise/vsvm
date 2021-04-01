import enum
import inspect
import string
import sys

from Code import *
from Data import *
from General import *
from Token import *


MAX_ARRAY_SIZE = 0x1000


def ExitWithLineError(tokl):
    sys.stderr.write("[!] line %u:\n" % tokl.line_number)
    sys.stderr.write("      %s\n" % tokl.line)
    sys.exit(-1)


def main():
    
    if len(sys.argv) != 2:
        sys.stderr.write("[!] usage: python3 %s <filename>\n" % sys.argv[0]);
        sys.exit(-1)

    filename = sys.argv[1]
    try:
        fp = open(filename, "r");
        lines = fp.readlines()
    except:
        sys.stdout.write("[!] failed to open input file: %s\n" % filename)
        sys.exit(-1)

    tokenized_lines = []

    # tokenize content lines
    # (discard comment/whitespace lines)
    for i in range(len(lines)):

        unstripped_line = lines[i]
        line = unstripped_line.strip('\n')
        line_number = i + 1

        if IsContentLine(line):

            tokl = TokenizeLine(line, line_number)

            if tokl:
                if CheckTokenCombo(tokl.tokens):
                    tokenized_lines.append(tokl)
                else:
                    ExitWithLineError(tokl)
            else:
                sys.stderr.write("[!] line %u:\n" % line_number)
                sys.stderr.write("      %s\n" % line)
                sys.exit(-1)

    # ensure first token starts a CODE or DATA section
    first_tokl = tokenized_lines[0]
    if first_tokl.line_type != TokenLineType.CODE_LABEL and first_tokl.line_type != TokenLineType.DATA_LABEL:
        sys.stderr.write("[!] first content line must be \"CODE:\" or \"DATA:\" section label\n")
        ExitWithLineError(first_tokl)
        sys.exit(-1)

    section = None
    pos = 0

    labels = {}

    # [+] create rough instances of instructions and allocations
    # [+] calculate size and position (offset) for each token line
    # [+] create label dictionary for resolving labels
    for tokl in tokenized_lines:

        tokl.pos = pos

        if tokl.line_type == TokenLineType.CODE_LABEL:

            section = SectionLabel.CODE
            tokl.size = 0

        elif tokl.line_type == TokenLineType.DATA_LABEL:

            section = SectionLabel.DATA
            tokl.size = 0

        elif tokl.line_type == TokenLineType.ID_LABEL:

            if tokl.tokens[0].id not in labels.keys():
                labels[tokl.tokens[0].id] = pos
            else:
                sys.stderr.write("[!] label \"%s\" already defined\n" % tokl.tokens[0].id)
                ExitWithLineError(tokl)

            tokl.size = 0

        elif tokl.line_type == TokenLineType.INSN:

            if section == SectionLabel.DATA:
                sys.stderr.write("[!] instructions cannot be in DATA section\n")
                ExitWithLineError(tokl)

            insn = Instruction()
            insn.operation = tokl.tokens[0].op
            insn.operand_format = TokenComboToOperandFormat(tokl.tokens)

            if insn.operand_format == OperandFormat.O:
                pass
            elif insn.operand_format == OperandFormat.OR:
                insn.rega = tokl.tokens[1].reg
            elif insn.operand_format == OperandFormat.ORR:
                insn.rega = tokl.tokens[1].reg
                insn.regb = tokl.tokens[2].reg
            elif insn.operand_format == OperandFormat.ORM:
                insn.rega = tokl.tokens[1].reg
                insn.regb = tokl.tokens[2].reg
            elif insn.operand_format == OperandFormat.OMR:
                insn.rega = tokl.tokens[1].reg
                insn.regb = tokl.tokens[2].reg
            elif insn.operand_format == OperandFormat.OI:
                if tokl.tokens[1].token_type == TokenType.IMM:
                    insn.imm = tokl.tokens[1].imm
                elif tokl.tokens[1].token_type == TokenType.ID:
                    insn.lbl = tokl.tokens[1].id
            elif insn.operand_format == OperandFormat.ORI:
                insn.rega = tokl.tokens[1].reg
                if tokl.tokens[2].token_type == TokenType.IMM:
                    insn.imm = tokl.tokens[2].imm
                elif tokl.tokens[2].token_type == TokenType.ID:
                    insn.lbl = tokl.tokens[2].id
            elif insn.operand_format == OperandFormat.OMI:
                insn.rega = tokl.tokens[1].reg
                insn.imm = tokens[2].imm
            else:
                sys.stderr.write("[!] (should not be possible) line %u\n" % inspect.currentframe().f_lineno);
                ExitWithLineError(tokl)
            
            tokl.size = operand_format_sizes[insn.operand_format]
            tokl.insn = insn

        elif tokl.line_type == TokenLineType.ALLOC:

            if section == SectionLabel.CODE:
                sys.stderr.write("[!] allocations cannot be in CODE section\n")
                ExitWithLineError(tokl)

            alloc = Allocation()
            alloc.id = tokl.tokens[1].id

            if alloc.id not in labels.keys():
                labels[alloc.id] = pos
            else:
                sys.stderr.write("[!] label \"%s\" already defined\n" % alloc.id)
                ExitWithLineError(tokl)

            if tokl.tokens[0].op == OpAlloc.B1:
                alloc.element_size = 1
            elif tokl.tokens[0].op == OpAlloc.B2:
                alloc.element_size = 2
            else:
                sys.stderr.write("[!] (should not be possible) line %u\n" % inspect.currentframe().f_lineno);
                ExitWithLineError(tokl)

            if tokl.tokens[1].token_type == TokenType.ID:
                if len(tokl.tokens) == 3:
                    if tokl.tokens[2].token_type == TokenType.IMM:
                        alloc.elements = [tokl.tokens[2].imm]
                    elif tokl.tokens[2].token_type == TokenType.STRING:
                        if tokl.tokens[0].op == OpAlloc.B2:
                            sys.stderr.write("[!] cannot initialize \"B2\" array with string\n")
                            ExitWithLineError(tokl) 
                        alloc.elements = StringToImmArray(tokl.tokens[2].the_string)
                else:
                    alloc.elements = [0]
            elif tokl.tokens[1].token_type == TokenType.ID_ARRAY:
                if tokl.tokens[1].num_elements > MAX_ARRAY_SIZE:
                    sys.stderr.write("[!] exceeded maximum array size\n");
                    ExitWithLineError(tokl)
                if len(tokl.tokens) == 3:
                    alloc.elements = tokl.tokens[2].elements
                else:
                    alloc.elements = [0]*tokl.tokens[1].num_elements
            else:
                sys.stderr.write("[!] (should not be possible) line %u\n" % inspect.currentframe().f_lineno);
                ExitWithLineError(tokl)
            
            tokl.size = alloc.element_size * len(alloc.elements)
            tokl.alloc = alloc
        
        else:
            sys.stderr.write("[!] (should not be possible) line %u\n" % inspect.currentframe().f_lineno);
            ExitWithLineError(tokl)

        pos += tokl.size

    # resolve labels
    for tokl in tokenized_lines:

        if tokl.line_type == TokenLineType.INSN:
            lbl = tokl.insn.lbl
            if lbl != "":
                if lbl in labels:
                    lbl_pos = labels[lbl]
                    diff = lbl_pos - tokl.pos
                    if (diff < 0):
                        diff += 0x10000 #16-bit registers
                    tokl.insn.imm = diff
                else:
                    sys.stderr.write("[!] could not find label (\"%s\")\n" % lbl)
                    ExitWithLineError(tokl)
            else:
                pass

    # assemble!
    raw = []

    for tokl in tokenized_lines:
        
        if tokl.line_type == TokenLineType.INSN:

            arr = tokl.insn.Serialize()
            if arr:
                raw += arr
            else:
                ExitWithLineError(tokl)

        elif tokl.line_type == TokenLineType.ALLOC:
            
            arr = tokl.alloc.Serialize()
            if arr:
                raw += arr
            else:
                ExitWithLineError(tokl)

        else:
            pass

    sys.stdout.write("pos: %u\n" % pos)
    sys.stdout.write("finished assembling (%u bytes)\n" % len(raw));

    fp = open("/tmp/out.vsvm", "wb")
    fp.write(bytes(raw))
    fp.close()


if __name__ == "__main__":
    main()