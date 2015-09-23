UTILDIR=../util
CPP=g++
CC=gcc
CFLAGS=-I. -w -I$(UTILDIR)/include -I$(UTILDIR)/include/gsl
#LFLAGS=-lm $(UTILDIR)/lib/novas.a $(UTILDIR)/lib/cspice.a $(UTILDIR)/lib/csupport.a $(UTILDIR)/lib/libgsl.a $(UTILDIR)/lib/libgslcblas.a 
LFLAGS=-lm $(UTILDIR)/lib/cspice.a $(UTILDIR)/lib/csupport.a -L $(UTILDIR) -lgsl -lgslcblas

clean:
	@echo "Cleaning..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "#" -exec rm -rf {} \;
	@rm -rf *.pyc *.out *.exe *.png

%.exe:%.opp
	$(CPP) $^ $(LFLAGS) -o $@

%.opp:%.cpp
	$(CPP) -c $(CFLAGS) $^ -o $@

%.out:%.o
	$(CC) $^ $(LFLAGS) -o $@

%.o:%.c
	$(CC) -c $(CFLAGS) $^ -o $@

