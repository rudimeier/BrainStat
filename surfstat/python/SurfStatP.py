import sys
sys.path.append("python")
sys.path.append("../surfstat")
import surfstat_wrap as sw
import matlab.engine
import numpy as np
from scipy.interpolate import interp1d
from scipy.io import loadmat

# WRAPPING FUNCTIONS NEED TO BE REMOVED LATER...
sw.matlab_init_surfstat()
eng = matlab.engine.start_matlab()
eng.addpath('matlab/')
def var2mat(var):
    # Brings the input variables to matlab format.
    if isinstance(var, np.ndarray):
        var = var.tolist()
    elif var == None:
        var = []
    if not isinstance(var,list) and not isinstance(var, np.ndarray):
        var = [var]
    return matlab.double(var)

def py_SurfStatP(slm, mask=None, clusthresh=0.001):
    
    l, v =np.shape(slm['t'])
    
    if mask is None:
        mask = np.ones((1,v), dtype=bool)
    
    
    df = np.zeros((2,2))
    
    ndf = len(slm['df'])
    df[0, 0:ndf] = slm['df']
    df[1, 0:2] = slm['df'][ndf-1]
    
    # NOT YET IMPLEMENTED
    #if 'dfs' in slm.keys():
    #    df[0, ndf-1] = ...
    
    # NOT YET IMPLEMENTED
    #if v == 1:
    #    ....
    
    if clusthresh < 1:
        # NEED TO BE CALLED FROM PYTHON STAT_THRESHOLD
        thresh, b,c,d,e,f = eng.stat_threshold(var2mat(0),
                            var2mat(1),
                            var2mat(0),
                            var2mat(df),
                            var2mat(clusthresh),
                            var2mat([]),
                            var2mat([]),
                            var2mat([]),
                            var2mat(slm['k']),
                            var2mat([]),
                            var2mat([]),
                            var2mat(0),
                            nargout=6)
    else:
        thresh = clusthresh

    # NEED TO BE CALLED FROM PYTHON SURFSTATRESELS
    resels, reselspvert, edg = sw.matlab_SurfStatResels(slm, mask)
    N = mask.sum()
    
    if np.max(slm['t'][0, mask.flatten()]) < thresh:
        pval = {}
        varA = np.concatenate((np.array([[10]]), slm['t']), axis=1)
       
        # NEED TO BE CALLED FROM PYTHON STAT_THRESHOLD
        pval['P'] = np.array(eng.stat_threshold(var2mat(resels),
                                                var2mat(N),
                                                var2mat(1),
                                                var2mat(df),
                                                var2mat(varA),
                                                var2mat([]),
                                                var2mat([]),
                                                var2mat([]),
                                                var2mat(slm['k']),
                                                var2mat([]),
                                                var2mat([]),
                                                var2mat(0),
                                                nargout=1))
        pval['P'] = pval['P'][0, 1:v+1]
        peak = []
        clus = []
        clusid = []
    
    else:
        # NEED TO BE CALLED FROM PYTHON SURFSTATPEAKCLUSTER
        peak, clus, clusid  = sw.matlab_SurfStatPeakClus(slm, mask, thresh,
                                                         reselspvert, edg)
        slm['t'] = slm['t'].reshape(1, slm['t'].size)

        varA = np.concatenate((np.array([[10]]), peak['t'].T , slm['t']),
                              axis=1)
        varB = np.concatenate((np.array([[10]]), clus['resels']))
                
        # NEED TO BE CALLED FROM PYTHON STAT_THRESHOLD
        pp, clpval = eng.stat_threshold(var2mat(resels),
                                        var2mat(N),
                                        var2mat(1),
                                        var2mat(df),
                                        var2mat(varA),
                                        var2mat(thresh),
                                        var2mat(varB),
                                        var2mat([]),
                                        var2mat(slm['k']),
                                        var2mat([]),
                                        var2mat([]),
                                        var2mat(0),
                                        nargout=2)
        pp = np.array(pp)
        clpval = np.array(clpval)
        
        peak['P'] = pp[:,1:len(peak['t'])+1].T
        pval = {}
        pval['P'] = pp[0,len(peak['t']) + np.arange(1,v+1)]
        
        if slm['k'] > 1:
            print('NOT YET IMPLEMENTED')
            
        clus['P'] = clpval[1:len(clpval)]
        
        x = np.concatenate((np.array([[0]]), clus['clusid']), axis=0)
        y = np.concatenate((np.array([[1]]), clus['P']), axis=0)
        
        pval['C'] = interp1d(x.flatten(),y.flatten())(clusid)
    
    # NEED TO BE CALLED FROM PYTHON STAT_THRESHOLD
    tlim = eng.stat_threshold(var2mat(resels),
                                var2mat(N),
                                var2mat(1),
                                var2mat(df),
                                var2mat([0.5, 1]),
                                var2mat([]),
                                var2mat([]),
                                var2mat([]),
                                var2mat(slm['k']),
                                var2mat([]),
                                var2mat([]),
                                var2mat(0),
                                nargout=1)
    tlim = np.array(tlim)
    tlim = tlim[0,1]

    pval['P'] = pval['P'] * (slm['t'][0,:] > tlim) + (slm['t'][0,:] <= tlim)
    pval['mask'] = mask

    return pval, peak, clus, clusid

