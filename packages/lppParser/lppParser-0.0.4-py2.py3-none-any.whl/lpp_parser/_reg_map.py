import re
from functools import partial
from .data import ELEM_Z_MAP

# map of regex
# [settings], primary beam, and frag beam
_AZQ_REG = r'.*A,Z,Q.*=\ *(\d+)(\D+)(\d+)\+.*'  # 1:A, 2:name, 3:Q
_EK_REG = r'.*Energy.*=\ *(\d+(?:\.\d+)?).*'  # 1: Energy in MeV/u
_PWR_REG = r'.*Intensity.*=\ *(\d+(?:\.\d+)?).*'  # 1: Power in kW
_RF_FREQ_REG = r'.*RF.*=\ * (\d+(?:\.\d+)?).*'  # 1: RF frequency in MHz
_TAU_REG = r'.*Bunch.*=\ *(\d+(?:\.\d+)?).*'  # 1: Bunch length in ns
_ISO_REG = r'.*Settings.*=\ *(\d+)([a-zA-Z]+).*'  # Settings on A,Z, 1: A, 2: name

REG_MAP = {
    # match_key: (regex, (tuple of attribs, type tuple for all groups)
    'PRIM_BEAM_NAME': (_AZQ_REG, (('A', 'name', 'Q'), (int, str, int))),
    'PRIM_BEAM_EK': (_EK_REG, (('Ek', ), (float, ))),
    'PRIM_BEAM_PWR': (_PWR_REG, (('power', ), (float, ))),
    'RF_FREQ': (_RF_FREQ_REG, (('rf_freq', ), (float, ))),
    'BUNCH_LENGTH': (_TAU_REG, (('tau', ), (float, ))),
    'FRAG_BEAM_NAME': (_ISO_REG, (('A', 'name'), (int, str))),
}


def get_params(match_key: str, line: str):
    """Return matched parameters as a dict.
    """
    _regex, _tuple_of_key_type = REG_MAP[match_key]
    r = re.match(_regex, line)
    params = {
        k: partial(t, g)()
        for g, k, t in zip(r.groups(), *_tuple_of_key_type)
    }
    if 'name' in params:
        # add 'Z' if 'name' key presents
        params['Z'] = ELEM_Z_MAP[params['name']]  # int
    return params
