import unittest

from analysis import Feature
from theory import (LMHologram, Sphere)
from utilities import coordinates

import os
import cv2
import numpy as np

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_IMAGE = os.path.join(THIS_DIR, 'data/crop.png')


class TestFeature(unittest.TestCase):

    def setUp(self):
        data = cv2.imread(TEST_IMAGE, 0).astype(float)
        data /= np.mean(data)
        coords = coordinates(data.shape)
        model = LMHologram(wavelength=0.447, magnification=0.048, n_m=1.34)
        self.data = data
        self.coords = coords
        self.feature = Feature(data=data, coordinates=coords,
                               model=model, percentpix=0.1)
        model.particle.r_p = [data.shape[0]//2, data.shape[1]//2, 330]
        model.particle.a_p = 1.1
        model.particle.n_p = 1.4

    def test_data(self):
        self.feature.data = self.data
        self.assertEqual(self.data.size, self.feature.data.size)

    def test_residuals(self):
        self.feature.data = self.data
        self.feature.optimize()
        res = self.feature.residuals()
        self.assertEqual(self.data.size, res.size)

    def test_model(self):
        model = LMHologram()
        self.feature.model = model
        self.assertIs(self.feature.model, model)

    def test_getsetparticle(self):
        z_p = 200.
        p = self.feature.particle
        p.z_p = z_p
        self.feature.particle = p
        self.assertEqual(self.feature.particle.z_p, z_p)


if __name__ == '__main__':
    unittest.main()
