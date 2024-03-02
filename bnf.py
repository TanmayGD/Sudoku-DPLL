import copy
import re

def bidirectionals(clause):
    if "<=>" not in clause:
        return clause

    idx = clause.find("<=>")

    flag = 0
    i = idx - 1
    j = idx + 1 
    
    while ( i >= 0 ):
        x = clause[i]

        if x == '(':
            if flag == 0:
                break
            else:
                flag -= 1
        else:
            if x == ')':
                flag += 1
        i = i - 1
    
    while ( j < len(clause) ):
        x = clause[j]

        if x == ')':
            if flag == 0:
                break
            else:
                flag -= 1
        else:
            if x == '(':
                flag += 1
        j = j + 1
        
        
    left = clause[i+1:idx]
    right = clause[idx+3:j]

    clause = clause[0:i+1] + "(" + left + "=>" + right + ")" + "^" + "(" + right + "=>" + left + ")" + clause[j:len(clause)] 

    return bidirectionals(clause)
    
def implications(clause):
    if "=>" not in clause:
        return clause

    idx = clause.find("=>")

    flag = 0
    i = idx - 1
    j = idx + 1 
    
    while ( i >= 0 ):
        x = clause[i]

        if x == '(':
            if flag == 0:
                break
            else:
                flag -= 1
        else:
            if x == ')':
                flag += 1
        i = i - 1
    
    while ( j < len(clause) ):
        x = clause[j]

        if x == ')':
            if flag == 0:
                break
            else:
                flag -= 1
        else:
            if x == '(':
                flag += 1
        j = j + 1
        
        
    left = clause[i+1:idx]
    right = clause[idx+2:j]

    #print("left is", left)
    if len(left) <=2 or left[-1] == ")":
        clause = clause[0:i+1] + "!" + left  + "v" + right + clause[j:len(clause)] 
    else:
        clause = clause[0:i+1] + "!" + "(" + left  + ")" +"v" + right + clause[j:len(clause)]
    return implications(clause)

def negations(clause):
    if "!(" not in clause:
        return clause

    flag, lis, sym = 0, [], 0
    idx = clause.find("!(")
    
    temp = copy.deepcopy(clause)

    i = idx + 2
    while ( i < len(clause) ):
        x = copy.deepcopy(clause[i])

        if x == ')':
            if flag == 0:
                break
            else:
                flag -= 1
        else:
            if x == '(':
                if flag == 0:
                    lis.append(i)
                flag += 1
            else:
                if flag == 0:
                    if ( x.isnumeric() or x == "_" or x.isupper()) and sym == 0:
                        lis.append(i)
                        sym = 1
                    else:
                        if x == "v":
                            clause = clause[:i] + "^" + clause[i + 1:]
                        else:
                            if x == "^":
                                clause = clause[:i] + "v" + clause[i + 1:]
                            else:
                                if x == "!":
                                    lis.append(-i)
                                    i = i + 1
                        sym = 0
        i = i + 1
    
    # clause = clause[:i] + clause[i + 1:]

    j = 0
    for p in range(0,len(lis)):
        
        if lis[p] >= 0:
            lis[p] = lis[p] + j
            j += 1
        else:
            lis[p] = lis[p] - j
            j -= 1

    for p in lis:
        if p >= 0:
            clause = clause[:p] + "!" + clause[p:]
        else:
            clause = clause[:abs(p)] + clause[abs(p)+1:]

    clause = clause[:idx] + clause[idx + 1:]

    return negations(clause)

