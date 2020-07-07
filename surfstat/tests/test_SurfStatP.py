import sys
sys.path.append("python")
from SurfStatP import *
import surfstat_wrap as sw
import numpy as np
import pytest

def dummy_test(slm, mask=None, clusthresh=0.001):

    try:
        # wrap matlab functions
        M_pval, M_peak, M_clus, M_clusid = sw.matlab_SurfStatP(slm, mask, clusthresh)
        
        print('AAAAAAAAAXXXXXXXXX ', M_pval, M_peak, M_clus, M_clusid)
        
    except:
        pytest.skip("Original MATLAB code does not work with these inputs.")

    # run python equivalent
    PY_pval, PY_peak, PY_clus, PY_clusid = py_SurfStatP(slm, mask, clusthresh)

    # compare matlab-python outputs
    testout_SurfStatP = []

    for key in M_pval:
        testout_SurfStatP.append(np.allclose(M_pval[key], PY_pval[key], 
                                      rtol=1e-05, equal_nan=True))
    for key in M_peak:
        testout_SurfStatP.append(np.allclose(M_peak[key], PY_peak[key], 
                                      rtol=1e-05, equal_nan=True))
    for key in M_clus:
        testout_SurfStatP.append(np.allclose(M_clus[key], PY_clus[key], 
                                      rtol=1e-05, equal_nan=True))
    testout_SurfStatP.append(np.allclose(M_clusid, PY_clusid, 
                              rtol=1e-05, equal_nan=True))


    assert all(flag == True for (flag) in testout_SurfStatP)

# data from Sofie
def test_1():  

    slmfile = './data/slm.mat'
    slmdata = loadmat(slmfile)

    slm = {}

    slm['t'] = slmdata['slm']['t'][0,0]
    slm['df'] = slmdata['slm']['df'][0,0]
    slm['k'] = slmdata['slm']['k'][0,0]
    slm['resl'] = slmdata['slm']['resl'][0,0]
    slm['tri'] = slmdata['slm']['tri'][0,0]

    dummy_test(slm)


# randomize Sofie's data a little bit
def test_2():

    v = int(64984)
    y = int(194940)

    slmfile = './data/slm.mat'
    slmdata = loadmat(slmfile)

    slm = {}

    slm['t'] = np.random.rand(1,v)
    slm['df'] = np.array([1111]) 
    slm['k'] = 1
    slm['resl'] = slmdata['slm']['resl'][0,0]
    slm['tri'] = slmdata['slm']['tri'][0,0]

    dummy_test(slm)


# data from Sofie, slm['t'] is array of shape (1,1)
def test_3():

    slmfile = './data/slm.mat'
    slmdata = loadmat(slmfile)

    slm = {}

    slm['t'] = np.array([[-0.1718374541922737]])
    slm['df'] = slmdata['slm']['df'][0,0]
    slm['k'] = 1
    slm['resl'] = slmdata['slm']['resl'][0,0]
    slm['tri'] = slmdata['slm']['tri'][0,0]

    dummy_test(slm)


