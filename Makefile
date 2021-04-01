.PHONY : all install uninstall clean

CXX=g++
CXXFLAGS=-Wall -O2 -std=c++11

export CXX
export CXXFLAGS

all : 
	mkdir -p bin
	$(MAKE) -C src

clean :
	$(MAKE) -C src clean