def distribute(clause):
    if clause.count("(") == 1 and clause.count(")") == 1:
        return clause[1:len(clause)-1]

    
    flag, lis, lis1 = 0, [], []
    #i = idx - 1
    offset = 0

    while(1):
        
            
        idx = clause.find("v",offset)

        if idx == -1:
            return clause

        print("idx is", idx)
        print("len is", len(clause))

        
        offset = idx + 1

        flag, lis, lis1 = 0, [], []
        i = idx - 1
        diff_flag = 0

        while ( i >= 0 ):
            x = clause[i]
            
            if x == '(':
                if flag == 0:
                    break
                else:
                    flag -= 1
            else:
                if x == ')':
                    flag += 1
                    if  diff_flag ==1:
                        break
                else:
                    if x == "^":
                        if flag == 1:
                            lis.append(i)
                        else:
                            if flag == 0:
                                break
            i = i - 1
        
        j = idx + 1
        flag = 0
        diff_flag = 0

        while ( j < len(clause) ):
            x = clause[j]

            if x == ')':
                if flag == 0 or diff_flag == 1:
                    break
                else:
                    flag -= 1
            else:
                if x == '(':
                    flag += 1
                else:
                    if x == "^" and flag == 1:
                        lis1.append(i)
                        diff_flag += 1
                    else:
                        if x == "v" and flag == 0:
                            print("blah"+str(j))
                            break
            j = j + 1

        if len(lis1) == 0 and len(lis) == 0:
            print("i is"+clause[i]+"at"+ str(i))
            continue
        else:
            break

    if i < 0:
        i = 0
    if j > len(clause):
        j += 1

    print("i " + str(i))
    print("idx " + str(idx))
    print("j " + str(j))
    print("lis " + str(len(lis)))
    print("lis1 " + str(len(lis1)))

    if len(lis1) > 0:
        temp = copy.deepcopy(idx)
        temp1 = copy.deepcopy(i)

        while (1):
            if ( clause[temp].isnumeric() or clause[temp] == "_" or clause[temp].isupper() or clause[temp] =="!"):
                break
            else:
                temp = temp - 1

        while (1):
            if ( clause[temp1].isnumeric() or clause[temp1] == "_" or clause[temp1].isupper() or clause[temp1] =="!" ):
                break
            else:
                temp1 = temp1 + 1

        left = clause[temp1:temp+1]
        temp3 = copy.deepcopy(idx)
        temp4 = copy.deepcopy(j)

        while (1):
            if ( clause[temp3].isnumeric() or clause[temp3] == "_" or clause[temp3].isupper() or clause[temp3] =="!"):
                break
            else:
                temp3 = temp3 + 1

        while (1):
            if ( clause[temp4].isnumeric() or clause[temp4] == "_" or clause[temp4].isupper() or clause[temp4] =="!" ):
                break
            else:
                temp4 = temp4 - 1

        right = clause[temp3:temp4+1]

        print("left " + left)
        print("right " + right)


        
        if "^" in right:
            a = right.split("^")[0]
            b = right.split("^")[1]
            if len(left) <=2:
                clause = clause[:i+1] +  "("+ a + "v" +  left + "^" +  b + "v" +  left+ ")"  + clause[j+1:]
            else:
                clause = clause[:i+1] +  "("+  a + "v" +"("+ left + ")" + "^" +  b  + "v" +"("+ left +  ")"+ ")" + clause[j+1:]

    #return distribute(clause)

    

    if match:
        # print("Match found:", match)
        # print(" the string version is", match.group())
        for k in range(1,4):
            # break
            if match.group(k):
                tem.append(match.group(k))
        
        clause = clause.replace(match.group(), "("+ tem[2] + "v" +  tem[0] + "^" +  tem[1] + "v" +  tem[0]+ ")" )
        tem = []
        print(clause)
        if line == "!A v (C ^ E) v (!B => !D)":
            match = re.search(right, clause)
            for k in range(1,4):
                print(match.group(k))
                if match.group(k):
                    tem.append(match.group(k))
    
            print(tem)

            clause = clause.replace(match.group(), "("+ tem[2] + "v" +  tem[0] + "^" +  tem[1] + "v" +  tem[2]+ ")" )
            clause = clause.replace("(","")
            clause = clause.replace(")","")
            clause = clause.split("^")

        print(clause)
    else:
        print("No match found.")


    return clause


