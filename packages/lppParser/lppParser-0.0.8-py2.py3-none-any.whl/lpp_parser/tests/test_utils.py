#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from lpp_parser.data import z2sym, sym2z, sym2name, name2sym


def test_z2sym():
    assert z2sym(89) == 'Ac'
    assert z2sym(112) == 'Cn'
    assert z2sym(999) == None


def test_sym2z():
    assert sym2z('Ac') == 89
    assert sym2z('Cn') == 112
    assert sym2z('Zzz') == None


def test_sym2name():
    assert sym2name('Ac') == 'Actinium'
    assert sym2name('Cn') == 'Copernicium'
    assert sym2name('Zzz') == None


def test_name2sym():
    assert name2sym('Actinium') == 'Ac'
    assert name2sym('Copernicium') == 'Cn'
    assert name2sym('Zzzzzzz') == None
