#!/usr/bin/python


import unittest


from pymatgen.core import Structure
from pymatgen.core.lattice import Lattice
from pymatgen.io.smartio import CifParser
from pymatgen import write_structure
from pymatgen.core.surface import Slab, SurfaceGenerator
import os
import itertools
import numpy as np



def get_path(path_str):
    forder = str(os.getcwd()) + "/surface_tests"
    path = os.path.join(forder, path_str)
    print path
    return path

class SlabTest(unittest.TestCase):

    def setUp(self):
        C1 = CifParser(get_path("ZnO-wz.cif"))
        zno = C1.get_structures(primitive=False)
        zno1 = zno[0]
        zno55 = SurfaceGenerator(zno1, [1, 0, 0], 5, 5, lll_reduce=False,
                                 standardize=False).get_slab()
        #print zno55[0]
        #write_structure(zno55[0], "surface_tests/ZnO55.cif")
        self.zno1 = zno1
        self.zno55 = zno55
        self.h = Structure(Lattice.cubic(3), ["H"],
                            [[0, 0, 0]])
        self.libcc = Structure(Lattice.cubic(3.51004), ["Li", "Li"],
                               [[0, 0, 0], [0.5, 0.5, 0.5]])
        Li_Fe_P_O4 = CifParser(get_path("LiFePO4.cif"))
        self.lifepo4 = (Li_Fe_P_O4.get_structures(primitive = False)[0])
        Li_Fe_P_O4_compare = CifParser(get_path("LiFePO4_010_original_3.005.cif"))
        self.lifepo4_compare = (Li_Fe_P_O4_compare.get_structures(primitive = False)[0])

    def test_init(self):
        zno_slab = Slab(self.zno55, self.zno55.miller_index, 0,
                        self.zno55.normal, self.zno55.scale_factor,
                        self.zno1, self.zno55.min_slab_size,
                        self.zno55.min_vac_size)
        m =self.zno55.lattice.matrix
        area = np.linalg.norm(np.cross(m[0], m[1]))
        self.assertAlmostEqual(zno_slab.surface_area, area)
        self.assertEqual(zno_slab.lattice.lengths_and_angles,
                         self.zno55.lattice.lengths_and_angles)
        self.assertEqual(zno_slab.normal.all, self.zno55.normal.all)
        self.assertEqual(zno_slab.parent.composition, self.zno1.composition)
        self.assertEqual(len(zno_slab), 8)

    def test_add_adsorbate_atom(self):
        zno_slab = Slab(self.zno55, self.zno55.miller_index,
                        0, self.zno55.normal, self.zno55.scale_factor,
                        self.zno1, self.zno55.min_slab_size, self.zno55.min_vac_size)
        zno_slab.add_adsorbate_atom([1], 'H', 1)

        self.assertEqual(len(zno_slab), 9)
        self.assertEqual(str(zno_slab[8].specie),'H')
        self.assertAlmostEqual(zno_slab.get_distance(1,8), 1)
        self.assertTrue(zno_slab[8].c>zno_slab[0].c)
        m =self.zno55.lattice.matrix
        area = np.linalg.norm(np.cross(m[0], m[1]))
        self.assertAlmostEqual(zno_slab.surface_area, area)
        self.assertEqual(zno_slab.lattice.lengths_and_angles,
                         self.zno55.lattice.lengths_and_angles)
        self.assertEqual(zno_slab.normal.all, self.zno55.normal.all)

if __name__ == "__main__":
    unittest.main()