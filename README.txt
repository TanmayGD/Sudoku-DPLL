Author: Tanmay Gopaldas Dadhania

The python file should run with any system having python 3:

Example of how to runs:

1) python lab2.py 11=4 12=5 23=2 25=7 27=6 28=3 38=2 39=8 44=9 45=5 52=8 53=6 57=2 62=2 64=6 67=7 68=5 77=4 78=7 79=6 82=7 85=4 86=5 93=8 96=6 

2) python lab2.py 11=9 14=6 15=7 16=2 21=2 26=1 27=4 39=8 44=1 51=7 52=4 54=3 55=9 58=8 63=6 66=4 78=2 79=9 89=1 91=5 92=6 93=1 97=7 -r

The following arguments are accepted:
IMPORTANT: Order of these arguments does not matter 

Required command line arguments:
1. python lab2.py are required
2. 1+ assignments of sudoku board are required.

Optional command line arguments:
1. "-v" - Gives a verbose DPLL solution along with the answer
2. IMPORTANT "-r" - Solves the sudoku board by random DPLL assignments, this mode was made for the expert and hard inputs. Without this flag the program in it's normal operation make smallest lexographical guess but this causes the program to take 2-3 hours to run the expert and hard inputs. That is I created a random flag that makes random guesses to hasten the process to finish the processing in sub 30 seconds. In the case of the medium input the default program takes about 25 seconds to work.
