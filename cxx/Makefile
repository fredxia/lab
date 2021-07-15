#-*- mode: makefile -*-
HDRS = 
SRC = cpp_features.cc
OBJS = $(SRCS:.cc=.o)

CXXFLAGS = -g -std=c++0x -Wall
CFLAGS = -g -Wall

%.o : %.cc $(HDRS)
	g++ $(CXXFLAGS) -c $<

cpp_features : cpp_features.o
	g++ -o $@ $^

clean :
	rm -f *.o cpp_features
