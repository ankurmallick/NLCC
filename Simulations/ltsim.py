import numpy as np
import matplotlib.pyplot as plt
import time
plt.style.use('publication')

num_rep = 2
exp_rate = 0.2
comp_time = 0.005

def RS(m,c,delta):
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
    return u

def encoder(A,x,u):
    #Generates a single encoded symbol
    m=A.shape[0] #Number of rows
    d=1+np.random.choice(m, size=None, replace=True, p=u) #Degree
    rows=np.random.choice(m, size=d, replace=False, p=None)
    Ae_current=np.sum(A[rows,:],axis=0)
    be_current=Ae_current.dot(x)
    return [d, rows.tolist(), be_current]

def decoder(be,encrows,numrows,rowslist):
    #Decodes a single row at a time
    pos=numrows.index(1) #Target encoding position
    r=encrows[pos][0] #Target source position
    bd_current=be[pos] #Target source symbol
    numrows[pos]-=1 #Removing link
    for j in rowslist[r]:
        #For all encoded symbols connected to source symbol
        try:
            encrows[j].remove(r) #Remove link
        except:
            print (j)
            print (r)
            print (rowslist[r])
            print (encrows[j])
            raise
        numrows[j]-=1 #Reduce degree
        be[j]=be[j]-bd_current #Update encoded symbol
    return (r,bd_current)

def fcrunner(A,x,c,delta,u):
    b=A.dot(x)
    m=A.shape[0]
    decrows=np.zeros(m) #keeps a track of decoded rows
    bd=np.zeros(m)
    decnum=0
    be=[] #list of encoded symbols
    encrows=[] #list of rows corresponding to each encoded symbol
    numrows=[] #degree of each encoded symbol
    rowslist = [[] for _ in range(m)]
    k=0
    encnum=0 #Includes redundant encoded symbols as well
    encnum_list=[]
    decnum_list=[]
    encop_list = [encoder(A,x,u) for _ in range(2*m)]
    degrees_mat = np.asarray([encop[0] for encop in encop_list]).reshape((m,2))
    if m == 500:
        degrees_mat *= num_rep
    # setup_time = np.random.exponential(scale=1/exp_rate,size=m).reshape((-1,1))
    setup_time = 1.0+np.random.pareto(a=1,size=m).reshape((-1,1))
    sym_time = np.cumsum(degrees_mat*comp_time,axis=1)
    enc_times = np.reshape(setup_time+sym_time,(-1,))
    enc_ord = np.argsort(enc_times)
    ctr = 0
    print (enc_times.shape)
    while decnum<m:
        encnum+=1
        encnum_list.append(encnum) #Number of encoded symbols received
        if len(encop_list)>0:
            # print (enc_ord[ctr])
            encop = encop_list[enc_ord[ctr]]
            time_inst = enc_times[ctr]
            ctr += 1
        else:
            encop=encoder(A,x,u)
        encrows_temp=encop[1][:]
        #print encop[0]
        for row in encrows_temp:
            if decrows[row]==1:
                #Contains symbol that has already been decoded
                encop[0]-=1
                encop[1].remove(row)
                encop[2]=encop[2]-bd[row]
        if encop[0]<=0:
            decnum_list.append(decnum)
            continue #No new information
        numrows.append(encop[0])
        encrows.append(encop[1])
        be.append(encop[2])
        for i in encop[1]:
            rowslist[i].append(k)
        k+=1
        while any([num==1 for num in numrows]):
            decop=decoder(be,encrows,numrows,rowslist)
            decnum+=1
            decrows[decop[0]]=1
            bd[decop[0]]=decop[1]
            #print decnum
            if decnum==m:
                print ("Decoding Complete")
                print (np.linalg.norm(bd-b)/np.linalg.norm(b))
                break
        decnum_list.append(decnum) #Number of symbols decoded upto this point
    #print k
    return time_inst

def main():
#    m=10000
#    c=0.2
#    delta=0.05
#    u=RS(m,c,delta)
#    print u[0][0:50]
#    plt.plot(u[0][0:50])
#        encrows.append(t[0])
#        numrows.append(len(t[0]))
#    plt.show()
    N=500 #Number of MC simulations
    m=500 #Number of symbols
    
    A=np.random.rand(m,1)
    x=np.random.rand(1)

    c=0.03
    delta=0.5
    u=np.ravel(RS(m,c,delta))
    times_vect = np.zeros(N)
    for i in range(N):
        print (i)
        times_vect[i]=fcrunner(A,x,c,delta,u)
#             degrees_arr[i] = np.asarray(degrees_list)
#             encnum[i]=encnum_list[-1]
        print (times_vect[i])
    np.save('lt_times_'+str(m)+'.npy',times_vect)
#         np.save('degrees_'+str(m)+'.npy',degrees_arr)
        # plt.hist(encnum)
        # plt.show()
if __name__ == '__main__':
    main()
