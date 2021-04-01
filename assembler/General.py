import enum
import string

from Code import *
from Data import *



class SectionLabel(enum.Enum):
    CODE = 0
    DATA = 1

section_labels = ["CODE", "DATA"]

def IsSectionLabel(s):
    if s in section_labels:
        return True
    return False


#############
#  STRINGS  #
#############


def IsId(s):
    if s[0] in string.ascii_letters or s[0] == '_':
        for c in s:
            if c not in string.ascii_letters and c not in string.digits and c != '_':
                return False
        if IsSectionLabel(s):
            return False
        elif IsOpInsn(s):
            return False
        elif IsRegister(s):
            return False
        elif IsOpAlloc(s):
            return False
        else:
            return True
    return False


def IsImmDec(s):
    for c in s:
        if c not in string.digits:
            return False
    return True


def IsImmHex(s):
    if len(s) > 2:
        if s[0:2] == "0x":
            for c in s[2:]:
                if c not in string.hexdigits:
                    return False
            return True
    return False


def IsImmAscii(s):
    if len(s) == 3:
        if s[0] == '\'' and s[-1] == '\'':
            if s[1] in string.printable:
                return True
    return False


def StringToImmArray(s):
    arr = []
    for c in s:
        arr.append(ord(c))
    arr.append(0x00)
    return arr
    

###########
#  LINES  #
###########


def IsWhitespaceLine(line):
    for c in line:
        if c not in string.whitespace:
            return False
    return True


def IsCommentLine(line):
    if (len(line) > 2):
        if (line[0:2] == "//"):
            return True
    return False


def IsContentLine(line):
    if line == "":
        return False
    elif IsWhitespaceLine(line):
        return False
    elif IsCommentLine(line):
        return False
    else:
        return True