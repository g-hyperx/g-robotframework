import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def _logistics_api_request_download_file(url=None, source_id=None, token=None, path=None):
    payload = json.dumps({"source_id": source_id})
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    with open(path, "wb") as binary_file:
        binary_file.write(response.content)
        binary_file.close()


def _logistics_api_request_upload_file(url=None, upload_id=None, token=None, company=None, path=None, file_name=None):
    payload = {'upload_id': upload_id, 'company': company}
    files = [('files', (file_name, open(path, 'rb'), 'text/csv'))]
    headers = {'x-access-token': token}
    response = requests.request(
        "PUT", url, headers=headers, data=payload, files=files, verify=False)
    return response


def _logistics_api_request_get_upload_detail(url=None, upload_id=None, token=None):
    headers = {'x-access-token': token}
    response = requests.request(
        "GET", url+f"?upload_id={upload_id}", headers=headers, data=None, verify=False)

    jsonData = json.loads(response.content)
    return jsonData


def _logistics_api_request_send_success(url=None, upload_id=None, token=None,incompleted=None,remark=None,bom=False):
    payload = json.dumps({
        "upload_id": upload_id,
        "incompleted": incompleted,
        "remark":remark,
        "bom_flag":bom
    })
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    return response


def _logistics_api_request_send_page_count(url=None, upload_id=None, token=None, page_count=None):
    payload = json.dumps({
        "upload_id": upload_id,
        "page_count": int(page_count)
    })
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    return response

def _logistics_api_request_send_start(url=None, upload_id=None, token=None):
    payload = json.dumps({
        "upload_id": upload_id,
    })
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    return response

def _logistics_api_request_send_fail_message(url=None, upload_id=None, token=None, message=None):
    up_dict = {"upload_id":upload_id}
    payload = json.dumps({
        "addition": json.dumps(up_dict),
        "remark": str(message)
    })
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    return response

def _logistics_api_request_create_transaction(url=None,upload_id=None , token=None, user_id=None, directory_id=None, tenant_id=None, remark=None, page_count=None, success=None, transaction_name=None, invalid_format=None):
    payload = json.dumps({
        "upload_id": str(upload_id),
        "user_id": str(user_id),
        "directory_id": str(directory_id),
        "tenant_id": str(tenant_id),
        "remark": str(remark),
        "page_count": int(page_count),
        "success": bool(success),
        "transaction_name": str(transaction_name),
        "invalid_format": bool(invalid_format)
    })
    headers = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response



def _new_version_ghf_api_request_download_file(apiUrl=None, source_id=None, token=None, path=None):
    headers = {
        'x-api-key': token,
    }
    response = requests.request("GET", f"{apiUrl}/files/source-file/{source_id}", headers=headers, verify=False)
    with open(path, "wb") as binary_file:
        binary_file.write(response.content)
        binary_file.close()
        


def _new_version_ghf_api_request_upload_file(apiUrl=None, ts_id=None, token=None, path=None, file_name=None):
    files = [('files', (file_name, open(path, 'rb'), 'text/csv'))]
    headers = {'x-api-key': token}
    response = requests.request(
        "PUT", f"{apiUrl}/files/robot/{ts_id}/result", headers=headers, files=files, verify=False)
    return response


def _new_version_ghf_api_request_send_success(apiUrl=None, ts_id=None, token=None, page_count=0, invalid_page_count=0,remark=None,bom=False):
    payload = json.dumps({
        "mode": "success",
        "remark":remark,
        "is_bom_flag":bool(bom),
        "data_page_count": int(page_count),
        "nodata_page_count": int(invalid_page_count),
    })
    headers = {
        'x-api-key': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", f"{apiUrl}/transaction/{ts_id}", headers=headers, data=payload, verify=False)
    return response


def _new_version_ghf_api_request_send_start(apiUrl=None, ts_id=None, token=None):
    payload = json.dumps({
        "mode": "start",
    })
    headers = {
        'x-api-key': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", f"{apiUrl}/transaction/{ts_id}", headers=headers, data=payload, verify=False)
    return response

def _new_version_ghf_api_request_fail_message(apiUrl=None, ts_id=None, token=None, page_count=0, invalid_page_count=0,remark=None,bom=False):
    payload = json.dumps({
        "mode": "failed",
        "remark": remark,
        "is_bom_flag":bool(bom),
        "data_page_count": int(page_count),
        "nodata_page_count": int(invalid_page_count),
    })
    headers = {
        'x-api-key': token,
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", f"{apiUrl}/transaction/{ts_id}", headers=headers, data=payload, verify=False)
    return response