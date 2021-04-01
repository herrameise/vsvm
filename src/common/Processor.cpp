#include "Processor.h"
using namespace vsvm;

#include <cstring>

#include "Registers.h"




Processor::Processor()
{
    Reset();
}


Processor::~Processor() {}


uint16_t Processor::GetRegister(
    int regno)
{
    if (regno < 0 || regno >= NUM_REGS)
    {
        return 0x0000;
    }

    return registers[regno];
}


void Processor::SetRegister(
    int         regno,
    uint16_t    val)
{
    if (regno < 0 || regno >= NUM_REGS)
    {
        return;
    }

    registers[regno] = val;
}


void Processor::Reset()
{
    memset((void*)registers, 0x00, sizeof(registers));
}