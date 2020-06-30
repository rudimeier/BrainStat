# This file contains all the matlab_Surfstat* wrapper functions. Some of
# them are not yet implemented

#import matlab.engine
import matlab
import oct2py
import numpy as np
import sys

def matlab_init_surfstat():
    global surfstat_eng
    #surfstat_eng = matlab.engine.start_matlab()
    surfstat_eng = oct2py.Oct2Py()
    addpath = surfstat_eng.addpath('matlab')

# ==> SurfStatAvSurf.m <==
def matlab_SurfStatAvSurf(filenames, fun):
    sys.exit("Function matlab_SurfStatAvSurf is not implemented yet")

# ==> SurfStatAvVol.m <==
def matlab_SurfStatAvVol(filenames, fun, Nan):
    sys.exit("Function matlab_SurfStatAvVol is not implemented yet")

# ==> SurfStatColLim.m <==
def matlab_SurfStatColLim(clim):
    sys.exit("Function matlab_SurfStatColLim is not implemented yet")

# ==> SurfStatColormap.m <==
def matlab_SurfStatColormap(map):
    sys.exit("Function matlab_SurfStatColormap is not implemented yet")







# ==> SurfStatCoord2Ind.m <==
def matlab_SurfStatCoord2Ind(coord, surf):
    if isinstance(coord, np.ndarray):
        coord = matlab.double(coord.tolist())
    surf_mat = surf.copy()
    for key in surf_mat.keys():
        surf_mat[key] = matlab.double(surf_mat[key].tolist())  
    ind = surfstat_eng.SurfStatCoord2Ind(coord, surf_mat)
    return np.array(ind)







# ==> SurfStatDataCursor.m <==
def matlab_SurfStatDataCursor(empt,event_obj):
    sys.exit("Function matlab_SurfStatDataCursor is not implemented yet")

# ==> SurfStatDataCursorP.m <==
def matlab_SurfStatDataCursorP(empt,event_obj):
    sys.exit("Function matlab_SurfStatDataCursorP is not implemented yet")

# ==> SurfStatDataCursorQ.m <==
def matlab_SurfStatDataCursorQ(empt,event_obj):
    sys.exit("Function matlab_SurfStatDataCursorQ is not implemented yet")

# ==> SurfStatDelete.m <==
def matlab_SurfStatDelete(varargin):
    sys.exit("Function matlab_SurfStatDelete is not implemented yet")







# ==> SurfStatEdg.m <==
def matlab_SurfStatEdg(surf):
    surf_mat = surf.copy()
    for key in surf_mat.keys():
        if np.ndim(surf_mat[key]) == 0:
            surf_mat[key] = surfstat_eng.double(surf_mat[key].item())
        else:
            surf_mat[key] = surf_mat[key].tolist()
    edg = surfstat_eng.SurfStatEdg(surf_mat)
    return np.array(edg)








# ==> SurfStatF.m <==
def matlab_SurfStatF(slm1, slm2):

    slm1_mat = slm1.copy()
    for key in slm1_mat.keys():
        if np.ndim(slm1_mat[key]) == 0:
            slm1_mat[key] = surfstat_eng.double(slm1_mat[key])
        else:
            slm1_mat[key] = matlab.double(slm1_mat[key].tolist())    

    slm2_mat = slm2.copy()
    for key in slm2_mat.keys():
        if np.ndim(slm2_mat[key]) == 0:
            slm2_mat[key] = surfstat_eng.double(slm2_mat[key])
        else:
            slm2_mat[key] = matlab.double(slm2_mat[key].tolist())    
    
    result_mat = (surfstat_eng.SurfStatF(slm1_mat, slm2_mat))    

    result_mat_dic = {key: None for key in result_mat.keys()}
    for key in result_mat:
        result_mat_dic[key] = np.array(result_mat[key])
    return result_mat_dic







# ==> SurfStatInd2Coord.m <==
def matlab_SurfStatInd2Coord(ind, surf):
    if isinstance(ind, np.ndarray):
        ind = matlab.double(ind.tolist())
    surf_mat = surf.copy()
    for key in surf_mat.keys():
        surf_mat[key] = matlab.double(surf_mat[key].tolist())  
    coord = surfstat_eng.SurfStatInd2Coord(ind, surf_mat)
    return np.array(coord)







