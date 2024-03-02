import sys
import re
import input_helper
import dpll

def output(ans):

    if ans == 0:
        print("NO VALID ASSIGNMENTS")

    out = {}

    for i in ans:
        if "true" in i: # Creating a dictionary to convert the output in grid format
            value = i.split("_")[0].replace("n","")
            row = i.split("_")[1].split("_")[0].replace("r","") 
            column = i.split("_")[2].split("=")[0].replace("c","")
            if row in out:
                temp = out[row]
                scene = [column,value]
                temp.append(scene)
            else:
                out[row] = [[column,value]]

    temp = []

    for k in out: # Sorting these rows to print columns in order
        temp = out[k]
        temp.sort(key= lambda x:x[0])
        
    for i in range(1,10): # Iterating the dictionary to print the sudoku
        p = str(i)
        for j in range(0,9):
            print(out[p][j][1]+" ",end="")
        print("")

def main():

    if len(sys.argv) < 2:
        print("Insufficient number of arguements provided.")
        sys.exit(1)

    i = 1

    verbose_flag = False
    file_name = ""
    initial_list = []
    bnf_flag = False
    random_flag = False
    train_file = None

    while (i<len(sys.argv)): # Using flags to understand command line inputs
        if sys.argv[i] == "-v":  
            verbose_flag = True
        else:
            if sys.argv[i] == "-bnf":
                try:
                    re.search("\.",sys.argv[i+1])
                except:    
                    print("Error handling arguments")
                    exit(1)
                else:
                    if re.search("\.",sys.argv[i+1]):
                        train_file = sys.argv[i+1]
                        i = i + 1
                    else:
                        print("Wrong filename for training")
                        exit(1)
            else:
                if "=" in sys.argv[i]:
                    initial_list.append(sys.argv[i])
                else:
                    if sys.argv[i] == "-r":
                        random_flag = True
                    else:
                        print("Invalid Input")
                        exit(1)
        i = i + 1
    
    ans = []

    if len(initial_list) == 0:
        print("No assignements provided")
        exit(1)

    if bnf_flag == False:
        clauses = input_helper.generate_clauses(initial_list) # Using the initial assingments to generate all the clauses
    else:
        clauses = 
    dic = input_helper.get_dictionary(clauses) # Creating a dictionary to keep track of all the literals

    print(len(clauses))

    dpll.singleton(clauses,dic,ans,verbose_flag)

    #dpll.true_literal(clauses,dic,ans,verbose_flag)

    #print(len(clauses))



    output(dpll.dpll_helper(clauses,dic,ans,verbose_flag,random_flag)) # Running algorithms and printing the output
            
if __name__ == "__main__":
    main()