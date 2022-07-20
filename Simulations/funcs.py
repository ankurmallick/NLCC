import numpy as np

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

def get_tail(vect):
    probs, bin_edges = np.histogram(vect,bins=100,density=False)
    tail = np.cumsum(probs[::-1])[::-1]/vect.shape[0]
    return tail,bin_edges

def get_rep_time(times,num_rep):
    
    num_workers = times.shape[0]
    num_coupons = num_workers//num_rep #Each worker does num_rep computations
    times_mat = times.reshape((num_rep,num_coupons))
    coupon_times = times_mat.min(0)
    
    return np.amax(coupon_times)

def get_bcc_time(times,num_rep):
    
    num_workers = times.shape[0]
    num_coupons = num_workers//num_rep #Each worker does num_rep computations
    coupon_vect = np.arange(num_coupons)
    assign_vect = np.random.choice(coupon_vect,size=num_workers) #Coupons are randomly sampled
    
#     print (assign_vect)
    
    coupon_times = [np.amin(times[assign_vect==coupon]) for coupon in coupon_vect]
    
    return np.amax(coupon_times)
    
    

# def get_lt_time(times,decthresh):
#     return np.sort(times)[decthresh]

# def get_lt_degree(num_src,num_enc)
#     c=0.03
#     delta=0.5
#     u = RS(num_src,c,delta)
#     d = 1+np.random.choice(num_src, size=num_enc, replace=True, p=u) #Degree