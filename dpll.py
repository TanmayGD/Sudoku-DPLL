import copy

def singleton(clauses,dic,ans, verbose_flag):
    
    idx = -1

    for i in clauses:   
        if len(i) == 1: # Flaging a singleton by checking for a clause with a single element
            if  verbose_flag:
                print("easy case: singleton "+i[0]) 
            idx = i   
            break     

    if idx == -1:
        return 
    else:
        propagate(clauses,idx[0],dic)
            
        if "!" in idx[0]:
            ans.append(idx[0][1:]+"= false")
            dic.pop(idx[0][1:])
        else:
            ans.append(idx[0]+"= true")
            dic.pop(idx[0])
            
        singleton(clauses,dic,ans, verbose_flag)

def true_literal(clauses,dic,ans, verbose_flag):
    
    idx = -1
    flag = -1
    for i in dic:
        if dic[i][0] == 0: # Flaging a true by checking for entry in the dictionary that has a 0
            if  verbose_flag: 
                print("easy case: true literal "+i+" = false ")   
            idx = i 
            flag = 1  
            break
        else:
            if i[1] == 0:   
                if verbose_flag:
                    print("easy case: true literal "+i+" = true ")
                idx = i
                flag = 1   
                break     

    if idx == -1:
        return 
    else:
        if flag == 1:     
            propagate(clauses,"!"+idx,dic)
            
            ans.append(idx[0][1:]+"= false")
            dic.pop(idx)
            
            true_literal(clauses,dic,ans,verbose_flag)
        
        else:

            propagate(clauses,idx,dic)

            ans.append(idx[0]+"= true")
            dic.pop(idx)
            
            true_literal(clauses,dic,ans,verbose_flag)
        
def propagate(lis, literal,dic):

    if "!" in literal: # creating the negated literal
        neg_literal = literal[1:]
    else:
        neg_literal = "!"+literal 

    idx = -1
    flag = -1

    for p in range(0,len(lis)): # finding a instance of a negated literal or a literal
        if literal in lis[p]:
            idx = p
            flag = 1
            break
        else:
            if neg_literal in lis[p]:
                idx = p
                flag = 0
                break

    if idx == -1:
        return
    
    else:
        if flag == 1:
            for j in lis[idx]:
                if "!" in j: # updating the dictionary
                    dic[j[1:]][1] -= 1
                else:
                    dic[j][0] -= 1
            
            lis.pop(idx) # updating clauses
            propagate(lis,literal,dic)
        else:
            if "!" in neg_literal: # updating the dictionary
                dic[neg_literal[1:]][1] -= 1
            else:
                dic[neg_literal][0] -= 1
            lis[idx].remove(neg_literal) # updating the line with the negated literal
            propagate(lis,literal,dic)


def dpll_helper(lis, dic,ans,verbose_flag,random_flag):

    singleton(lis,dic,ans,verbose_flag) # solving for easy cases first

    true_literal(lis,dic,ans,verbose_flag)

    if len(lis) == 0: # checking for exit condition
        return ans
    
    for k in lis: # checking for failure case
        if len(k) == 0:
            if not verbose_flag:
                print("Contradiction! Backtracking!")
            return 0

    if not random_flag: 
        literal = min(dic)
    else:
        for b in dic:
            literal = b
            break

    new_list = copy.deepcopy(lis)
    new_ans =  copy.deepcopy(ans)
    new_dic =  copy.deepcopy(dic)

    propagate(new_list,literal,new_dic)
    if not verbose_flag:
        print("hard case: "+literal+" = true ")
    new_ans.append(literal+"= true")
    new_dic.pop(literal)

    temp = dpll_helper(new_list,new_dic,new_ans,verbose_flag,random_flag)

    if temp == 0:
        
        new_list = copy.deepcopy(lis)
        new_ans =  copy.deepcopy(ans)
        new_dic =  copy.deepcopy(dic)

        propagate(new_list,"!"+literal,new_dic)
        new_ans.append("!"+literal+"= false") # If recursion returns false then guessing false for the literal
        if not verbose_flag:
            print("hard case: "+literal+" = false ")
        new_dic.pop(literal)

        return dpll_helper(new_list,new_dic,new_ans,verbose_flag,random_flag)

    else:
        return temp
