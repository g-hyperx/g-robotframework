from requests import put, post
from .constant import HOST
import json

def _add_queue_to_multiplex_queue(job_multiplex_queue_id=None, name=None, data = None):
    if job_multiplex_queue_id is None:
        raise AssertionError('None job_multiplex_queue_id!')
    if name is None:
        raise AssertionError('None name!')
    if data is None:
        raise AssertionError('None data!')
    

    if isinstance(data, dict):
        data = json.dumps(data)
    
    vdata = {
        "job_multiplex_queue_id": job_multiplex_queue_id,
        "name": name,
        "data": data
    }
    resp = post(f"{HOST}/add-queue-to-multiplex-queue", json=vdata)
    if resp.status_code == 200:
        return resp.content.decode()
    else:
        raise AssertionError(resp.content.decode())

def _get_queue_inside_multiplex_queue(job_multiplex_queue_id=None):
    if job_multiplex_queue_id is None:
        raise AssertionError('None job_multiplex_queue_id!')

    data = {
        "job_multiplex_queue_id": job_multiplex_queue_id
    }
    resp = post(f"{HOST}/get-queue-inside-multiplex-queue", json=data)

    if resp.status_code == 200:
        return resp.content.decode()
    else:
        raise AssertionError(resp.content.decode())
    