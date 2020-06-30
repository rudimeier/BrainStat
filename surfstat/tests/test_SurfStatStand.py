import numpy as np
import pytest
import sys

sys.path.append("python")
from SurfStatStand import *
import surfstat_wrap as sw

sw.matlab_init_surfstat()

def dummy_test(Y, mask, subtractordivide):

	try:
		# wrap matlab functions
		Wrapped_Y, Wrapped_Ym = sw.matlab_SurfStatStand(Y, mask, subtractordivide) 

	except:
		pytest.fail("ORIGINAL MATLAB CODE DOES NOT WORK WITH THESE INPUTS...")

	# python function
	Python_Y, Python_Ym = py_SurfStatStand(Y, mask, subtractordivide)

	# compare matlab-python outputs
	testout_SurfStatStand = []

	testout_SurfStatStand.append(np.allclose(Wrapped_Y, Python_Y, \
					   			rtol=1e-05, equal_nan=True))

	testout_SurfStatStand.append(np.allclose(Wrapped_Ym, Python_Ym, \
					   			rtol=1e-05, equal_nan=True))
	#result_SurfStatStand = all(flag == True for (flag) in testout_SurfStatStand)

	assert all(flag == True for (flag) in testout_SurfStatStand)


#### test 1a
# 1D inputs --- row vectors
def test_1d_row_vectors():
	v = np.random.randint(1,9)
	a = np.arange(1,v)
	a = a.reshape(1, len(a))
	Y = a
	mask = None
	subtractordivide = 's'
	dummy_test(Y, mask=mask, subtractordivide=subtractordivide)

#### test 1b
# 1D inputs --- row vectors & mask
def test_1d_row_vectors_mask():
	a = np.arange(1,11)
	a = a.reshape(1, len(a))
	Y = a
	mask = np.array([1, 1, 0, 1, 1, 1, 1, 1, 1, 1], dtype=bool)
	subtractordivide = 's'
	dummy_test(Y, mask=mask, subtractordivide=subtractordivide)
	

#### test 2a
# 2D inputs --- 2D arrays & mask
def test_2d_arrays_mask():
	a = np.arange(1,11)
	a = a.reshape(1, len(a))
	Y = np.concatenate((a,a), axis=0)
	mask = np.array([1, 1, 0, 0, 1, 1, 1, 1, 1, 1], dtype=bool)
	subtractordivide = 's'
	dummy_test(Y, mask=mask, subtractordivide=subtractordivide)


#### test 3a
# 3D inputs --- 3D arrays & mask
def test_3d_arrays_mask():
	a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
	Y = np.zeros((3,4,2))
	Y[:,:,0] = a
	Y[:,:,1] = a
	mask = np.array([1, 1, 0, 0], dtype=bool)
	subtractordivide = 's'
	dummy_test(Y, mask=mask, subtractordivide=subtractordivide)

