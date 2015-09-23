#  Test the Bulirsch_Stoer method in the file bulirsch_stoer.c
#
#  Dependent on: (no external dependencies)
#
#  After downloading change permissions: chmod 744 test_Bulirsch_Stoer.sh
#  Execute as ./test_Bulirsch_Stoer.sh (unless your profile has a PATH set to
#                                       this directory)
#
#
# Change! if bulirsch_stoer.c is in a different directory.
gcc -g -c -o x1.o bulirsch_stoer.c

# Change! if test_Bulirsch_Stoer.c is in a different directory.
gcc -g -o cvers1 test_Bulirsch_Stoer_met.c x1.o -lm 

# Change! if you profile has a PATH set to this directory.
time ./cvers1 $1

# Delete temporary files.
rm x1.o
