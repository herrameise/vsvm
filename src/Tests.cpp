#include "Tests.h"

#include <cstdio>
#include <cstring>

#include "common/Instruction.h"
#include "common/Machine.h"
#include "common/Names.h"
#include "common/Opcodes.h"
#include "common/Processor.h"
#include "common/Registers.h"
using namespace vsvm;



unsigned int RunTests()
{
    unsigned int failed = 0;
    
    if (Test_InstructionHardCoded() == false) { failed++; }
    if (Test_InstructionSerialization() == false) { failed++; }
    
    return failed;
}


bool Test_InstructionHardCoded()
{
    printf("\n");
    printf("TEST CASE: Instruction - Hard Coded\n");
    
    Instruction insns[NUM_OP_FMTS];
    const char* expected[NUM_OP_FMTS];
    
    // "O" instruction
    insns[0].operation = OP_SYS;
    insns[0].operand_format = OP_FMT_O;
    expected[0] = "sys";
    
    // "OR" instruction
    insns[1].operation = OP_POP;
    insns[1].operand_format = OP_FMT_OR;
    insns[1].rega = REG_R5;
    expected[1] = "pop     R5";
    
    // "ORR" instruction
    insns[2].operation = OP_XOR;
    insns[2].operand_format = OP_FMT_ORR;
    insns[2].rega = REG_R1;
    insns[2].regb = REG_R7;
    expected[2] = "xor     R1, R7";
    
    // "ORM" instruction
    insns[3].operation = OP_LD2;
    insns[3].operand_format = OP_FMT_ORM;
    insns[3].rega = REG_R4;
    insns[3].regb = REG_R5;
    expected[3] = "ld2     R4, [R5]";
    
    // "OMR" instruction
    insns[4].operation = OP_STR1;
    insns[4].operand_format = OP_FMT_OMR;
    insns[4].rega = REG_R0;
    insns[4].regb = REG_R6;
    expected[4] = "str1    [R0], R6";
    
    // "OI" instruction
    insns[5].operation = OP_PUSH;
    insns[5].operand_format = OP_FMT_OI;
    insns[5].imm = 3456;
    expected[5] = "push    3456";
    
    // "ORI" instruction
    insns[6].operation = OP_SHL;
    insns[6].operand_format = OP_FMT_ORI;
    insns[6].rega = REG_R3;
    insns[6].imm = 8;
    expected[6] = "shl     R3, 8";
    
    // "OMI" instruction
    insns[7].operation = OP_STR2;
    insns[7].operand_format = OP_FMT_OMI;
    insns[7].rega = REG_R7;
    insns[7].imm = 5280;
    expected[7] = "str2    [R7], 5280";
    
    unsigned int failed = 0;
    
    for (unsigned int i = 0; i < NUM_OP_FMTS; i++)
    {
        printf("\n");
        printf("  [*] test case %u of %u\n", i+1, NUM_OP_FMTS);
        
        char output[1024];
        if(insns[i].ToAssemblyText(output) == false)
        {
            printf("    [!] ToAssemblyText() failed\n");
            failed++;
            continue;
        }
        
        printf("    output:       %s\n", output);
        printf("    expected:     %s\n", expected[i]);
        
        if (strcmp(output, expected[i]) != 0)
        {
            printf("    [!] <<< FAIL >>>\n");
            failed++;
        }
    }

    if (failed > 0) { return false; }
    else { return true; }
}



bool Test_InstructionSerialization()
{
    printf("\n");
    printf("TEST CASE: Instruction - Serialization\n");
    
    uint8_t expected_raw[NUM_OP_FMTS][4] =
    {
        { 0x1D, 0x00, 0x00, 0x00 },
        { 0x32, 0x05, 0x00, 0x00 },
        { 0x49, 0x71, 0x00, 0x00 },
        { 0x6E, 0x54, 0x00, 0x00 },
        { 0x8F, 0x60, 0x00, 0x00 },
        { 0xB1, 0x80, 0x0D, 0x00 },
        { 0xCB, 0x03, 0x08, 0x00 },
        { 0xF0, 0x07, 0xA0, 0x14 }
    };
    
    unsigned int expected_size[NUM_OP_FMTS] =
    {
        1, 2, 2, 2, 2, 3, 4, 4
    };
    
    const char* expected_text[NUM_OP_FMTS] =
    {
        "sys",
        "pop     R5",
        "xor     R1, R7",
        "ld2     R4, [R5]",
        "str1    [R0], R6",
        "push    3456",
        "shl     R3, 8",
        "str2    [R7], 5280"
    };

    unsigned int failed = 0;
    
    for (unsigned int i = 0; i < NUM_OP_FMTS; i++)
    {
        printf("\n");
        printf("  [*] test case %u of %u\n", i+1, NUM_OP_FMTS);
        
        Instruction insn;
        unsigned int size;
        
        printf("    Deserialize()\n");
        
        if (insn.Deserialize(expected_raw[i], &size) == false)
        {
            printf("      [!] Instruction::Deserialize() failed\n");
            failed++;
            continue;
        }
        
        printf("      output:       %u bytes\n", size);
        printf("      expected:     %u bytes\n", expected_size[i]);
        
        if (size != expected_size[i])
        {
            printf("      [!] <<< FAIL >>>\n");
            failed++;
            continue;
        }
        
        printf("    ToAssemblyText()\n");
        
        char out_text[1024];
        if (insn.ToAssemblyText(out_text) == false)
        {
            printf("      [!] Instruction::ToAssemblyText() failed\n");
            failed++;
            continue;
        }
        
        printf("      output:       %s\n", out_text);
        printf("      expected:     %s\n", expected_text[i]);
        
        if (strcmp(out_text, expected_text[i]) != 0)
        {
            printf("      [!] <<< FAIL >>>\n");
            failed++;
            continue;
        }
        
        printf("    Serialize()\n");
        
        uint8_t out_raw[4];
        if (insn.Serialize(out_raw, &size) == false)
        {
            printf("      [!] Instruction::Serialize() failed\n");
            failed++;
            continue;
        }
        
        printf("      output:       %02X %02X %02X %02X\n",
            out_raw[0], out_raw[1], out_raw[2], out_raw[3]);

        printf("      expected:     %02X %02X %02X %02X\n",
            expected_raw[i][0], expected_raw[i][1],
            expected_raw[i][2], expected_raw[i][3]);
        
        if (memcmp(out_raw, expected_raw[i], 0) != 0)
        {
            printf("      [!] <<< FAIL >>>\n");
            failed++;
            continue;
        }
    }
    
    if (failed > 0) { return false; }
    else { return true; }
}