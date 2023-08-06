# -*- coding: utf-8 -*-
"""Module for the DE2 LANG instrument.

Supports the Langmuir Probe (LANG) instrument on Dynamics Explorer 2 (DE2).

From CDAWeb:

The Langmuir Probe Instrument (LANG) was a cylindrical electrostatic probe that
obtained measurements of electron temperature, Te, and electron or ion
concentration, Ne or Ni, respectively, and spacecraft potential.  Data from
this investigation were used to provide temperature and density measurements
along magnetic field lines related to thermal energy and particle flows within
the magnetosphere-ionosphere system, to provide thermal plasma conditions for
wave-particle interactions, and to measure large-scale and fine-structure
ionospheric effects of energy deposition in the ionosphere.  The Langmuir Probe
instrument was identical to that used on the AE satellites and the Pioneer
Venus Orbiter. Two independent sensors were connected to individual adaptive
sweep voltage circuits which continuously tracked the changing electron
temperature and spacecraft potential, while autoranging electrometers adjusted
their gain in response to the changing plasma density. The control signals used
to achieve this automatic tracking provided a continuous monitor of the
ionospheric parameters without telemetering each volt-ampere (V-I) curve.
Furthermore, internal data storage circuits permitted high resolution, high
data rate sampling of selected V-I curves for transmission to ground to verify
or correct the inflight processed data. Time resolution was 0.5 seconds.


References
----------
J. P. Krehbiel, L. H. Brace, R. F. Theis, W. H. Pinkus, and R. B. Kaplan,
"The Dynamics Explorer 2 Langmuir Probe (LANG)", Space Sci. Instrum., 5,
493-502, 1981.

Properties
----------
platform
    'de2'
name
    'lang'
inst_id
    None Supported
tag
    None Supported


Warnings
--------
- Currently no cleaning routine.


"""

import datetime as dt
import functools

from pysat.instruments.methods import general as mm_gen

from pysatNASA.instruments.methods import cdaweb as cdw
from pysatNASA.instruments.methods import de2 as mm_de2
from pysatNASA.instruments.methods import general as mm_nasa

# ----------------------------------------------------------------------------
# Instrument attributes

platform = 'de2'
name = 'lang'
tags = {'': '500 ms cadence Langmuir Probe data'}
inst_ids = {'': ['']}

# ----------------------------------------------------------------------------
# Instrument test attributes

_test_dates = {'': {'': dt.datetime(1983, 1, 1)}}

# ----------------------------------------------------------------------------
# Instrument methods


# Use standard init routine
init = functools.partial(mm_nasa.init, module=mm_de2, name=name)

# No cleaning, use standard warning function instead
clean = mm_nasa.clean_warn

# ----------------------------------------------------------------------------
# Instrument functions
#
# Use the default CDAWeb and pysat methods

# Set the list_files routine
fname = 'de2_plasma500ms_lang_{year:04d}{month:02d}{day:02d}_v{version:02d}.cdf'
supported_tags = {'': {'': fname}}
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)

# Set the load routine
load = cdw.load

# Set the download routine
basic_tag = {'remote_dir': ''.join(('/pub/data/de/de2/plasma_lang',
                                    '/plasma500ms_lang_cdaweb/{year:4d}/')),
             'fname': fname}
download_tags = {'': {'': basic_tag}}
download = functools.partial(cdw.download, supported_tags=download_tags)

# Set the list_remote_files routine
list_remote_files = functools.partial(cdw.list_remote_files,
                                      supported_tags=download_tags)
