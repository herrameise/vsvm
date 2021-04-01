#include <cstdio>

#include "common/Names.h"
#include "common/Opcodes.h"
#include "Tests.h"



int main(
    int     argc,
    char*   argv[])
{
    unsigned int failed = RunTests();
    
    printf("\n\n");
    printf("=========================================\n");
    printf("SUMMARY: %u tests failed\n", failed);
    printf("=========================================\n");
    printf("\n");

    return 0;
}