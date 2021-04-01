#ifndef __VSVM_ERROR_H__
#define __VSVM_ERROR_H__



typedef enum VSVM_ERROR {
    VSVM_SUCCESS = 0,
    VSVM_BAD_INSTRUCTION,
    VSVM_OUT_OF_MEMORY
} VSVM_ERROR;

const char* VsvmErrorString(
    VSVM_ERROR error);



#endif // __VSVM_ERROR_H__