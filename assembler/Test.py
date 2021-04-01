from Token import *


tests = []
tests.append("CODE:")
tests.append("DATA:")
tests.append("add")
tests.append("B1")
tests.append("R0")
tests.append("[R1]")
tests.append("12")
tests.append("0xA400")
tests.append("'A'")
tests.append("\"Long John Silver\"")
tests.append("{1,1,0xFACE,'A',5,8}")
tests.append("loop_start")
tests.append("loop_start:")
tests.append("numbuf[64]")
tests.append("numbuf[0x40]")


for test in tests:

    print(test + ' '*(25-len(test)), end="")

    token = TokenizeString(test)

    if token:
        print(token.token_type)
    else:
        print("(unknown token type)")