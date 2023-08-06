# -*- coding: utf-8 -*-
"""Module for the JPL GPS data products.

Supports ROTI data produced at JPL from International
GNSS Service Total Electron Content (TEC)

The rate of TEC index (ROTI) characterizes TEC fluctuations observed along
receiver-to-satellite line of sight links over a 5-minute interval.
The measurement is obtained by processing GNSS dual-frequency phase data and
computing the standard deviation of the rate of TEC change over that interval
after removing its background variation trend.

ROTI data are provided as global maps using a 2.5 x 5 degree (geographic
latitude x longitude) grid. The median ROTI value is calculated in each bin.
GNSS data contributing to the ROTI computation are primarily collected from
the global network of International GNSS Service and the regional network of
Continuous Operating Reference Station (CORS).

References
----------
Pi, X., A. J. Mannucci, U. J. Lindqwister, and C. M. Ho, Monitoring of global
ionospheric irregularities using the worldwide GPS network, Geophys. Res.
Lett., 24, 2283, 1997.

Pi, X., F. J. Meyer, K. Chotoo, Anthony Freeman, R. G. Caton, and C. T.
Bridgwood, Impact of ionospheric scintillation on Spaceborne SAR observations
studied using GNSS, Proc. ION-GNSS, pp.1998-2006, 2012.


Properties
----------
platform
    'jpl'
name
    'gps'
tag
    ['roti']
inst_id
    None supported

Warnings
--------
- The cleaning parameters for the instrument are still under development.

"""

import datetime as dt
import functools

import pysat
from pysat.instruments.methods import general as mm_gen

from pysatNASA.instruments.methods import cdaweb as cdw
from pysatNASA.instruments.methods import general as mm_nasa
from pysatNASA.instruments.methods import gps as mm_gps

# ----------------------------------------------------------------------------
# Instrument attributes

platform = 'jpl'
name = 'gps'
tags = {'roti': 'Rate of change in TEC'}
inst_ids = {'': ['roti']}
pandas_format = False
# ----------------------------------------------------------------------------
# Instrument test attributes

_test_dates = {'': {'roti': dt.datetime(2013, 1, 1)}}

# ----------------------------------------------------------------------------
# Instrument methods


def init(self):
    """Initialize the Instrument object with instrument specific values.

    Runs once upon instantiation.

    """

    pysat.logger.info('')
    self.acknowledgements = mm_gps.ackn_str
    self.references = '\n'.join((mm_gps.refs['mission'],
                                 mm_gps.refs['roti15min_jpl']))

    return


# No cleaning, use standard warning function instead
clean = mm_nasa.clean_warn

# ----------------------------------------------------------------------------
# Instrument functions
#
# Use the default CDAWeb and pysat methods

# Set the list_files routine
fname = 'gps_roti15min_jpl_{year:4d}{month:02d}{day:02d}_v{version:02d}.cdf'
supported_tags = {'': {'roti': fname}}
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)

# Set the load routine
load = functools.partial(cdw.load, pandas_format=pandas_format)

# Set the download routine
basic_tag = {'remote_dir': '/pub/data/gps/roti15min_jpl/{year:4d}/',
             'fname': fname}
download_tags = {'': {'roti': basic_tag}}
download = functools.partial(cdw.download, supported_tags=download_tags)

# Set the list_remote_files routine
list_remote_files = functools.partial(cdw.list_remote_files,
                                      supported_tags=download_tags)
