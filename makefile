CPP=g++
CFLAGS=-I. -w
LFLAGS=-lm

clean:
	@echo "Cleaning..."
	@find . -name "*~" -exec rm -rf {} \;
	@rm -rf *.pyc *.out *.exe

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

commit:
	@echo "Commiting..."
	@git commit -am "Commit"
	@git push origin master
