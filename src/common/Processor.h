#ifndef __VSVM_PROCESSOR_H__
#define __VSVM_PROCESSOR_H__

#include <cstdint>



namespace vsvm
{
    class Processor
    {
    public:
        Processor();

        ~Processor();

        uint16_t GetRegister(
            int regno);

        void SetRegister(
            int         regno,
            uint16_t    value);

        void Reset();

    private:
        uint16_t registers[12];
    };
}



#endif // __VSVM_PROCESSOR_H__