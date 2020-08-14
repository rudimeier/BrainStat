import sys
sys.path.append('matlab')
import numpy as np
import scipy.io as sio
import matlab.engine
import matlab

global eng
eng = matlab.engine.start_matlab()
addpath = eng.addpath('matlab')



def py_SurfStatInflate(surf, w=0.5, spherefile='sphere.obj'):
    """Inflates a surface mesh to hemi-ellipsoids.

    Parameters
    ----------
    surf : a dictionary with key 'coord',
        surf['coord'] : 2D numpy array of shape (3,v),
            matrix of coordinates, v is the number of vertices.
    w : a float, by default 0.5,
        weight in [0,1] given to hemi-ellipsoids.
    spherefile : string, by default 'sphere.obj',
        filename of a sphere surface for the left hemisphere. If
        it is a *.obj file, it assumes that the triangulation of the
        right hemisphere is a mirror image; if it is an FS file,
        then it assumes it is identical. The default is 'sphere.obj'
        for a 40962 vertex (v=81924 for both hemispheres)
        icosahedral mesh, or 'lh.sphere' for a 163842 vertex
        (v=327684 for both hemispheres) icosahedral mesh.

    Returns
    -------
    surfw : a dictionary with key 'coord',
        surfw['coord'] : 2D numpy array of shape (3,v),
            matrix of inflated coordinates.
    """
    
    v = surf['coord'].shape[1]
    
    if v <= 81924:
    
        # MATLAB RAPPING FOR *obj FILE READ IN --> has to be changed...
        sphere_mat = eng.SurfStatReadSurf(spherefile)
        sphere = {}
        sphere['tri'] = np.array(sphere_mat['tri']) 
        sphere['coord'] = np.array(sphere_mat['coord'])
    
        if v == 81924:
            sys.exit("NOT YET IMPLEMENTED...")
        else:
            if surf['coord'][0,:].mean() / abs(surf['coord'][0,:]).mean() < -0.5:
                sys.exit("NOT YET IMPLEMENTED...")
            else:
                row1 = -sphere['coord'][0,:] * (sphere['coord'][0,:] < 0)                                                   
                row1 = row1.reshape(1, len(row1))
                sphere['coord'] = np.concatenate((row1, sphere['coord'][1:3,:]))
    else:
        sys.exit("NOT YET IMPLEMENTED...")
        
    maxs = surf['coord'].max(1)
    mins = surf['coord'].min(1)
    maxsp = sphere['coord'].max(1)
    minsp = sphere['coord'].min(1)
    surfw = surf

    for i in range(0,3): 
        surfw['coord'][i,:] = ((sphere['coord'][i,:] - minsp[i]) / \
        (maxsp[i]-minsp[i]) * (maxs[i]-mins[i]) + mins[i]) * w + \
        surf['coord'][i,:]*(1-w) 

    return surfw
    
    