# ==> SurfStatInflate.m <==
def matlab_SurfStatInflate(surf, w, spherefile):
    sys.exit("Function matlab_SurfStatInflate is not implemented yet")






# ==> SurfStatLinMod.m <==
def matlab_SurfStatLinMod(T, M, surf=None, niter=1, thetalim=0.01, drlim=0.1):

    # TODO implement ignored arguments

    if isinstance(T, np.ndarray):
        T = T.tolist()
    else:
        T = surfstat_eng.double(T)

    if isinstance(M, np.ndarray):
        M = M.tolist()
    else:
        M = surfstat_eng.double(M)

    if surf is None:
        result_mat = surfstat_eng.SurfStatLinMod(T, M)
    else:
        surf_mat = surf.copy()
        for key in surf_mat.keys():
            if np.ndim(surf_mat[key]) == 0:
                surf_mat[key] = surfstat_eng.double(surf_mat[key].item())
            else:
                surf_mat[key] = matlab.double(surf_mat[key].tolist())    
        result_mat = surfstat_eng.SurfStatLinMod(T, M, surf_mat)    

    result_mat_dic = {key: None for key in result_mat.keys()}
    for key in result_mat:
        result_mat_dic[key] = np.array(result_mat[key])

    return result_mat_dic

# ==> SurfStatListDir.m <==
def matlab_SurfStatListDir(d, exclude):
    sys.exit("Function matlab_SurfStatListDir is not implemented yet")

# ==> SurfStatMaskCut.m <==
def matlab_SurfStatMaskCut(surf):
    sys.exit("Function matlab_SurfStatMaskCut is not implemented yet")






# ==> SurfStatNorm.m <==
def matlab_SurfStatNorm(Y, mask=None, subdiv='s'):
	# Normalizes by subtracting the global mean, or dividing it. 
    # Inputs     	
    # Y      = numpy array of shape (n x v) or (n x v x k). 
    #          v=#vertices.
    # mask   = numpy boolean array of shape (1 x v). 
    #          True=inside the mask, False=outside. 
    # subdiv = 's' for Y=Y-Yav or 'd' for Y=Y/Yav.
    # Outputs
    # Y      = normalized data, numpy array of shape (n x v) or (n x v x k)
    # Yav    = mean of input Y along the mask, numpy array of shape (n x 1) or (n x k)   

    Y = Y.tolist()

    if mask is None and subdiv=='s':
        Y, Ya = surfstat_eng.SurfStatNorm(Y, nargout=2)
    
    elif mask is not None and subdiv=='s':
        mymask = np.array(mask, dtype=int)
        mymask = matlab.logical(mymask.tolist())
        Y, Ya = surfstat_eng.SurfStatNorm(Y, mymask, nargout=2)

    elif mask is not None and subdiv=='d':
        mymask = np.array(mask, dtype=int)
        mymask = matlab.logical(matlab.double(mymask.tolist()))
        Y, Ya = surfstat_eng.SurfStatNorm(Y, mymask, subdiv, nargout=2)

    return np.array(Y), np.array(Ya)






# ==> SurfStatP.m <==
# TODO original matlab signature was SurfStatP(slm, mask, clusthresh):
def matlab_SurfStatP(results):
    return surfstat_eng.SurfStatP(results)

# ==> SurfStatPCA.m <==
def matlab_SurfStatPCA(Y, mask, X, k):
    sys.exit("Function matlab_SurfStatPCA is not implemented yet")

# ==> SurfStatPeakClus.m <==
def matlab_SurfStatPeakClus(slm, mask, thresh, reselspvert, edg):
    sys.exit("Function matlab_SurfStatPeakClus is not implemented yet")

# ==> SurfStatPlot.m <==
def matlab_SurfStatPlot(x, y, M, g, varargin):
    sys.exit("Function matlab_SurfStatPlot is not implemented yet")

