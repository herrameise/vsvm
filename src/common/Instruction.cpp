#include "Instruction.h"
using namespace vsvm;

#include <cstdio>
#include <cstdint>
#include <cstring>

#include <string>
using std::string;

#include "Names.h"
#include "Opcodes.h"
#include "Registers.h"



Instruction::Instruction()
{
    Reset();
}


Instruction::~Instruction() {}


void Instruction::Reset()
{
    operation = 0x00;
    operand_format = 0x00;
    rega = 0x00;
    regb = 0x00;
    imm = 0x0000;
}


bool Instruction::Validate()
{
    // operation range
    if (operation == OP_RES || operation > OP_NOP)
    {
        fprintf(stderr, "[!] VSVM: invalid operation (0x%02X)\n", operation);
        return false;
    }

    // operand format range
    if (operand_format > OP_FMT_OMI)
    {
        fprintf(stderr, "[!] VSVM: invalid operand format (0x%02X)\n", operand_format);
        return false;
    }

    // operand format validity based on operation
    if (VALID_OP_FMTS[operation][operand_format] == false)
    {
        fprintf(stderr, "[!] VSVM: invalid operand format (0x%02x) for operation (0x%02x)\n",
            operand_format, operation);
        return false;
    }

    // register A range
    if (rega > REG_SP)
    {
        if (rega == REG_IP)
        {
            fprintf(stderr, "[!] VSVM: invalid register A (REG_IP)\n");
            return false;
        }
        else if (rega == REG_FL)
        {
            fprintf(stderr, "[!] VSVM: invalid register A (REG_FL)\n");
            return false;
        }
        else
        {
            fprintf(stderr, "[!] VSVM: invalid register A (0x%02X)\n", rega);
            return false;
        }
    }

    // register B range
    if (regb > REG_SP)
    {
        if (regb == REG_IP)
        {
            fprintf(stderr, "[!] VSVM: invalid register B (REG_IP)\n");
            return false;
        }
        else if (regb == REG_FL)
        {
            fprintf(stderr, "[!] VSVM: invalid register B (REG_FL)\n");
            return false;
        }
        else
        {
            fprintf(stderr, "[!] VSVM: invalid register B (0x%02X)\n", regb);
            return false;
        }
    }
    
    // immediate value is always "valid" at this level, so no need to check it

    return true;
}


bool Instruction::Serialize(
    uint8_t*        raw,
    unsigned int*   size)
{  
    memset(raw, 0x00, 4);
    
    raw[0] = operation;
    raw[0] |= (operand_format << 5);
    
    switch (operand_format)
    {
        case OP_FMT_O:
            *size = 1;
            break;
            
        case OP_FMT_OR:
            raw[1] = rega;
            *size = 2;
            break;
            
        case OP_FMT_ORR:
            raw[1] = rega;
            raw[1] |= (regb << 4);
            *size = 2;
            break;
            
        case OP_FMT_ORM:
            raw[1] = rega;
            raw[1] |= (regb << 4);
            *size = 2;
            break;
            
        case OP_FMT_OMR:
            raw[1] = rega;
            raw[1] |= (regb << 4);
            *size = 2;
            break;
            
        case OP_FMT_OI:
            raw[1] = (uint8_t)(imm & 0x00FF);
            raw[2] = (uint8_t)(imm >> 8);
            *size = 3;
            break;
            
        case OP_FMT_ORI:
            raw[1] = rega;
            raw[2] = (uint8_t)(imm & 0x00FF);
            raw[3] = (uint8_t)(imm >> 8);
            *size = 4;
            break;
            
        case OP_FMT_OMI:
            raw[1] = rega;
            raw[2] = (uint8_t)(imm & 0x00FF);
            raw[3] = (uint8_t)(imm >> 8);
            *size = 4;
            break;
            
        default:
            // should never be possible
            return false;
            break;
    }
    
    if (Validate() == false) { return false; }
    
    return true;
}


bool Instruction::Deserialize(
    uint8_t*        raw,
    unsigned int*   size)
{
    operation = (raw[0] & 0x1F) >> 0; // bits 0-4
    operand_format = (raw[0] & 0xE0) >> 5; // bits 5-7
    
    switch (operand_format)
    {
        case OP_FMT_O:
            *size = 1;
            break;
            
        case OP_FMT_OR:
            rega = (raw[1] & 0x0F) >> 0;
            *size = 2;
            break;
            
        case OP_FMT_ORR:
            rega = (raw[1] & 0x0F) >> 0;
            regb = (raw[1] & 0xF0) >> 4;
            *size = 2;
            break;
            
        case OP_FMT_ORM:
            rega = (raw[1] & 0x0F) >> 0;
            regb = (raw[1] & 0xF0) >> 4;
            *size = 2;
            break;
            
        case OP_FMT_OMR:
            rega = (raw[1] & 0x0F) >> 0;
            regb = (raw[1] & 0xF0) >> 4;
            *size = 2;
            break;
            
        case OP_FMT_OI:
            *size = 3;
            imm = raw[1] | (((uint16_t)raw[2]) << 8);
            *size = 3;
            break;
            
        case OP_FMT_ORI:
            rega = (raw[1] & 0x0F) >> 0;
            imm = raw[2] | (((uint16_t)raw[3]) << 8);
            *size = 4;
            break;
            
        case OP_FMT_OMI:
            rega = (raw[1] & 0x0F) >> 0;
            imm = raw[2] | (((uint16_t)raw[3]) << 8);
            *size = 4;
            break;
            
        default:
            // should not be possible
            return false;
            break;
    }
    
    if (Validate() == false) { return false; }
    
    return true;
}


bool Instruction::ToAssemblyText(
    char* buffer)
{
    if (Validate() == false)
    {
        buffer[0] = '\0';
        return false;
    }
    
    std::string text;
    
    text += OP_NAMES[operation];
    
    switch (operand_format)
    {
        case OP_FMT_O:
            break;
            
        case OP_FMT_OR:
            text += OP_NAMES_SPACES[operation];
            text += REG_NAMES[rega];
            break;
            
        case OP_FMT_ORR:
            text += OP_NAMES_SPACES[operation];
            text += REG_NAMES[rega];
            text += ", ";
            text += REG_NAMES[regb];
            break;
            
        case OP_FMT_ORM:
            text += OP_NAMES_SPACES[operation];
            text += REG_NAMES[rega];
            text += ", [";
            text += REG_NAMES[regb];
            text += "]";
            break;
            
        case OP_FMT_OMR:
            text += OP_NAMES_SPACES[operation];
            text += "[";
            text += REG_NAMES[rega];
            text += "], ";
            text += REG_NAMES[regb];
            break;
            
        case OP_FMT_OI:
            text += OP_NAMES_SPACES[operation];
            text += std::to_string(imm);
            break;
            
        case OP_FMT_ORI:
            text += OP_NAMES_SPACES[operation];
            text += REG_NAMES[rega];
            text += ", ";
            text += std::to_string(imm);
            break;
            
        case OP_FMT_OMI:
            text += OP_NAMES_SPACES[operation];
            text += "[";
            text += REG_NAMES[rega];
            text += "], ";
            text += std::to_string(imm);
            break;
            
        default:
            // should never be possible
            return false;
            break;
    }
    
    strcpy(buffer, text.c_str());
    return true;
}