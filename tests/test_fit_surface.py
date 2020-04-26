import sys
sys.path.insert(0,"../")
import pytest
import falco
import proper
import numpy as np
import testing_defaults_WFIRST_LC as DEFAULTS
import matplotlib.pyplot as plt


def test_fit_DM_surface_with_DM():
    mp = DEFAULTS.mp
    
    flagPlotDebug = False
    
    mp.path = falco.config.Object()
    mp.path.falco = './'  #--Location of FALCO
    mp.path.proper = './' #--Location of the MATLAB PROPER library
    
    ##--Output Data Directories (Comment these lines out to use defaults within falco-matlab/data/ directory.)
    mp.path.config = './' #--Location of config files and minimal output files. Default is [mainPath filesep 'data' filesep 'brief' filesep]
    mp.path.ws = './' # (Mostly) complete workspace from end of trial. Default is [mainPath filesep 'data' filesep 'ws' filesep];
    
    
    ## Step 3: Overwrite default values as desired
    
    mp.dm1.xtilt = 45
    mp.dm1.ytilt = 20
    mp.dm1.zrot = 30
    
    mp.dm1.xc = mp.dm1.Nact/2 - 1/2 + 1;
    mp.dm1.yc = mp.dm1.Nact/2 - 1/2 -1;
    
    
    ## Step 4: Initialize the rest of the workspace
    
    out = falco.setup.flesh_out_workspace(mp)
    
    
    ## Generate a DM surface and try to re-create the actuator commands
    
    normFac = 1;
    mp.dm1.V = normFac*np.random.rand(mp.dm1.Nact,mp.dm1.Nact)
    DM1Surf =  falco.dms.gen_surf_from_act(mp.dm1, mp.dm1.compact.dx, mp.dm1.compact.Ndm)
    
    if(flagPlotDebug):
        plt.figure(1); plt.imshow(mp.dm1.V); plt.colorbar(); plt.pause(0.1);
        plt.figure(2); plt.imshow(DM1Surf); plt.colorbar(); plt.pause(0.1);
    
    #--Fit the surface
    # DMSurf = pad_crop(DMSurf,500);
    Vout = falco.dms.fit_surf_to_act(mp.dm1,DM1Surf)/mp.dm1.VtoH
    Verror = mp.dm1.V - Vout;
    rmsVError = np.sqrt(np.mean(Verror.flatten()**2))/normFac;
    print('RMS fitting error to voltage map is %.2f%%.\n'%(rmsVError*100))
    
    if(flagPlotDebug):
        plt.figure(3); plt.imshow(Vout); plt.colorbar(); plt.pause(0.1);
        plt.figure(4); plt.imshow(Verror); plt.colorbar(); plt.pause(0.1);
        
    assert(rmsVError<2.5/100)
    
    
def test_fit_PSD_error_map_with_DM():

    mp = DEFAULTS.mp
    
    flagPlotDebug = False
    
    mp.path = falco.config.Object()
    mp.path.falco = './'  #--Location of FALCO
    mp.path.proper = './' #--Location of the MATLAB PROPER library
    
    ##--Output Data Directories (Comment these lines out to use defaults within falco-matlab/data/ directory.)
    mp.path.config = './' #--Location of config files and minimal output files. Default is [mainPath filesep 'data' filesep 'brief' filesep]
    mp.path.ws = './' # (Mostly) complete workspace from end of trial. Default is [mainPath filesep 'data' filesep 'ws' filesep];
    
    
    ## Step 3: Overwrite default values as desired
    
    mp.dm1.xtilt = 45
    mp.dm1.ytilt = 20
    mp.dm1.zrot = 30
    
    mp.dm1.xc = (mp.dm1.Nact/2 - 1/2) + 1;
    mp.dm1.yc = (mp.dm1.Nact/2 - 1/2) -1;
    
    
    ## Step 4: Initialize the rest of the workspace
    
    out = falco.setup.flesh_out_workspace(mp)
    
    
    ## Step 5
    
    # Determine the region of the array corresponding to the DM surface for use in the fitting.
    mp.dm1.V = np.ones((mp.dm1.Nact,mp.dm1.Nact))
    testSurf =  falco.dms.gen_surf_from_act(mp.dm1, mp.dm1.compact.dx, mp.dm1.compact.NdmPad)
    testArea = np.zeros(testSurf.shape)
    testArea[testSurf >= 0.5*np.max(testSurf)] = 1
    
    #--PROPER initialization
    pupil_ratio = 1 # beam diameter fraction
    wl_dummy = 1e-6 # dummy value needed to initialize wavelength in PROPER (meters)
    wavefront = proper.prop_begin(mp.dm1.compact.NdmPad*mp.dm1.dx, wl_dummy, mp.dm1.compact.NdmPad, pupil_ratio)
    # PSD Error Map Generation using PROPER
    amp = 9.6e-19; b = 4.0;
    c = 3.0;
    errorMap = proper.prop_psd_errormap( wavefront, amp, b, c, TPF=True )
    errorMap = errorMap*testArea;
    
    if(flagPlotDebug):
        plt.figure(1); plt.imshow(testArea); plt.colorbar(); plt.pause(0.1);
        plt.figure(2); plt.imshow(errorMap); plt.colorbar(); plt.pause(0.1);
    
    #--Fit the surface
    Vout = falco.dms.fit_surf_to_act(mp.dm1,errorMap)/mp.dm1.VtoH
    mp.dm1.V = Vout
    DM1Surf =  falco.dms.gen_surf_from_act(mp.dm1, mp.dm1.compact.dx, mp.dm1.compact.NdmPad)  
    surfError = errorMap - DM1Surf;
    rmsError = np.sqrt(np.mean((surfError[testArea==1].flatten()**2)))
    print('RMS fitting error to voltage map is %.2e meters.\n'%rmsError)
    
    if(flagPlotDebug):
        plt.figure(3); plt.imshow(Vout); plt.colorbar(); plt.pause(0.1);
        plt.figure(4); plt.imshow(DM1Surf); plt.colorbar(); plt.pause(0.1);
        plt.figure(5); plt.imshow(surfError); plt.colorbar(); plt.title('Difference'); plt.pause(0.1);

    assert(rmsError<2.0e-9)