# ==> SurfStatQ.m <==
def matlab_SurfStatQ(slm, mask):
    sys.exit("Function matlab_SurfStatQ is not implemented yet")

# ==> SurfStatROI.m <==
def matlab_SurfStatROI(centre, radius, surf):
    sys.exit("Function matlab_SurfStatROI is not implemented yet")

# ==> SurfStatROILabel.m <==
def matlab_SurfStatROILabel(lhlabel, rhlabel, nl, nr):
    sys.exit("Function matlab_SurfStatROILabel is not implemented yet")

# ==> SurfStatReadData.m <==
def matlab_SurfStatReadData(filenames, dirname, maxmem):
    sys.exit("Function matlab_SurfStatReadData is not implemented yet")

# ==> SurfStatReadData1.m <==
def matlab_SurfStatReadData1(filename):
    sys.exit("Function matlab_SurfStatReadData1 is not implemented yet")

# ==> SurfStatReadSurf.m <==
def matlab_SurfStatReadSurf(filenames,ab,numfields,dirname,maxmem):
    sys.exit("Function matlab_SurfStatReadSurf is not implemented yet")

# ==> SurfStatReadSurf1.m <==
def matlab_SurfStatReadSurf1(filename, ab, numfields):
    sys.exit("Function matlab_SurfStatReadSurf1 is not implemented yet")

# ==> SurfStatReadVol.m <==
def matlab_SurfStatReadVol(filenames,mask,step,dirname,maxmem):
    sys.exit("Function matlab_SurfStatReadVol is not implemented yet")

# ==> SurfStatReadVol1.m <==
def matlab_SurfStatReadVol1(file, Z, T):
    sys.exit("Function matlab_SurfStatReadVol1 is not implemented yet")

# ==> SurfStatResels.m <==
def matlab_SurfStatResels(slm, mask):
    sys.exit("Function matlab_SurfStatResels is not implemented yet")





# ==> SurfStatSmooth.m <==
def matlab_SurfStatSmooth(Y, surf, FWHM):
    
    #Y : numpy array of shape (n,v) or (n,v,k)
    #    surface data, v=#vertices, n=#observations, k=#variates.
    #surf : a dictionary with key 'tri' or 'lat'
    #    surf['tri'] = numpy array of shape (t,3), triangle indices, or
    #    surf['lat'] = numpy array of shape (nx,ny,nz), 1=in, 0=out,
    #    (nx,ny,nz) = size(volume).
    #FWHM : approximate FWHM of Gaussian smoothing filter, in mesh units.

    Y_mat = matlab.double(Y.tolist())

    surf_mat = surf.copy()

    for key in surf_mat.keys():
        if np.ndim(surf_mat[key]) == 0:
            surf_mat[key] = surfstat_eng.double(surf_mat[key].item())
        else:
            surf_mat[key] = matlab.double(surf_mat[key].tolist())

    FWHM_mat = FWHM

    Y_mat_out = surfstat_eng.SurfStatSmooth(Y_mat, surf_mat, FWHM_mat)

    return np.array(Y_mat_out)





# ==> SurfStatStand.m <==
def matlab_SurfStatStand(Y, mask=None, subtractordivide='s'):

	# Standardizes by subtracting the global mean, or dividing it.
 	# Inputs
	# Y      = numpy array of shape (n x v), v=#vertices.
	#        = NEED TO BE DISCUSSED: it works for (n x v x k) now, DO WE NEED THAT?
	# mask   = numpy boolean array of shape (1 x v). 
    #          True=inside the mask, False=outside.
	# subdiv = 's' for Y=Y-Ymean or 'd' for Y=(Y/Ymean -1)*100. 
	# Outputs
	# Y      = standardized data, numpy array of shape (n x v).
	# Ym     = mean of input Y along the mask, numpy array of shape (n x 1).

    Y = matlab.double(Y.tolist())
    if mask is None and subtractordivide=='s':
        Y, Ya = surfstat_eng.SurfStatStand(Y, nargout=2)
    
    elif mask is not None and subtractordivide=='s':
        mymask = np.array(mask, dtype=int)
        mymask = matlab.logical(matlab.double(mymask.tolist()))
        Y, Ya = surfstat_eng.SurfStatStand(Y, mymask, nargout=2)

    elif mask is not None and subtractordivide=='d':
        mymask = np.array(mask, dtype=int)
        mymask = matlab.logical(matlab.double(mymask.tolist()))
        Y, Ya = surfstat_eng.SurfStatStand(Y, mymask, subtractordivide, nargout=2)

    return np.array(Y), np.array(Ya)





    
