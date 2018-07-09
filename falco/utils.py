import numpy as np
import itertools


def ceil_even(x_in):
    """Compute the next highest even integer above the input

    Parameters
    ----------
    x_in : float
        Scalar value

    Returns
    --------
    x_out : integer
        Even-valued integer
    """

    return int(2*np.ceil(0.5*x_in))

def ceil_odd(x_in):
    """Compute the next highest odd integer above the input

    Parameters
    ----------
    x_in : float
        Scalar value

    Returns
    --------
    x_out : integer
        Odd-valued integer
    """
    x_out = int(np.ceil(x_in))
    if x_out % 2 == 0: x_out +=1
    return x_out

def padOrCropEven(Ain, Ndes, **kwargs):
    """
    Pad or crop an even-sized input matrix to the desired size.

    Parameters
    ----------
    Ain : np.ndarray
        Rectangular or square input array with even size along each dimension
    Ndes : int
        Desired, even number of points across output array.  The output array will be
        padded/cropped to a square shape.

    Returns
    -------
    Aout : np.ndarray
        Square, even-sized padded or cropped array
    """
    extrapval = kwargs.get('extrapval', 0)  # Value to use for extrapolated points
    Ny0, Nx0 = Ain.shape

    if Nx0 % 2 or Ny0 % 2:  # Size of input array is odd along at least one dimension
        raise ValueError('Input is not an even-sized array')
    elif Nx0 != Ny0:
        raise ValueError('Input is not square')
    elif not isinstance(Ndes, int):
        raise ValueError('Wrong number of dimensions specified for output')

    if min(Nx0, Ny0) > Ndes:  # Output array is smaller than input, so crop
        Aout = Ain[(Ny0 - Ndes) // 2:(Ny0 + Ndes) // 2, (Nx0 - Ndes) // 2:(Nx0 + Ndes) // 2]
    elif max(Nx0, Ny0) < Ndes:  # Output array is bigger than input, so pad
        pad_x = (Ndes - Nx0) // 2
        pad_y = (Ndes - Ny0) // 2
        Aout = np.pad(Ain, (pad_y, pad_x), mode='constant', constant_values=extrapval)
    else:  # Do nothing
        Aout = Ain

    return Aout


def allcomb(*args, **kwargs):
    """
    Compute the Cartesian product of a series of iterables, i.e. the list consisting of all n-tuples
    formed by choosing one element from each of the n inputs.  The output list will have
    have length (P1 x P2 x ... x PN), where P1, P2, ..., PN are the lengths of the N input lists.

    Examples:
        allcomb([1, 3, 5], [-3, 8], [0, 1]) % numerical input:
            [(1, -3, 0), (1, -3, 1), (1, 8, 0), (1, 8, 1), (3, -3, 0), (3, -3, 1), (3, 8, 0),
            (3, 8, 1), (5, -3, 0), (5, -3, 1), (5, 8, 0), (5, 8, 1)]

        allcomb('abc','XY') % character arrays
            [('a', 'X'), ('a', 'Y'), ('b', 'X'), ('b', 'Y'), ('c', 'X'), ('c', 'Y')]

        allcomb('xy', [65, 66]) % a combination
            [('x', 65), ('x', 66), ('y', 65), ('y', 66)]  % a 4-by-2 character array

    Parameters
    ----------
    args
        An arbitrary long series of iterables.  May be of different lengths and types.

    Returns
    -------
    list of tuple
        Cartesian product of input lists (explained above)
    """
    return list(itertools.product(*args))
