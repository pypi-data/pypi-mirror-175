import re
from functools import partial
from .data import sym2z, sym2name

# map of regex
# [settings], primary beam, and frag beam

# 1: A, 2: symbol, 3: Q
_AZQ_REG = r'.*A,Z,Q.*=\ *(\d+)([a-zA-Z]+)\ *(\d+)\+.*'

# 1: Energy in MeV/u
_EK_REG = r'.*Energy.*=\ *(\d+(?:\.\d+)?).*'

# 1: Power in kW
_PWR_REG = r'.*Intensity.*=\ *(\d+(?:\.\d+)?).*'

# 1: RF frequency in MHz
_RF_FREQ_REG = r'.*RF.*=\ * (\d+(?:\.\d+)?).*'

# 1: Bunch length in ns
_TAU_REG = r'.*Bunch.*=\ *(\d+(?:\.\d+)?).*'

# Settings on A,Z, 1: A, 2: symbol
_ISO_REG = r'.*Settings.*=\ *(\d+)([a-zA-Z]+).*'


REG_MAP = {
    # match_key: (regex, (tuple of attribs, type tuple for all groups)
    'PRIM_BEAM_NAME': (_AZQ_REG, (('A', 'symbol', 'Q'), (int, str, int))),
    'PRIM_BEAM_EK': (_EK_REG, (('Ek', ), (float, ))),
    'PRIM_BEAM_PWR': (_PWR_REG, (('power', ), (float, ))),
    'RF_FREQ': (_RF_FREQ_REG, (('rf_freq', ), (float, ))),
    'BUNCH_LENGTH': (_TAU_REG, (('tau', ), (float, ))),
    'FRAG_BEAM_NAME': (_ISO_REG, (('A', 'symbol'), (int, str))),
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
    if 'symbol' in params:
        # add 'Z' and 'name' if 'symbol' key presents
        symbol = params['symbol']
        params['Z'] = sym2z(symbol)  # int
        params['name'] = sym2name(symbol)  # str
    return params
