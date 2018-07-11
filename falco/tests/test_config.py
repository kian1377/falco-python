import numpy as np
import os
import scipy.io
import falco.config.ModelParameters
import falco.config.DeformableMirrorParameters
import falco.tests.test_masks

def _get_default_LC_config_data():
    _LC_default_LC_config_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_default_LC_config_data.mat")
    return scipy.io.loadmat(_LC_default_LC_config_data_file, struct_as_record=False, squeeze_me=True)

def _recursive_compare(c1, c2, exceptions=[], only_check_common=False):
    if type(c1) in (int,float,str) or type(c2) in (int,float,str):
        assert(c1==c2)
        return

    if type(c1) in (list, np.ndarray):
        try:
            assert(np.allclose(c1,c2))
        except MemoryError:
            assert(len(c1) == len(c2))
            for i in range(len(c1)):
                _recursive_compare(c1[i], c2[i], exceptions, only_check_common)
        return

    c1_k = [k for k in dir(c1) if k[0]!="_" and not k in exceptions]
    c2_k = [k for k in dir(c2) if k[0]!="_" and not k in exceptions]

    assert(only_check_common or (set(c1_k) == set(c2_k)))

    for k in c1_k:
        if k in exceptions or (only_check_common and not k in c2_k):
            continue
        v1 = eval("c1."+k)
        v2 = eval("c2."+k)

        _recursive_compare(v1,v2,exceptions,only_check_common)

def test_default_LC_config():
    #Default config generated by Python
    mp1 = falco.config.ModelParameters()
    dm1 = falco.config.DeformableMirrorParameters()
    #Default config generated by MATLAB
    data = _get_default_LC_config_data()
    mp2 = data["mp"]
    dm2 = data["DM"]
    #Python class generated from a MATLAB struct
    mp3 = falco.config.ModelParameters(mat_struct=mp2)
    dm3 = falco.config.DeformableMirrorParameters(mat_struct=dm2)

    _recursive_compare(mp1,mp2,exceptions=["init_ws","get_PSF_norm_factor","runLabel"])
    _recursive_compare(mp1,mp3,exceptions=["init_ws","get_PSF_norm_factor","runLabel"])
    _recursive_compare(mp2,mp3,exceptions=["init_ws","get_PSF_norm_factor","runLabel"])

    _recursive_compare(dm1,dm2,exceptions=[])
    _recursive_compare(dm1,dm3,exceptions=[])
    _recursive_compare(dm2,dm3,exceptions=[])

def test_init_ws():
    mp1 = falco.config.ModelParameters()
    mp1.init_ws()

    mp2 = falco.tests.test_masks._get_LC_single_trial_mp_data()

    #Wttlam_ele are indices and MATLAB is one off
    exceptions=["Wttlam_ele","Wttlam_si","Wttlam_ti","inds"]
    _recursive_compare(mp1,mp2,exceptions=exceptions,only_check_common=True)