def dis(clause):

    # right = r'\(+([!A-Za-z_]+)\)*\(*\^([!A-Za-z_]+)\)+v\(*([!A-Za-z_^]+)\)*' 
    # left = r'\(*([!A-Za-z_^]+)\)*v\(([!A-Za-z_]+)\)*\(*\^([!A-Z_]+)\)'

    right = r'\(([!A-Za-z_\^]+)\){0,1}\^\({0,1}([!A-Za-z_\^]+)\)+v\({0,1}([!A-Za-z_\^]+)\){0,1}' 
    left = r'\({0,1}([!A-Za-z_\^]+)\){0,1}v\(+([!A-Za-z_\^]+)\)*\^\(*([!A-Za-z_\^]+)\)'


    left_match = re.search(left, clause)

    right_match = re.search(right, clause)
    flag = 0
    y = 0
    j=0
    if left_match:
        check = left_match.group(0)
        print(check)
        for y in range(0,len(check)):
            if check[y] == "(":
                continue
            else:
                break
        for j in range(len(check)-1,-1):
            if check[j] == "(":
                continue
            else:
                break
        print(check[y:j].count("(")-check[y:j].count(")"))
        count = check[y:j].count("(")-check[y:j].count(")")
        if count < 0:
            flag = 1


    if left_match and flag == 0:
        tem = []
        
        # count = left_match.count("(")-left_match.count(")")
        # if count>0:
        #     left_match = left_match[count:]
        # else:
        #     left_match = left_match[:-count]

        for k in range(0,4):
            if left_match.group(k):
                print(left_match.group(k))
                if "^" in left_match.group(k) and k > 0 and left_match.group(k)[0] != "^":
                    tem.append("("+ left_match.group(k) +")")
                else:
                    tem.append(left_match.group(k))

        
    
        
        # if len(tem[0]) <= 2 and "^" in tem[0]:
        #     tem[0] = tem[0].replace("^","")
        #     other = left_match.group().replace("^","",1)

        # if tem[0][0] == "^" or tem[0][0] == "v":
        #     tem[0] = tem[0][1:]
        #     tem[1] = tem[1][1:]

        count = tem[0].count("(")-tem[0].count(")")
        print(tem)
        print(count)
        if count>0:
            tem[0] = tem[0][count:]
        else:
            tem[0] = tem[0][:count]

        print(tem)
        # if "^" in tem[1]:
        #     print("here")
        #     clause = clause.replace(tem[0], "("+ tem[3] + "v" + "(" + tem[1] + ")" + "^" +  tem[2] + "v" + "(" + tem[1] + ")"  + ")" )

        clause = clause.replace(tem[0],  tem[3] + "v" +  tem[1] + "^" +  tem[2] + "v" +  tem[1] )

        print( "The left replacement string is ",tem[0] )
        print( "The new string is ",clause )

        return dis(clause)
    else:
        if right_match:
            tem = []

            check = left_match

            # count = left_match.count("(")-left_match.count(")")
            # if count>0:
            #     left_match = left_match[count:]
            # else:
            #     left_match = left_match[:-count]


            for k in range(0,4):
                if "^" in right_match.group(k) and k > 0:
                    tem.append("("+ right_match.group(k) +")")
                else:
                    tem.append(right_match.group(k))

            if tem[0][-1] == "^" or tem[0][-1] == "v":
                tem[0] = tem[0][0:len(tem[0])-1]
                tem[3] = tem[3][0:len(tem[0])-1]

            count = tem[0].count("(")-tem[0].count(")")
            print(tem)
            print(count)
            if count>0:
                tem[0] = tem[0][count:]
            else:
                tem[0] = tem[0][:count]

            clause = clause.replace(tem[0], "("+ tem[3] + "v" +  tem[1] + "^" +  tem[3] + "v" +  tem[2]+ ")" )

            # if "^" in tem[3] or "^" in tem[2]:
            #     print("here")
            #     clause = clause.replace(tem[0],"(" +  "(" + tem[1] + ")" + tem[] + "(" + tem[] + ")" + tem[]  + ")" )

            # print( "The right replacement string is ",right_match.group() )
            # print( "The new string is ",clause )

            return clause
        else:
            return clause


    

def driver(lines):
    for line in lines:
        if line.count('(') != line.count(')'):
            scenebhai

    clause = clause.replace(" ","")


# clause = "!(A v !B) <=> (!C => D) ^ E"
# clause = clause.replace(" ","")
# clause = bidirectionals(clause)
# print(clause)
# clause = implications(clause)
# print(clause)
# clause = clause.replace("!!","")
# print(clause)
# print(distribute(negations(clause)))

# clause = "(A <=> C) => D"
# clause = clause.replace(" ","")
# clause = bidirectionals(clause)
# print(clause)
# clause = implications(clause)
# print(clause)
# clause = clause.replace("!!","")
# print(clause)
# clause = negations(clause)
# print(clause)
# clause = distribute(clause)
# print(clause)
# clause = distribute(clause)
# print(clause)
# clause = distribute(clause)
# print(clause)
# clause = distribute(clause)
# print(clause)

# clause = "!A v (C ^ E) v (!B => !D)"
# clause = clause.replace(" ","")
# clause = bidirectionals(clause)
# print(clause)
# clause = implications(clause)
# print(clause)
# clause = clause.replace("!!","")
# print(clause)
# clause = distribute(negations(clause))
# print(clause)
# clause = distribute(clause)
# print(clause)
#lines = ["!(A v !B) <=> (!C => D) ^ E","(A <=> C) => D","!A v (C ^ E) v (!B => !D)","A => !B"]
lines= ["!(A v !B) <=> (!C => D) ^ E"]
for line in lines:
    print(line)
    clause = line.replace(" ","")
    clause = bidirectionals(clause)
    print(clause)
    clause = implications(clause)
    print(clause)
    clause = clause.replace("!!","")
    print(clause)
    clause = negations(clause)
    print(clause)
    clause = dis(clause)
    clause = clause.replace("(","")
    clause = clause.replace(")","")
    clause = clause.split("^")
    print(clause)
    for j in clause:
        temp = j.split("v")
        print(temp)


    # right = r'\([!A-Z_]+^[!A-Z_]+\)+v[A-Z_]+'
    
    ' \( [A-Za-z_]+\^[A-Za-z_]+ \)v[A-Za-z_]+ v[!A-Za-z_]       |[\(\)!A-Za-z]+v[\(\)!A-Za-z]+\^[\(\)!A-Za-z]+' 

    # Using re.search() to find a match

    
    