import sys
sys.path.append("python")
from SurfStatInflate import *
import surfstat_wrap as sw
import numpy as np
import pytest

def dummy_test(surf, w=0.5, spherefile=None):

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

    print(testout_SurfStatInflate)
    
    #return all(flag == True for (flag) in testout_SurfStatInflate)

    return

sw.matlab_init_surfstat()


def test_1():
    v = 40962
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    w = np.random.rand() 
    dummy_test(surf, w)

def test_2():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    w = np.random.rand() 
    dummy_test(surf, w)
    
def test_3():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=300, size=(3,v))
    dummy_test(surf)
    
def test_4():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=1000, size=(3,v))
    w = np.random.rand() 
    dummy_test(surf, w)
    
def test_5():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    w = np.random.rand() 
    dummy_test(surf, w)
    
def test_6():
    v = 81924
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    dummy_test(surf)

def test_7():
    v = 81924
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    dummy_test(surf)
    
def test_8():
    v = 81924
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=300, size=(3,v))
    dummy_test(surf)
    
def test_9():
    v = 81924
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=1000, size=(3,v))
    dummy_test(surf)
    
def test_10():
    v = 81924
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    dummy_test(surf)   

def test_11():
    v = 40962
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    surf['coord'][0,:] = np.ones((1,v)) * -1
    dummy_test(surf)

def test_12():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    surf['coord'][0,:] = np.ones((1,v)) * -1
    dummy_test(surf)
    
def test_13():
    v = 40962
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=-1, size=(3,v))
    dummy_test(surf)
    
def test_14():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=-10, size=(3,v))
    dummy_test(surf)
    
def test_15():
    v = 40962
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    surf['coord'][0,:] = -1*abs(surf['coord'][0,:])     
    dummy_test(surf)
    
def test_16():
    v = 163842
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    dummy_test(surf)

def test_17():
    v = 163842
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    dummy_test(surf)
    
def test_18():
    v = 163842
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=300, size=(3,v))
    dummy_test(surf)
    
def test_19():
    v = 163842
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=1000, size=(3,v))
    dummy_test(surf)
    
def test_20():
    v = 163842
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    dummy_test(surf)

def test_21():
    v = 163842
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    surf['coord'][0,:] = np.ones((1,v)) * -1
    dummy_test(surf)

def test_22():
    v = 163842
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    surf['coord'][0,:] = np.ones((1,v)) * -1
    dummy_test(surf)
    
def test_23():
    v = 163842
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=-1, size=(3,v))
    dummy_test(surf)
    
def test_24():
    v = 163842
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=-10, size=(3,v))
    dummy_test(surf)
    
def test_25():
    v = 163842
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    surf['coord'][0,:] = -1*abs(surf['coord'][0,:])     
    dummy_test(surf)

def test_26():
    v = 327684
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    dummy_test(surf)

def test_27():
    v = 327684
    surf = {}
    surf['coord'] = np.random.uniform(low=-3, high=3, size=(3,v))
    dummy_test(surf)
    
def test_28():
    v = 327684
    surf = {}
    surf['coord'] = np.random.uniform(low=-300, high=300, size=(3,v))
    dummy_test(surf)
    
def test_29():
    v = 327684
    surf = {}
    surf['coord'] = np.random.randint(low=-1000, high=1000, size=(3,v))
    dummy_test(surf)
    
def test_30():
    v = 327684
    surf = {}
    surf['coord'] = np.random.randint(low=-(v-1), high=(v+1), size=(3,v))
    dummy_test(surf)

def test_31():
    v = 32492
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    w = np.random.rand() 
    spherefile = './tests/data/loadconte69_sphereleft.obj'
    dummy_test(surf, w, spherefile)
    
def test_32():
    v = 32492
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    w = np.random.rand() 
    spherefile = './tests/data/loadconte69_sphereright.obj'
    dummy_test(surf, w, spherefile)
    
def test_33():
    v = 32492
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    w = np.random.rand() 
    spherefile = './tests/data/FS_loadconte69_left.sphere'
    dummy_test(surf, w, spherefile)
    
def test_34():
    v = 32492
    surf = {}
    surf['coord'] = np.random.rand(3,v)
    w = np.random.rand() 
    spherefile = './tests/data/FS_loadconte69_right.sphere'
    dummy_test(surf, w, spherefile)
