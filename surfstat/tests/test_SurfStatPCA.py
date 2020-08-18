import sys
sys.path.append("python")
sys.path.append("/data/p_02323/BrainStat/surfstat/")
import surfstat_wrap as sw
from SurfStatPCA import *
from term import Term
import numpy as np
import random
import pytest

def dummy_test(Y, mask=None, X=0, c=4):

    try:
        # wrap matlab functions
        M_pcntvar, M_U, M_V = sw.matlab_SurfStatPCA(Y, mask, X, c)
        #print('AAAAA  ', M_pcntvar, M_U, M_V)
    except:
        pytest.skip("Original MATLAB code does not work with these inputs.")

    # run python equivalent
    P_pcntvar, P_U, P_V = py_SurfStatPCA(Y, mask, X, c)

    #print('BBBBB  ')
    #print(M_U)
    #print(P_U)
    #print(P_V)
    # compare matlab-python outputs
    testout_SurfStatPCA = []

    testout_SurfStatPCA.append(np.allclose(M_pcntvar, P_pcntvar, 
                               rtol=1e-05, equal_nan=True))
    testout_SurfStatPCA.append(np.allclose(M_U, P_U, 
                               rtol=1e-05, equal_nan=True))
    testout_SurfStatPCA.append(np.allclose(M_V, P_V, 
                               rtol=1e-05, equal_nan=True))

    print(testout_SurfStatPCA)
    
    return
    
sw.matlab_init_surfstat()

#    Y : 2D numpy array of shape (n,v) , or 3D numpy array of shape (n,v,k),
#        v is the number of vertices.
#    mask : 2D numpy array of shape (1,v), ones and zeros,
#        mask array, 1=inside, 0=outside, by default np.ones((1,v)).
#    X : a scalar, or 2D numpy array of shape (n,p), or type term,
#        if array, X is a design matrix of p covariates for the linear model,
#        if term, X is model formula. The PCA is done on the v x v correlations
#        of the residuals and the components are standardized to have unit
#        standard deviation about zero. If X=0, nothing is removed. If X=1,
#        the mean (over rows) is removed (default).
#    c : an int (has to be <=n), by default 4,
#        number of components in PCA

# NOT WORKING --> eig functions differ
# Y: 2D arry, mask: 2D array ones, X: scalar, c: int
n = np.random.randint(1,100)
v = np.random.randint(1,100)

Y = np.random.rand(n,v)
mask = np.ones((1,v))  
X = random.uniform(0,100) 
c = n

print('n : ', n, 'v : ', v, 'c: ', c)
print(Y)
print(X)
dummy_test(Y, mask, X, c)

Y = np.array([[1,1], [1,1]]) 
mask = np.ones((1,2))  
X = 0 
c = 1 

dummy_test(Y, mask, X, c)



Y = np.zeros((2,2,2))
Y[:,:,0] = np.array([[1,1], [1,1]])
Y[:,:,1] = np.array([[1,1], [1,1]])
mask = np.ones((1,2))  
X = 0 
c = 1 
dummy_test(Y, mask, X, c)



Y = np.zeros((2,2,2))
Y[:,:,0] = np.array([[1,1], [1,1]])
Y[:,:,1] = np.array([[1,1], [1,1]])
mask = np.ones((1,2))  
X = np.array([[0.6, 0.6]])
c = 1 
dummy_test(Y, mask, X, c)


Y = np.zeros((2,2,2))
Y[:,:,0] = np.array([[1,1], [1,1]])
Y[:,:,1] = np.array([[1,1], [1,1]])
mask = np.ones((1,2))  
X = np.array([[0.6, 0.6], [1,1]])
c = 1 
dummy_test(Y, mask, X, c)

Y = np.zeros((2,2,2))
Y[:,:,0] = np.array([[1,1], [1,1]])
Y[:,:,1] = np.array([[1,1], [1,1]])
mask = np.ones((1,2))  
X = np.array([[0.6, 0.6], [1,1]])
c = 1 
dummy_test(Y, mask, X, c)



### NOT WORKING
Y = np.array([[1,1], [1,1]]) 
mask = np.ones((1,2))  
X = np.array([[1,1,1,1]])
c = 1 
dummy_test(Y, mask, X, c)



### NOT WORKING
Y = np.array([[1,1], [1,1]]) 
mask = np.ones((1,2))  
X = Term(np.array([[1,1,1,1]])) 
c = 1 
dummy_test(Y, mask, X, c)


