# Program Structure

A VSVM program has a **header** and one or more **sections** (which can be either "CODE" or "DATA"). Each section consists of a **section header** and the actual data that gets loaded into VSVM memory.

For a VSVM program with `N` sections, the high-level structure will look like this:
```
==> program header
==> section[0]
  ==> section header
  ==> data
==> section[1]
  ==> section header
  ==> data
==> section[N-1]
  ==> section header
  ==> data
(...)
```

Header structure:
```C
#define MAGIC 0x4D565356 // "VSVM"

typedef struct ProgramHeader
{
    uint32_t    magic;
    uint16_t    version_major;
    uint16_t    version_minor;
    uint32_t    num_sections;
    uint32_t    file_size;
    uint32_t    crc32;
} ProgramHeader;
```

Section header structure:
```C
#define SECTION_TYPE_CODE   0x0000
#define SECTION_TYPE_DATA   0x0001

typedef struct SectionHeader
{
    uint16_t    section_type;
    uint16_t    data_size;
} SectionHeader;
```
