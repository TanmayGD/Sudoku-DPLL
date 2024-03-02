def generate_clauses(lis):
    cnf_lines = []
    for i in lis: # Adding the assigned elements to the clauses
        j = i.split(" ")
        for k in j:
            spl = k.split("=")
            cnf_lines.append(["n" + spl[1] + "_r" + spl[0][0] + "_c" + spl[0][1]])
    
    helper(cnf_lines)

    return cnf_lines


def helper(cnf_lines): # Generating all the common rules for sudoku
    for r in range(1, 10):
        for c in range(1, 10):
            for n in range(1, 10):
                
                for temp_n in range(n + 1, 10):
                    cnf_lines.append(["!n" + str(n) + "_r" + str(r) + "_c" + str(c), "!n" + str(temp_n) + "_r" + str(r) + "_c" + str(c)])
                for temp_c in range(c + 1, 10):
                    cnf_lines.append(["!n" + str(n) + "_r" + str(r) + "_c" + str(c), "!n" + str(n) + "_r" + str(r) + "_c" + str(temp_c)])
                for temp_r in range(r + 1, 10):
                    cnf_lines.append(["!n" + str(n) + "_r" + str(r) + "_c" + str(c), "!n" + str(n) + "_r" + str(temp_r) + "_c" + str(c)])

                
                min_r = 1 if r / 3 <= 1 else (4 if r / 3 <= 2 else 7)
                min_c = 1 if c / 3 <= 1 else (4 if c / 3 <= 2 else 7)

                for i in range(min_r, min_r + 3):
                    for j in range(min_c, min_c + 3):
                        if i != r and j != c:
                            cnf_lines.append(["!n" + str(n) + "_r" + str(r) + "_c" + str(c), "!n" + str(n) + "_r" + str(i) + "_c" + str(j)])

            check = []
            for i in range(1, 10):
                check.append("n" + str(i) + "_r" + str(r) + "_c" + str(c))
            cnf_lines.append(check)

    return cnf_lines

def get_dictionary(clauses): 
    
    dic = {}
    
    for i in clauses:
            for j in i:
                if "!" in j: # Iterating through all the clauses and populating the dictionary
                    if j[1:] in dic.keys():
                        dic[j[1:]][1] += 1
                    else:
                        dic[j[1:]] = [0,1]
                else:
                    if j in dic.keys():
                        dic[j][0] += 1
                    else:
                        dic[j] = [1,0]

    return dic