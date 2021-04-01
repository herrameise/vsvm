.PHONY : all

OBJS= \
	Error.o \
	Instruction.o \
	Machine.o \
	Names.o \
	Opcodes.o \
	Processor.o

all : $(OBJS)

%.o : %.cpp
	$(CXX) $< -c -fPIC $(CXXFLAGS) -o $@

clean :
	-rm -f *.o
