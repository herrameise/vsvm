#ifndef __VSVM_INSTRUCTION_H__
#define __VSVM_INSTRUCTION_H__

#include <cstdint>



namespace vsvm
{
    class Instruction
    {
    public:
        Instruction();
        
        ~Instruction();
        
        void Reset();

        bool Validate();

        bool Serialize(
            uint8_t*        raw,
            unsigned int*   size);
            
        bool Deserialize(
            uint8_t*        raw,
            unsigned int*   size);
        
        bool ToAssemblyText(
            char* buffer);
        
        uint8_t     operation;
        uint8_t     operand_format;
        uint8_t     rega;
        uint8_t     regb;
        uint16_t    imm;
    };
}



#endif //__VSVM_INSTRUCTION_H__