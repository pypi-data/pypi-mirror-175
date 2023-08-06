#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read .lpp file.
"""
import re

from ._reg_map import get_params


def get_lpp_info(filepath: str):
    """Return a list of interested info from the given .lpp file.
    """
    info_dict = {
        'settings': {
            'primary_beam': {},
            'frag_beam': {},
        },
    }
    processed_nline = 0
    with open(filepath, "r") as fp:
        line = fp.readline()
        while line:
            processed_nline += 1
            if line.strip().startswith('[settings]'):
                print(f"{processed_nline}: hit [settings] section")
                _line1 = fp.readline()  # A,Z,Q
                info_dict['settings']['primary_beam'].update(
                    get_params('PRIM_BEAM_NAME', _line1))
                _line2 = fp.readline()  # Energy, MeV/u
                info_dict['settings']['primary_beam'].update(
                    get_params('PRIM_BEAM_EK', _line2))
                _line3 = fp.readline()  # Intensity (Power), kW
                info_dict['settings']['primary_beam'].update(
                    get_params('PRIM_BEAM_PWR', _line3))
                _line4 = fp.readline()  # RF frequency, MHz
                info_dict['settings']['primary_beam'].update(
                    get_params('RF_FREQ', _line4))
                _line5 = fp.readline()  # Bunch length, ns
                info_dict['settings']['primary_beam'].update(
                    get_params('BUNCH_LENGTH', _line5))
                _line6 = fp.readline()  # Settings on A, Z (isotope)
                info_dict['settings']['frag_beam'].update(
                    get_params('FRAG_BEAM_NAME', _line6))
            line = fp.readline()
    return info_dict


if __name__ == '__main__':
    lpp_filepath = "tests/44S_target8mm.lpp"
    get_lpp_info(lpp_filepath)
