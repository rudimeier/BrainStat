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
    """Corrected P-values for vertices and clusters.

    Parameters
    ----------
    slm : a dictionary with keys 't', 'df', 'k', 'resl', 'tri' (or 'lat'). Optional
        key 'dfs'.
        slm['t'] : 2D numpy array of shape (l,v).
            v is number of vertices, slm['t'][0,:] is the test statistic, rest of the
            rows are used to calculate cluster resels if slm['k']>1. See SurfStatF for
            the precise definition of extra rows.
        surf['df'] : 2D numpy array of shape (1,1).
            degrees of freedom.
        surf['k'] : float
            number of variates
        surf['resl'] : 2D numpy array of shape (e,k).
            sum over observations of squares of differences of normalized residuals
            along each edge.
        surf['tri'] : 2D numpy array of shape (3,t), dtype=int.
            triangle indices.
        or,
        surf['lat'] : 3D numpy array of shape (nx,ny,nz), 1's and 0's.
            in fact, [nx,ny,nz] = size(volume).
        surf['dfs'] : 2D numpy array of shape (1,v), dtype=int.
            optional effective degrees of freedom.
    mask : 2D numpy array of shape (1,v), dtype=bool.
        1=inside, 0=outside, v= number of vertices. Default: np.ones((1,v), dtype=bool)
    clusthresh: float.
        P-value threshold or statistic threshold for defining clusters. Default: 0.001.
    

    Returns
    -------
    pval : a dictionary with keys 'P', 'C', 'mask'.
        pval['P'] : 2D numpy array of shape (1,v).
            corrected P-values for vertices.
        pval['C'] : 2D numpy array of shape (1,v).
            corrected P-values for clusters.
        pval['mask'] : copy of input mask.
    peak : a dictionary with keys 't', 'vertid', 'clusid', 'P'.
        peak['t'] : 2D numpy array of shape (np,1). peaks (local maxima).
        peak['vertid'] : 2D numpy array of shape (np,1). vertex.
        peak['clusid'] : 2D numpy array of shape (np,1). cluster id numbers.
        peak['P'] : 2D numpy array of shape (np,1). corrected P-values for the peak.
    clus : a dictionary with keys 'clusid', 'nverts', 'resels', 'P.'
        clus['clusid'] : 2D numpy array of shape (nc,1). cluster id numbers
        clus['nverts'] : 2D numpy array of shape (nc,1). number of vertices in cluster.
        clus['resels'] : 2D numpy array of shape (nc,1). resels in the cluster.
        clus['P'] : 2D numpy array of shape (nc,1). corrected P-values for the cluster.
    clusid : 2D numpy array of shape (1,v). cluster id's for each vertex.

    Reference: Worsley, K.J., Andermann, M., Koulis, T., MacDonald, D.
    & Evans, A.C. (1999). Detecting changes in nonisotropic images.
    Human Brain Mapping, 8:98-101.
    """
    l, v =np.shape(slm['t'])

    if mask is None:
        mask = np.ones((1,v), dtype=bool)

    df = np.zeros((2,2))
    ndf = len(slm['df'])
    df[0, 0:ndf] = slm['df']
    df[1, 0:2] = slm['df'][ndf-1]
    
    if 'dfs' in slm.keys():
        df[0, ndf-1] = slm['dfs'][mask > 0].mean()
    
    if v == 1:
        varA = np.concatenate((np.array([[10]]), slm['t']), axis=1)
        pval = {}
        # NEED TO BE CALLED FROM PYTHON STAT_THRESHOLD
        pval['P'] = np.array(eng.stat_threshold(var2mat(0),
                                                var2mat(1),
                                                var2mat(0),
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
        pval['P'] = pval['P'][0,1]
        peak = []
        clus = []
        clusid = []

        # only a single p-value is returned, and function is stopped.
        return pval, peak, clus, clusid
        sys.exit()
    
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

