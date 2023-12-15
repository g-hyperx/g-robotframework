from requests import get, post
import json
from os import getenv


def _get_asset_string_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    tenantId = getenv("_TenantID")
    directoryId = getenv("_DirectoryID")
    apigwUrl = getenv("_APIGWUrl")
    
    agentType = getenv("AGENT_TYPE")

    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    if agentType == "serverless":
        apiKey = getenv("APIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agentless-APIKey": apiKey
                   },
                   json=data)
    else:
        apiKey = getenv("AGENTAPIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agent-API-Key": apiKey
                   },
                   json=data)

    if resp.status_code == 200:
        return resp.content.decode()
    else:
        raise AssertionError(resp.content.decode())


def _get_asset_integer_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    tenantId = getenv("_TenantID")
    directoryId = getenv("_DirectoryID")
    apigwUrl = getenv("_APIGWUrl")

    agentType = getenv("AGENT_TYPE")

    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    if agentType == "serverless":
        apiKey = getenv("APIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agentless-APIKey": apiKey
                   },
                   json=data)
    else:
        apiKey = getenv("AGENTAPIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agent-API-Key": apiKey
                   },
                   json=data)


    if resp.status_code == 200:
        return int(float(resp.content.decode()))
    else:
        raise AssertionError(resp.content.decode())


def _get_asset_float_variable(vname=None):
    if vname is None:
        raise AssertionError('None variable name!')

    tenantId = getenv("_TenantID")
    directoryId = getenv("_DirectoryID")
    apigwUrl = getenv("_APIGWUrl")

    agentType = getenv("AGENT_TYPE")

    data = {
        "Search": vname,
        "TenantID": tenantId,
        "DirectoryID": directoryId,
    }
    if agentType == "serverless":
        apiKey = getenv("APIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agentless-APIKey": apiKey
                   },
                   json=data)
    else:
        apiKey = getenv("AGENTAPIKEY")
        resp = get(f"{apigwUrl}/kernel/asset/get-variable",
                   headers={
                       "GHPX-Agent-API-Key": apiKey
                   },
                   json=data)


    if resp.status_code == 200:
        return float(resp.content.decode())
    else:
        raise AssertionError(resp.content.decode())
