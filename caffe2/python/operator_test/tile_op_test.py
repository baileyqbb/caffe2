from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

from hypothesis import given
import hypothesis.strategies as st

from caffe2.python import core
import caffe2.python.hypothesis_test_util as hu


class TestTile(hu.HypothesisTestCase):
    @given(M=st.integers(min_value=1, max_value=10),
           K=st.integers(min_value=1, max_value=10),
           N=st.integers(min_value=1, max_value=10),
           tiles=st.integers(min_value=1, max_value=3),
           axis=st.integers(min_value=0, max_value=2),
           **hu.gcs)
    def test_tile(self, M, K, N, tiles, axis, gc, dc):
        X = np.random.rand(M, K, N).astype(np.float32)

        op = core.CreateOperator(
            'Tile', ['X'], 'out',
            tiles=tiles,
            axis=axis,
        )

        def tile_ref(X, tiles, axis):
            dims = [1, 1, 1]
            dims[axis] = tiles
            tiled_data = np.tile(X, tuple(dims))
            return (tiled_data,)

        # Check against numpy reference
        self.assertReferenceChecks(gc, op, [X, tiles, axis],
                                   tile_ref)
        # Check over multiple devices
        self.assertDeviceChecks(dc, op, [X], [0])
        # Gradient check wrt X
        self.assertGradientChecks(gc, op, [X], 0, [0])


if __name__ == "__main__":
    import unittest
    unittest.main()
