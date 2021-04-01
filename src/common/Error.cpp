#include "Error.h"



const char* VsvmErrorString(
    VSVM_ERROR error)
{
    switch (error)
    {
        case VSVM_SUCCESS:
            return "success";
            break;
            
        case VSVM_BAD_INSTRUCTION:
            return "bad instruction";
            break;
            
        case VSVM_OUT_OF_MEMORY:
            return "out of memory";
            break;
            
        default:
            return "(unknown error)";
            break;
    }
}
