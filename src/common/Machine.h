#ifndef __VSVM_MACHINE_H__
#define __VSVM_MACHINE_H__

#include <cstdint>

#include <vector>

#include "Error.h"



namespace vsvm
{
    class Instruction;
    class Processor;

    class Machine
    {
    public:
        Machine();

        ~Machine();

        void Reset();

        VSVM_ERROR Crank();

    private:
        Processor*  m_processor;
        uint8_t     m_memory[64*1024]; // 64 kB
        
        std::vector<Instruction*> m_history;
    };
}



#endif // __VSVM_MACHINE_H__