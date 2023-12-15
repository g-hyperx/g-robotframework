from requests import put, post
import json

def _get_asset_string_variable(vname=None, tenantId=None, directoryId=None, apigwUrl=None):
    if vname is None:
        raise AssertionError('None variable name!')
    if tenantId is None:
        raise AssertionError('None variable tenant id!')
    if directoryId is None:
        raise AssertionError('None variable directory id!')
    if apigwUrl is None:
        raise AssertionError('None variable api gateway url!')
    
    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    resp = post(f"{apigwUrl}/kernel/asset/get-variable", json=data)
    
    if resp.status_code == 200:
        return resp.content.decode()
    else:
        raise AssertionError(resp.content.decode())

def _get_asset_integer_variable(vname=None, tenantId=None, directoryId=None, apigwUrl=None):
    if vname is None:
        raise AssertionError('None variable name!')
    if tenantId is None:
        raise AssertionError('None variable tenant id!')
    if directoryId is None:
        raise AssertionError('None variable directory id!')
    if apigwUrl is None:
        raise AssertionError('None variable api gateway url!')
    
    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    resp = post(f"{apigwUrl}/kernel/asset/get-variable", json=data)

    if resp.status_code == 200:
        return int(float(resp.content.decode()))
    else:
        raise AssertionError(resp.content.decode())

def _get_asset_float_variable(vname=None, tenantId=None, directoryId=None, apigwUrl=None):
    if vname is None:
        raise AssertionError('None variable name!')
    if tenantId is None:
        raise AssertionError('None variable tenant id!')
    if directoryId is None:
        raise AssertionError('None variable directory id!')
    if apigwUrl is None:
        raise AssertionError('None variable api gateway url!')

    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    resp = post(f"{apigwUrl}/kernel/asset/get-variable", json=data)

    if resp.status_code == 200:
        return float(resp.content.decode())
    else:
        raise AssertionError(resp.content.decode())
    