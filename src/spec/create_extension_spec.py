# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec
# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""Store the elliptical eye tracking output of DeepLabCut""",
        name="""ndx-ellipse-eye-tracking""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ben Dichter""".split(','))),
        contact=list(map(str.strip, """bdichter@lbl.gov""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.
    ns_builder.include_type('SpatialSeries', namespace='core')
    ns_builder.include_type('EyeTracking', namespace='core')
    ns_builder.include_type('TimeSeries', namespace='core')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    ellipse_series_spec = NWBGroupSpec(
        neurodata_type_def='EllipseSeries',
        neurodata_type_inc='SpatialSeries',
        doc='Information about an ellipse moving over time',
        datasets=[
            NWBDatasetSpec(
                name='data',  # override SpatialSeries 'data' dataset to be more explicit
                dtype='numeric',
                doc='The (x, y) coordinates of the center of the ellipse at each time point.',
                dims=('num_times', 'x, y'),
                shape=(None, 2),
            ),
            NWBDatasetSpec(
                name='area',
                dtype='float',
                doc='ellipse area',
                shape=(None, )
            ),
            NWBDatasetSpec(
                name='width',
                dtype='float',
                doc='width of ellipse',
                shape=(None, )
            ),
            NWBDatasetSpec(
                name='height',
                dtype='float',
                doc='height of ellipse',
                shape=(None, )
            ),
            NWBDatasetSpec(
                name='angle',
                dtype='float',
                doc='angle that ellipse is rotated by (phi)',
                shape=(None, )
            )
        ]
    )

    ellipse_eye_tracking_spec = NWBGroupSpec(
        neurodata_type_def='EllipseEyeTracking',
        neurodata_type_inc='EyeTracking',
        name=None,
        default_name='EyeTracking',
        doc='Stores detailed eye tracking information output from DeepLabCut',
        groups=[
            NWBGroupSpec(
                neurodata_type_inc=ellipse_series_spec,
                name=x,
                doc=x.replace('_', ' ')
            ) for x in ('eye_tracking', 'pupil_tracking', 'corneal_reflection_tracking')
        ] + [
            NWBGroupSpec(
                neurodata_type_inc='TimeSeries',
                name='likely_blink',
                doc='Indicator of whether there was a probable blink for this frame'
            )
        ],

    )

    # TODO: add all of your new data types to this list
    new_data_types = [ellipse_series_spec,  ellipse_eye_tracking_spec]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
