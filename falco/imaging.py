import falco
import numpy as np

def falco_get_PSF_norm_factor(mp):
    """
    Function to get the normalization factor for each model at each sub-band.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters

    Returns
    -------
    nothing
        Changes are made by reference to the structure mp

    """
    
    #AJER NOTE DEBUGGING mode only    
    if type(mp) is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
    pass
    
    """
    if type(mp) is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
        
    #--Initialize Model Normalizations
    if not hasattr(mp.Fend,'compact'):
         mp.Fend.compact = falco.config.EmptyObject() #--Initialize the new structure
    if not hasattr(mp.Fend,'eval'):
         mp.Fend.eval = falco.config.EmptyObject() #--Initialize the new structure
    if not hasattr(mp.Fend,'full'):
         mp.Fend.full = falco.config.EmptyObject() #--Initialize the new structure
    mp.Fend.compact.I00 = np.ones(mp.Nsbp) # Initial input before computing
    mp.Fend.eval.I00 =np.ones(mp.Nsbp) # Initial input before computing
    mp.Fend.full.I00 = np.ones((mp.Nsbp,mp.Nwpsbp)) # Initial input before computing

    modvar = falco.config.EmptyObject() #--Initialize the new structure
    modvar.zernIndex = 1
    modvar.whichSource = 'star'
    
    #--Compact Model Normalizations
    for si in range(mp.Nsbp):
        modvar.sbpIndex = si
        Etemp = falco.models.model_compact(mp, modvar,GETNORM=True)
        mp.Fend.compact.I00[si] = (np.abs(Etemp)**2).max()

    #--Compact Evaluation Model Normalizations
    for si in range(mp.Nsbp):
        modvar.sbpIndex = si
        Etemp = falco.models.model_compact(mp, modvar,GETNORM=True,EVAL=True)
        mp.Fend.eval.I00[si] = (np.abs(Etemp)**2).max()

    #--Full Model Normalizations (at points for entire-bandpass evaluation)
    if(mp.flagSim):
        for si in range(mp.Nsbp):
            for wi in range(mp.Nwpsbp):
                modvar.sbpIndex = si
                modvar.wpsbpIndex = wi
                Etemp = falco.models.model_full(mp, modvar,GETNORM=True)
                mp.Fend.full.I00[si,wi] = (np.abs(Etemp)**2).max()
    """

def falco_get_expected_summed_image(mp, cvar):
    """
    Returns summed image.

    Function to generate the expected broadband image over the entire
    bandpass by adding the model-based delta electric field on top of the
    current E-field estimate in each sub-bandpass.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    cvar: TBD
        TBD

    Returns
    -------
    TBD
        band-averaged image in units of normalized intensity
    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
    pass

def falco_get_gpct_sbp_image(mp, si):
    """
    Function to get an image in the specified sub-bandpass from the GPCT.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Normalized intensity in the sub-bandpass
        (i.e. approximate raw contrast but normalized 
        by a photometry measurement at a single offset)

    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
    pass

def falco_get_hcst_sbp_image(mp, si):
    """
    Function to get an image in the specified sub-bandpass from the Caltech
    HCST testbed. This function will need to be replaced in order to run on a
    different testbed. Note that the number of pixels per lambda*F# is
    predetermined. 

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Normalized intensity in the sub-bandpass
        (i.e. approximate raw contrast but normalized 
        by a photometry measurement at a single offset)

    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
    pass

def falco_get_image(mp, modvar):
    """
    Wrapper function to obtain a real image from a testbed camera or
    a simulated image with noise using the full model.
    For a single sub-bandpass only.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    modvar: TBD
        Structure of model variables

    Returns
    -------
    TBD
        TBD

    """
    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')
    pass

def falco_get_sbp_image(mp, si):
    """
    Function to get an image in the specified sub-bandpass.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Sub-bandpass image in units of normalized intensity

    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    if mp.flagSim:
        ImNI = falco_get_sim_sbp_image(mp, si)
    else:
        ImNI = falco_get_testbed_sbp_image(mp, si)

    return ImNI

def falco_get_sbp_image_fiber(mp, si):
    """
    Function to get an image in the specified sub-bandpass from an optical fiber.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Sub-bandpass image in units of normalized intensity
    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    if mp.flagSim:
        ImNI = falco_get_sim_sbp_image_fiber(mp, si)
    else:
        raise NotImplementedError('Testbed functionality not implemented for fibers yet.')

    return ImNI

def falco_get_sim_sbp_image(mp, si):
    """
    Function to get an image in the specified sub-bandpass.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Sub-bandpass image in units of normalized intensity
    """
    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    pass

def falco_get_sim_sbp_image_fiber(mp, si):
    """
    Function to get an image in the specified sub-bandpass.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Sub-bandpass image in units of normalized intensity

    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    pass

def falco_get_summed_image(mp):
    """
    Function to get a broadband image over the entire bandpass by summing the
    sub-bandpass images.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters

    Returns
    -------
    TBD
        band-averaged image in units of normalized intensity

    """

    if type(mp) is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    ### Compute the DM surfaces outside the full model to save some time
    
    ### Create image
    # SFF NOTE:
    Ibandavg = np.zeros((56,56))
    #for si in range(mp.Nsbp):
    #    Ibandavg = Ibandavg + mp.sbp_weights[si] * falco_get_sbp_image(mp, si);

    return Ibandavg


def falco_get_summed_image_fiber(mp):
    """
    Function to get a summed image from the back end of a single-mode optical
    fiber(s).

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters

    Returns
    -------
    TBD
        Total intensity across the bandpass from all fibers.
    
    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    pass

def falco_get_testbed_sbp_image(mp, si):
    """
    Function to get an image in the specified sub-bandpass from a testbed.
    This function calls an equivalent sub-function depending on mp.testbed.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    si: int
        Index of sub-bandpass for which to take the image

    Returns
    -------
    TBD
        Normalized intensity in the sub-bandpass
               (i.e. approximate raw contrast but normalized
           by a photometry measurement at a single offset)

    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    pass

def falco_sim_image_compact_offaxis(mp, x_offset, y_offset, **kwargs):
    """
    Function to return the perfect-knowledge E-field and summed intensity for
    the compact model.

    Parameters
    ----------
    mp: falco.config.ModelParameters
        Structure of model parameters
    x_offset: int
        TBD
    y_offset: int
        TBD
    kwargs: TBD
        TBD

    Returns
    -------
    TBD
        Tuple with E-field and summed intensity for compact model
    """

    if mp is not falco.config.ModelParameters:
        raise TypeError('Input "mp" must be of type ModelParameters')

    pass
