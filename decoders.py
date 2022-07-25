#Decoders for different coded computing schemes

import numpy as np
from scipy.sparse import csr_matrix

def sr_dec(dec_list,num_funcs):
    
    #dec_list contains the indices for each encoded symbol in order of arrival
    
    b = np.ones((num_funcs,1))
    
    A_list = []
    
    for (i,dec_sym) in enumerate(dec_list):
        
        a = np.zeros(num_funcs)
        a[dec_sym] = 1
        A_list.append(a)
        
        A = np.stack(A_list).T
        
        if np.linalg.matrix_rank(A) == np.linalg.matrix_rank(np.concatenate([A,b],1)):
            
            return i
    
    return -1

def lt_dec(dec_list,num_funcs):
    
    #dec_list contains the indices for each encoded symbol in order of arrival
    
    dec_num = 0
    dec_set = set()
    neighbours = {}
    visited = []
    
    for (i,dec_sym) in enumerate(dec_list):
        
        proc_sym = set([ind for ind in dec_sym if ind not in dec_set]) #Remove decoded symbols
        visited.append(proc_sym)
        
        if len(proc_sym) == 0:
            continue #No useful information
        
        for node in proc_sym:
            
            #Updating neighbours
            if node in neighbours:
                neighbours[node].append(i)
            else:
                neighbours[node] = [i]
        
        if len(proc_sym) == 1:
            
            #New degree 1 symbol
            ripple_node = proc_sym.pop()
            ripple = [ripple_node]
            
            while ripple:
                
                node = ripple.pop()
                
                if node in dec_set:
                    #Already processed
                    continue
                
                #Decode degree 1 symbol
                dec_set.add(node)
                dec_num += 1
                if dec_num == num_funcs:
                    return i
                
                
                for prev_ind in neighbours[node]:
                    
                    #Process neighbours
                    if node in visited[prev_ind]:
                        visited[prev_ind].remove(node)
                        if len(visited[prev_ind]) == 1:
                            new_node = visited[prev_ind].pop()
                            ripple.append(new_node)
    
    return -1
    
def bcc_dec(dec_list,num_funcs):
    
    #dec_list contains the indices for each encoded symbol in order of arrival
    
    ind_set = set()
    
    for (i,dec_sym) in enumerate(dec_list):
        
        for j in dec_sym:
            ind_set.add(j)
        
#         print (len(ind_set))
            
        if len(ind_set) == num_funcs:
            return i
    
    return -1
    
def rep_dec(dec_list,num_funcs):
    
    #dec_list contains the indices for each encoded symbol in order of arrival
    
    ind_set = set()
    
    for (i,dec_sym) in enumerate(dec_list):
        
        for j in dec_sym:
            ind_set.add(j)
            
        if len(ind_set) == num_funcs:
            return i
    
    return -1
    

