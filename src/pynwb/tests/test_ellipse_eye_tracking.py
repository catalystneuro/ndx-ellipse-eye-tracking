import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file

from ndx_ellipse_eye_tracking import EllipseEyeTracking, EllipseSeries
from ndx_events import Events


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    return nwbfile


class TestEllipseEyeTracking(TestCase):

    def setUp(self):
        """Set up an NWB file."""
        self.nwbfile = set_up_nwbfile()
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_constructor(self):
        """Test that the constructors."""

        eye_tracking = EllipseSeries(
            name='eye_tracking',
            data=np.ones((100, 2)),
            reference_frame='nose',
            area=np.ones((100, )),
            width=np.ones((100, )),
            height=np.ones((100, )),
            angle=np.ones((100, )),
            timestamps=np.arange(100)/20
        )

        pupil_tracking = EllipseSeries(
            name='eye_tracking',
            data=np.ones((100, 2)),
            reference_frame='nose',
            area=np.ones((100, )),
            width=np.ones((100, )),
            height=np.ones((100, )),
            angle=np.ones((100, )),
            timestamps=eye_tracking
        )

        corneal_reflection_tracking = EllipseSeries(
            name='eye_tracking',
            data=np.ones((100, 2)),
            reference_frame='nose',
            area=np.ones((100, )),
            width=np.ones((100, )),
            height=np.ones((100, )),
            angle=np.ones((100, )),
            timestamps=eye_tracking
        )

        likely_blink = Events(timestamps=[1.0, 5.0, 6.0], name='likely_blink',
                              description='blinks')

        ellipse_eye_tracking = EllipseEyeTracking(
            eye_tracking=eye_tracking,
            pupil_tracking=pupil_tracking,
            corneal_reflection_tracking=corneal_reflection_tracking,
            likely_blink=likely_blink
        )

        return ellipse_eye_tracking

    def test_roundtrip(self):

        ellipse_eye_tracking = self.test_constructor()
        self.nwbfile.add_acquisition(ellipse_eye_tracking)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(ellipse_eye_tracking, read_nwbfile.acquisition['EllipseEyeTracking'])