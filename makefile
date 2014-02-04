CPP=g++
CFLAGS=-I. -w
LFLAGS=-lm

clean:
	@echo "Cleaning..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "#" -exec rm -rf {} \;
	@rm -rf *.pyc *.out *.exe

reset:
	@echo "Reseting directory..."
	@rm -rf MercuPy
	@make -C util reset

%.exe:%.opp
	$(CPP) $(LFLAGS) $^ -o $@

%.opp:%.cpp .constants
	$(CPP) -c $(CFLAGS) $^ -o $@

%.out:%.o
	$(CC) $(LFLAGS) $^ -o $@

%.o:%.c .constants
	$(CC) -c $(CFLAGS) $^ -o $@

.constants:constants.py
	@bash .constants.sh

install:
	@echo "Installing components..."
	@bash -x .install.sh

installadmin:
	@echo "Installing components..."
	@bash .install.sh admin

commit:
	@echo "Commiting..."
	@git commit -am "Commit"
	@git push origin master
