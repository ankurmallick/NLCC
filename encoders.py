#Encoders for different coded computing schemes

import numpy as np

def RS(m,c=0.03,delta=0.5):
    
    #Returns Robust Soliton CDF for given parameters
    
    S=c*np.log(m/delta)*np.sqrt(m)
    rho=0.0
    tau=0.0
    r=round(m/S)
    u=np.zeros((1,m))
    
    for d_iter in range(m):
        d=float(d_iter+1)
        if d==1:
            rho=1/float(m)
        else:
            rho=1/(d*(d-1))
        if d>=1 and d<r:
            tau=1/(d*r)
        elif d==r:
            tau=np.log(S/delta)/r
        else:
            tau=0
        u[0][d_iter]=tau+rho
        
    u=u/np.sum(u)
    return np.ravel(u)

def sr_enc(p=1000,d=10):
    
    enc_all = []
    
    for i in range(p):
        
        #Encoded symbols at ith worker
        
        ind_vect = np.delete(np.arange(p),i)
        np.random.shuffle(ind_vect)
        ind_vect.tolist()
        enc_i = []
        
        for ctr in range(0,p,d):
            
            if ctr == 0:
                enc_i.append([i])
            else:
                start_pos = ctr - d
                end_pos = min(ctr,p-1)
                enc_i.append(ind_vect[start_pos:end_pos])
        
        enc_all.append(enc_i)
        
    return enc_all

def lt_enc(p=1000,d=10):
    
    #d-LT for p workers
    
    num = p//d
    
    u = RS(p)
    
    enc_all = []
    
    for i in range(p):
        
        #Encoded symbols at ith worker
        
        degs = 1+np.random.choice(p, size=num, replace=True, p=u) #Degree chosen according to RS distributions
        enc_i = []
        
        for j in range(num):
            
            #jth encoded symbol
            
            enc_sym = np.random.choice(p, size=degs[j], replace=False, p=None)
            enc_i.append(enc_sym.tolist())
        
        enc_all.append(enc_i)
            
    return enc_all

def bcc_enc(p=1000,d=10):
    
    #d-bcc for p workers
    
    enc_all = []
    
    for i in range(p):
        
        #Encoded symbol at ith worker
        
        j = np.random.randint(d)
        enc_i = [list(range(d*j,d*(j+1)))] #one symbol per worker        
        enc_all.append(enc_i)
    
    return enc_all
    

def rep_enc(p=1000,d=10):
    
    #d-rep for p workers
    
    enc_all = []
    
    for i in range(p):
        
        #Encoded symbol at ith worker
        
        j = i%d
        enc_i = [list(range(d*j,d*(j+1)))] #one symbol per worker        
        enc_all.append(enc_i)
    
    return enc_all
    
