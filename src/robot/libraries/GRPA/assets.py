from requests import put, post
from .constant import HOST
import json

def _get_asset_string_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    data = {
        "var_name": vname
    }
    resp = post(f"{HOST}/asset-variable", json=data)
    
    if resp.status_code == 200:
        return resp.content.decode()
    else:
        raise AssertionError(resp.content.decode())

def _get_asset_integer_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    data = {
        "var_name": vname
    }
    resp = post(f"{HOST}/asset-variable", json=data)

    if resp.status_code == 200:
        return int(float(resp.content.decode()))
    else:
        raise AssertionError(resp.content.decode())

def _get_asset_float_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    data = {
        "var_name": vname
    }
    resp = post(f"{HOST}/asset-variable", json=data)

    if resp.status_code == 200:
        return float(resp.content.decode())
    else:
        raise AssertionError(resp.content.decode())
    