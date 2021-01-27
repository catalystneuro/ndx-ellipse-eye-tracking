import os
from pynwb import load_namespaces, get_class
import ndx_events

# Set path of the namespace.yaml file to the expected install location
ndx_ellipse_eye_tracking_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-ellipse-eye-tracking.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_ellipse_eye_tracking_specpath):
    ndx_ellipse_eye_tracking_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-ellipse-eye-tracking.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_events.ndx_events_specpath)
load_namespaces(ndx_ellipse_eye_tracking_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level

EllipseSeries = get_class('EllipseSeries', 'ndx-ellipse-eye-tracking')
EllipseEyeTracking = get_class('EllipseEyeTracking', 'ndx-ellipse-eye-tracking')
