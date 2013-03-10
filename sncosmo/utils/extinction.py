# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Extinction functions."""

import numpy as np

__all__ = ['extinction_ratio_ccm']

# Optical/NIR coefficients from Cardelli (1989)
c1_ccm = [1., 0.17699, -0.50447, -0.02427, 0.72085, 0.01979, -0.77530, 0.32999]
c2_ccm = [0., 1.41338, 2.28305, 1.07233, -5.38434, -0.62251, 5.30260, -2.09002]
      
# Optical/NIR coefficents from O'Donnell (1994)
c1_odonnell = [1., 0.104, -0.609, 0.701, 1.137, -1.718, -0.827, 1.647, -0.505]
c2_odonnell = [0., 1.952, 2.908, -3.989, -7.985, 11.102, 5.491, -10.805, 3.347]

def extinction_ratio_ccm(wavelength, r_v=3.1, optical_coeffs='odonnell'):
    r"""Return the Cardelli, Clayton, and Mathis (1989) extinction curve.

    This function returns the ratio of total extinction to selective
    extinction: A(wavelengths)/E(B-V), where E(B-V) is the B-V color
    excess.

    Parameters
    ----------
    wavelength : float or list_like
        Wavelength(s) in Angstroms. Values must be between 909.1 and 33,333.3,
        the range of validity of the extinction curve paramterization.
    r_v : float, optional
        Ratio of total to selective extinction: R_V = A_V / E(B-V).
        Default is 3.1.
    optical_coeffs : {'odonnell', 'ccm'}, optional
        If 'odonnell' (default), use the updated parameters for the optical
        given by O'Donnell (1994) [2]_. If 'ccm', use the original paramters
        given by Cardelli, Clayton and Mathis (1989) [1]_.

    Returns
    -------
    extinction_ratio : float or `~numpy.ndarray`
        Ratio of total to selective extinction: A(wavelengths) / E(B - V)
        at given wavelength(s). 

    Notes
    -----
    In [1]_ the mean :math:`R_V`-dependent extinction law, is parameterized
    as

    .. math::

       <A(\lambda)/A_V> = a(x) + b(x) / R_V

    where the coefficients a(x) and b(x) are functions of
    wavelength. At a wavelength of approximately 5494.5 Angstroms (a
    characteristic wavelength for the V band), a(x) = 1 and b(x) = 0,
    so that A(5494.5 Angstroms) = A_V. The parameterization in terms
    of A_V is somewhat arbitrary. In this function, the curve is
    paramterized by selective extinction E(B-V) (color excess between
    B and V bands) rather than A_V (total extinction in the V
    band). By definition, A_V = R_V * E(B-V), so the relationship
    between the two is

    .. math::

       <A(\lambda)/E(B-V)> =  R_V <A(\lambda) / A_V>  = R_V a(x) + b(x)

    The flux transmission fraction as a function of wavelength can then be
    obtained by

    .. math::

       T(\lambda) = (10^{-0.4 <A(\lambda)/E(B-V)>})^{E(B-V)}

    or in code, ``t = np.power(10. ** (-0.4 * extinction_ratio), c)``
    where ``c`` is E(B-V). The first term can be computed ahead of time
    for a given set of wavelengths.

    For an alternative to the CCM curve, see the extinction curve
    given in Fitzpatrick (1999) [6]_.

    **Notes from the IDL routine CCM_UNRED:**

    1. The CCM curve shows good agreement with the Savage & Mathis (1979)
       [5]_ ultraviolet curve shortward of 1400 A, but is probably
       preferable between 1200 and 1400 A.
    2. Many sightlines with peculiar ultraviolet interstellar extinction 
       can be represented with a CCM curve, if the proper value of 
       R(V) is supplied.
    3. Curve is extrapolated between 912 and 1000 A as suggested by
       Longo et al. (1989) [3]_.
    4. Valencic et al. (2004) [4]_ revise the ultraviolet CCM
       curve (3.3 -- 8.0 um-1).  But since their revised curve does
       not connect smoothly with longer and shorter wavelengths, it is
       not included here.


    References
    ----------
    .. [1] Cardelli, Clayton, and Mathis 1989, ApJ, 345, 245
    .. [2] O'Donnell 1994, ApJ, 422, 158
    .. [3] Longo et al. 1989, ApJ, 339,474
    .. [4] Valencic et al. 2004, ApJ, 616, 912
    .. [5] Savage & Mathis 1979, ARA&A, 17, 73
    .. [6] Fitzpatrick 1999, PASP, 111, 63
    """

    wavelength = np.asarray(wavelength)
    in_ndim = wavelength.ndim
    
    x = 1.e4 / wavelength.ravel()  # Inverse microns.
    if ((x < 0.3) | (x > 11.)).any():
        raise ValueError("extinction only defined in wavelength range"
                         " [909.091, 33333.3].")

    a = np.empty(x.shape, dtype=np.float)
    b = np.empty(x.shape, dtype=np.float)
  
    # Infrared
    idx = x < 1.1
    if idx.any():
        a[idx] = 0.574 * x[idx] ** 1.61
        b[idx] = -0.527 * x[idx] ** 1.61

    # Optical/NIR
    idx = (x >= 1.1) & (x < 3.3)
    if idx.any():
        xp = x[idx] - 1.82

        if optical_coeffs == 'odonnell':
            c1, c2 = c1_odonnell, c2_odonnell
        elif optical_coeffs == 'ccm':
            c1, c2 = c1_ccm, c2_ccm
        else:
            raise ValueError('Unrecognized optical_coeffs: {0!r}'
                             .format(optical_coeffs))

        # we need to flip the coefficients, because in polyval
        # c[0] corresponds to x^(N-1), but above, c[0] corresponds to x^0
        a[idx] = np.polyval(np.flipud(c1), xp)
        b[idx] = np.polyval(np.flipud(c2), xp)

    # Mid-UV
    idx = (x >= 3.3) & (x < 8.)
    if idx.any():
        xp = x[idx]
        a[idx] = 1.752 - 0.316 * xp - 0.104 / ((xp - 4.67) ** 2 + 0.341)
        b[idx] = -3.090 + 1.825 * xp + 1.206 / ((xp - 4.67) ** 2 + 0.263)

    idx = (x > 5.9) & (x < 8.)
    if idx.any():
        xp = x[idx] - 5.9
        a[idx] += -0.04473 * xp ** 2 - 0.009779 * xp ** 3
        b[idx] += 0.2130 * xp ** 2 + 0.1207 * xp ** 3

    # Far-UV
    idx = x >= 8.
    if idx.any():
        xp = x[idx] - 8.
        c1 = [ -1.073, -0.628,  0.137, -0.070 ]
        c2 = [ 13.670,  4.257, -0.420,  0.374 ]
        a[idx] = np.polyval(np.flipud(c1), xp)
        b[idx] = np.polyval(np.flipud(c2), xp)

    extinction_ratio = a * r_v + b
    if in_ndim == 0:
        return extinction_ratio[0]
    return extinction_ratio
