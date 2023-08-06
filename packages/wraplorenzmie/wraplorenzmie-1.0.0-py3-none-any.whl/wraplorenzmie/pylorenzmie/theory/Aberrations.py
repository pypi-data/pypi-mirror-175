import numpy as np


class Aberrations(object):
    '''
    Abstraction of geometric aberrations

    ...
    
    Properties
    ----------
    coordinates : numpy.ndarray
        [2, npts] array of x and y coordinates
    pupil : float
        radius of the imaging system's pupil [pixels]
    coefficients : numpy.ndarray
        9-element array containing coefficients of Zernike polynomials
        c[0] : piston
        c[1] : x tilt
        c[2] : y tilt
        c[3] : defocus
        c[4] : 0 degree astigmatism
        c[5] : 45 degree astigmatism
        c[6] : x coma
        c[7] : y coma
        c[8] : spherical aberration
    piston : float
    xtilt : float
    ytilt : float
    defocus : float
    xastigmatism : float
    yastigmatism : float
    xcoma : float
    ycoma : float
    spherical : float

    Methods
    -------
    phase() : numpy.ndarray
        [npts] array of phase aberration values at each coordinate
    field() : numpy.ndarray
        [npts] array of complex aberration field values
    '''

    def __init__(self,
                 coordinates=None,
                 pupil=None,
                 coefficients=None,
                 **kwargs):
        self._pupil = None
        self._coordinates = None
        self._phase = 0.
        self.pupil = pupil
        self.coordinates = coordinates
        self.coefficients = coefficients or np.zeros(9)

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates
        if (self._pupil is None) and not (coordinates is None):
            self._pupil = np.max(coordinates)
        self.update_polynomials()

    @property
    def pupil(self):
        return self._pupil

    @pupil.setter
    def pupil(self, pupil):
        self._pupil = pupil
        self.update_polynomials()

    def update_polynomials(self):
        self._update = True
        if (self.coordinates is None) or (self.pupil is None):
            return
        x = self.coordinates[0, :] / self.pupil
        y = self.coordinates[1, :] / self.pupil
        rhosq = x*x + y*y
        self.zernike = [1.,
                        x, y,
                        2.*rhosq - 1.,
                        (x - y)*(x + y), 2.*x*y,
                        (3.*rhosq - 2.) * x, (3.*rhosq - 2.) * y,
                        6.*rhosq * (rhosq - 1.) + 1.]

    @property
    def properties(self):
        p = dict(piston=self.piston,
                 xtilt=self.xtilt,
                 ytilt=self.ytilt,
                 defocus=self.defocus,
                 xastigmatism=self.xastigmatism,
                 yastigmatism=self.yastigmatism,
                 xcoma=self.xcoma,
                 ycoma=self.ycoma,
                 spherical=self.spherical)
        return p

    @properties.setter
    def properties(self, properties):
        for name, value in properties.items():
            if hasattr(self, name):
                setattr(self, name, value)
                 
    @property
    def coefficients(self):
        return self._coefficients

    @coefficients.setter
    def coefficients(self, coefficients):
        self._coefficients = coefficients
        self._update = True

    @property
    def piston(self):
        return self.coefficients[0]

    @piston.setter
    def piston(self, value):
        self.coefficients[0] = value
        self._update = True

    @property
    def xtilt(self):
        return self.coefficients[1]

    @xtilt.setter
    def xtilt(self, value):
        self.coefficients[1] = value
        self._update = True

    @property
    def ytilt(self):
        return self.coefficients[2]

    @ytilt.setter
    def ytilt(self, value):
        self.coefficients[2] = value
        self._update = True

    @property
    def defocus(self):
        return self.coefficients[3]

    @defocus.setter
    def defocus(self, value):
        self.coefficients[3] = value
        self._update = True

    @property
    def xastigmatism(self):
        return self.coefficients[4]

    @xastigmatism.setter
    def xastigmatism(self, value):
        self.coefficients[4] = value
        self._update = True

    @property
    def yastigmatism(self):
        return self.coefficients[5]

    @yastigmatism.setter
    def yastigmatism(self, value):
        self.coefficients[5] = value
        self._update = True

    @property
    def xcoma(self):
        return self.coefficients[6]

    @xcoma.setter
    def xcoma(self, value):
        self.coefficients[6] = value
        self._update = True

    @property
    def ycoma(self):
        return self.coefficients[7]

    @ycoma.setter
    def ycoma(self, value):
        self.coefficients[7] = value
        self._update = True

    @property
    def spherical(self):
        return self.coefficients[8]

    @spherical.setter
    def spherical(self, value):
        self.coefficients[8] = value
        self._update = True

    def phase(self):
        if not self._update:
            return self._phase
        phase = 0.
        for a_n, phase_n in zip(self.coefficients, self.zernike):
            if a_n != 0:
                phase += a_n * phase_n
        self._phase = phase
        self._update = False
        return phase

    def field(self):
        return np.exp(1.j * self.phase())
        
        
