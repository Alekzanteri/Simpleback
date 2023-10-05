#calibration.py
#Note that this file is under Razorback license! Check https://github.com/BRGM/razorback for more info.

from pathlib import Path
import re
import numpy as np
import scipy.interpolate
import os
from razorback.data import get_data_file
import pathlib


__all__ = ['metronix']

abs_path=pathlib.Path(__file__).parent.resolve()#path of this exact file.
rel_path=r'metronix_calibration'#metronix calibration file


METRONIX_DATA_PATH = os.path.join(abs_path, rel_path)

METRONIX_CHOPPER_ON_LIMIT = 512.
METRONIX_VERSION_PATTERN = r".*(MFS\d\d).*"
METRONIX_ALPHA_MAP = {'MFS06': 4.0, 'MFS07': 32.0}


def metronix(filename, sampling_rate, chopper_on_limit=None, version_pattern=None, alpha_map=None):
    """ 
   This part is copied from Razorback code with few minor changes. This is needed for calibration of metronix files.

    """

    def start_stop(lines, mark):
        pattern = r'\s+'.join(re.split(r'\s+', mark.lower()))
        start = next(i for (i, l) in enumerate(lines, 1)
                     if re.match(pattern, l.lower().strip()))
        stop = [i for (i, l) in enumerate(lines[start:], start)
                if not l.strip()]
        stop = (stop or [None])[0]
        return start, stop

    def version(filename):
        name = Path(filename).stem
        m = re.match(version_pattern, name)
        if m is None:
            raise ValueError(f"cannot find version of calibration file '{filename}'")
        return m.group(1)

    def cal_mp(freq, module, phase):
        return freq * module * np.exp(1j * phase * np.pi/180.)

    def calibration(table, filename, chopper, alpha_map):
        freq = table[:, 0]
        calib = cal_mp(freq, table[:, 1], table[:, 2])
        tabuled = scipy.interpolate.interp1d(freq, calib, copy=False)

        vers = version(filename)
        if vers not in alpha_map:
            raise ValueError(
                f"unknown version '{vers}' of calibration file '{filename.name}'"
            )

        alpha = alpha_map[vers]
        freq_min = freq[0]
        mod_min = table[0, 1]

        def calib_func(f):
            if f < freq_min and chopper:
                phase = np.angle(f + 1j * alpha, deg=True)
                return cal_mp(f, mod_min, phase)
            return tabuled(f)

        return calib_func

    if chopper_on_limit is None:
        chopper_on_limit = METRONIX_CHOPPER_ON_LIMIT
    if version_pattern is None:
        version_pattern = METRONIX_VERSION_PATTERN
    if alpha_map is None:
        alpha_map = METRONIX_ALPHA_MAP
   
    filename = get_data_file(filename, METRONIX_DATA_PATH)
    with open(filename, 'r') as file:
        lines = file.readlines()

    chopper = sampling_rate <= chopper_on_limit
    mark = 'Chopper On' if chopper else 'Chopper Off'
    start, stop = start_stop(lines, mark)
    calib = calibration(np.loadtxt(lines[start:stop]), filename, chopper, alpha_map)
    return calib
