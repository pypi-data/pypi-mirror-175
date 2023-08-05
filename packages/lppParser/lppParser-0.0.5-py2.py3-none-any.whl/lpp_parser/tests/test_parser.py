#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lpp_parser import get_lpp_info

lpp_file1 = '44S_target8mm.lpp'
lpp_file2 = 'SetB.65.00-1H_E262_C15mm_36Ar__c_aris__PSv05_KFv3.5.0__CB1s-R4003.lpp'


def test_get_lpp_info_1():
    d = get_lpp_info(lpp_file1)
    settings = d['settings']
    assert settings['primary_beam'] == {
        'A': 48,
        'name': 'Ca',
        'Q': 20,
        'Z': 20,
        'Ek': 220.0,
        'power': 0.082,
        'rf_freq': 40.25,
        'tau': 0.261
    }
    assert settings['frag_beam'] == {'A': 44, 'name': 'S', 'Z': 16}


def test_get_lpp_info_2():
    d = get_lpp_info(lpp_file2)
    settings = d['settings']
    assert settings['primary_beam'] == {
        'A': 36,
        'name': 'Ar',
        'Q': 18,
        'Z': 18,
        'Ek': 262.0,
        'power': 10.0,
        'rf_freq': 40.25,
        'tau': 0.26
    }
    assert settings['frag_beam'] == {'A': 1, 'name': 'H', 'Z': 1}
