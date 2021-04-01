.PHONY: all clean

TARGET=../bin/vsvm

OBJS= \
	main.o \
	Tests.o

all : $(TARGET)

$(TARGET) : $(OBJS)
	make -C common
	$(CXX) *.o common/*.o $(CXXFLAGS) -o $(TARGET)
	
%.o : %.cpp
	$(CXX) $< -c -fPIC $(CXXFLAGS) -o $@

clean :
	make -C common clean
	-rm -f *.o
	-rm -f $(TARGET)
