import sys
sys.path.append("/data/p_02323/BrainStat/surfstat")
sys.path.append("/data/p_02323/BrainStat/surfstat/python")
sys.path.append("/data/p_02323/BrainStat/surfstat/matlab")
from SurfStatInflate import *
import surfstat_wrap as sw
import numpy as np
import pytest

def dummy_test(surf, w=0.5, spherefile='sphere.obj'):

    try:
        # wrap matlab functions
        M_surfw = sw.matlab_SurfStatInflate(surf, w, spherefile)

    except:
        pytest.skip("Original MATLAB code does not work with these inputs.")
	
    # run python functions
    P_surfw = py_SurfStatInflate(surf, w, spherefile)    

    # compare matlab-python outputs
    testout_SurfStatInflate = []

    for key in P_surfw:
        testout_SurfStatInflate.append(np.allclose(P_surfw[key], \
                                       M_surfw[key], \
                                       rtol=1e-05, equal_nan=True))

    #print(testout_SurfStatInflate)
    
    return all(flag == True for (flag) in testout_SurfStatInflate)


sw.matlab_init_surfstat()

def test_1():
    v = 40962
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    dummy_test(surf)

def test_2():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    dummy_test(surf)
    
def test_3():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=300, size=(3,v))
    dummy_test(surf)
    
def test_4():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=1000, size=(3,v))
    dummy_test(surf)
    
def test_5():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    dummy_test(surf)
