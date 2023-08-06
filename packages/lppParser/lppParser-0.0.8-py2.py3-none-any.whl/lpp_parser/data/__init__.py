import pathlib
import json

_CWDIR = pathlib.Path(__file__).parent


with open(_CWDIR.joinpath("sym_z_map.json"), "r") as fp:
    SYM_Z_MAP = json.load(fp)
    Z_SYM_MAP = {v: k for k,v in SYM_Z_MAP.items()}


with open(_CWDIR.joinpath("sym_name_map.json"), "r") as fp:
    SYM_NAME_MAP = json.load(fp)
    NAME_SYM_MAP = {v: k for k,v in SYM_NAME_MAP.items()}


def z2sym(z: int) -> str:
    """Return the chemical element symbol from the atomic number."""
    return Z_SYM_MAP.get(z, None)


def sym2z(sym: str) -> int:
    """Return the atomic number of the given chemical element symbol."""
    return SYM_Z_MAP.get(sym, None)


def sym2name(sym: str) -> int:
    """Return the name of a chemical element from the symbol."""
    return SYM_NAME_MAP.get(sym, None)


def name2sym(sym: str) -> int:
    """Return the symbol of a chemical element from the name."""
    return NAME_SYM_MAP.get(sym, None)
