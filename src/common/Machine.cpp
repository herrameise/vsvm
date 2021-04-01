#include "Machine.h"
using namespace vsvm;

#include <cstdio>
#include <cstring>

#include "Instruction.h"
#include "Opcodes.h"
#include "Processor.h"
#include "Registers.h"



Machine::Machine()
{
    m_processor = new Processor;
    Reset();
}


Machine::~Machine()
{
    delete m_processor;
}


void Machine::Reset()
{
    m_processor->Reset();
    memset((void*)m_memory, 0x00, sizeof(m_memory));
}


VSVM_ERROR Machine::Crank()
{
    uint16_t ip = m_processor->GetRegister(REG_IP);
    
    // reach end of memory
    if (ip >= (sizeof(m_memory) - 4))
    {
        return VSVM_OUT_OF_MEMORY;
    }
    
    Instruction* insn = new Instruction();
    unsigned int size;
    if (insn->Deserialize(&m_memory[ip], &size) != VSVM_SUCCESS)
    {
        return VSVM_BAD_INSTRUCTION;
    }
    
    // process instruction
    
    ip += size;
    m_processor->SetRegister(REG_IP, ip);
    
    return VSVM_SUCCESS;
}