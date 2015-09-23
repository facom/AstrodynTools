num=$1
rm ./cvers$num
gcc -g -c -o x1.o bs$num.c
gcc -g -o cvers$num test_bs$num.c x1.o -lm
rm x1.o
