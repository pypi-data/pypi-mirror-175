import pathlib
import json

_CWDIR = pathlib.Path(__file__).parent


with open(_CWDIR.joinpath("elem_z_map.json"), "r") as fp:
    ELEM_Z_MAP = json.load(fp)
    Z_ELEM_MAP = {v: k for k,v in ELEM_Z_MAP.items()}


def get_element_name(z: int):
    """Return the chemical element name from the atomic number."""
    return Z_ELEM_MAP.get(z, None)


def get_element_number(name: str):
    """Return the atomic number of the given chemical element name."""
    return ELEM_Z_MAP.get(name, None)
