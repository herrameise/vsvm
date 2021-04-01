import enum
import struct



class OpAlloc(enum.IntEnum):
    B1 = 0,
    B2 = 1

op_allocs = ["B1","B2"]
op_allocs_d = {}
for i in range(len(op_allocs)):
    op_allocs_d[op_allocs[i]] = i

def IsOpAlloc(s):
    if s in op_allocs:
        return True
    return False


class Allocation:
    id = ""
    element_size = None
    elements = []

    def Serialize(self):

        arr = bytearray()

        for element in self.elements:
            if self.element_size == 1:
                arr += struct.pack("<B", element)
            elif self.element_size == 2:
                arr += struct.pack("<H", element)

        return arr