# ==> SurfStatSurf2Vol.m <==
def matlab_SurfStatSurf2Vol(s, surf, template):
    sys.exit("Function matlab_SurfStatSurf2Vol is not implemented yet")
	
	
	

	
# ==> SurfStatT.m <==
def matlab_SurfStatT(slm, contrast):
    # T statistics for a contrast in a univariate or multivariate model.
    # Inputs
    # slm         = a dict with mandatory keys 'X', 'df', 'coef', 'SSE'
    # slm['X']    = numpy array of shape (n x p), design matrix.
    # slm['df']   = numpy array of shape (a,), dtype=float64, degrees of freedom
    # slm['coef'] = numpy array of shape (p x v) or (p x v x k)
    #             = array of coefficients of the linear model.
    #             = if (p x v), then k is thought to be 1.
    # slm['SSE']  = numpy array of shape (k*(k+1)/2 x v)
    #             = array of sum of squares of errors
    #
    # contrast    = numpy array of shape (n x 1)
    #             = vector of contrasts in the observations, ie.
    #             = ...

    slm_mat = slm.copy()
    
    for key in slm_mat.keys():
        if np.ndim(slm_mat[key]) == 0:
            slm_mat[key] = surfstat_eng.double(slm_mat[key].item())
        else:
            slm_mat[key] = matlab.double(slm_mat[key].tolist())

    contrast = contrast.tolist()
    
    slm_MAT = surfstat_eng.SurfStatT(slm_mat, contrast)
    
    slm_py = {}
    
    for key in slm_MAT.keys():
        slm_py[key] = np.array(slm_MAT[key])

    return slm_py
    
    
    
    

    
# ==> SurfStatView.m <==
def matlab_SurfStatView(struct, surf, title, background):
    sys.exit("Function matlab_SurfStatView is not implemented yet")

# ==> SurfStatView1.m <==
def matlab_SurfStatView1(struct, surf, varargin):
    sys.exit("Function matlab_SurfStatView1 is not implemented yet")

# ==> SurfStatViewData.m <==
def matlab_SurfStatViewData(data, surf, title, background):
    sys.exit("Function matlab_SurfStatViewData is not implemented yet")

# ==> SurfStatViews.m <==
def matlab_SurfStatViews(data, vol, z, layout):
    sys.exit("Function matlab_SurfStatViews is not implemented yet")

# ==> SurfStatVol2Surf.m <==
def matlab_SurfStatVol2Surf(vol, surf):
    sys.exit("Function matlab_SurfStatVol2Surf is not implemented yet")

# ==> SurfStatWriteData.m <==
def matlab_SurfStatWriteData(filename, data, ab):
    sys.exit("Function matlab_SurfStatWriteData is not implemented yet")

# ==> SurfStatWriteSurf.m <==
def matlab_SurfStatWriteSurf(filenames, surf, ab):
    sys.exit("Function matlab_SurfStatWriteSurf is not implemented yet")

# ==> SurfStatWriteSurf1.m <==
def matlab_SurfStatWriteSurf1(filename, surf, ab):
    sys.exit("Function matlab_SurfStatWriteSurf1 is not implemented yet")

# ==> SurfStatWriteVol.m <==
def matlab_SurfStatWriteVol(filenames, data, vol):
    sys.exit("Function matlab_SurfStatWriteVol is not implemented yet")

# ==> SurfStatWriteVol1.m <==
def matlab_SurfStatWriteVol(d, Z, T):
    sys.exit("Function matlab_SurfStatWriteVol is not implemented yet")
