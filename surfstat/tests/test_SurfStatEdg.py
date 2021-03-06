import sys
sys.path.append("python")
from SurfStatEdg import *
import surfstat_wrap as sw
import numpy as np
import pytest
from brainspace.datasets import load_conte69

sw.matlab_init_surfstat()

def dummy_test(surf):
    try:
        # wrap matlab functions
        Wrapped_edg = sw.matlab_SurfStatEdg(surf)

    except:
        pytest.skip("ORIGINAL MATLAB CODE DOES NOT WORK WITH THESE INPUTS...")

    Python_edg = py_SurfStatEdg(surf) + 1 # +1 to match across implementations.

    # compare matlab-python outputs
    testout = np.allclose(Wrapped_edg, Python_edg, rtol=1e-05, equal_nan=True)
    assert testout


#### Test 1 
def test_surf_tri():
	# take ax3 random arrays for surf['tri']
	a = np.random.randint(4,100)
	A = {}
	A['tri'] = np.random.rand(a,3)
	dummy_test(A)

#### Test 2
def test_surf_lat_2d():
    # dummy 3D array for surf['lat']
    A = {}
    A['lat'] = np.ones((10,10))
    dummy_test(A)

#### Test 3
def test_surf_lat_ones():
    # dummy 3D array for surf['lat']
    A = {}
    A['lat'] = np.ones((10,10,10))
    dummy_test(A)

### Test 4
def test_surf_lat_ones_zeros():
    A = {}
    A['lat'] = np.random.choice([0, 1], size=(10,10,10))    
    dummy_test(A)

# Test BSPolyData. 
def test_bspolydata():
    surf, _ = load_conte69()
    dummy_test(surf)
