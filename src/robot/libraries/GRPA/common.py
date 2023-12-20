from os import path
import os
import json
from pathlib import Path
import random
import string
import uuid

def _get_file_sorted_modified_date(path=None):
    files = os.listdir(path)
    files = [os.path.join(path, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def _join_list(collections=None,center=None):
    return str(center).join(map(str,collections))

def _json_to_dict(jsonstr=None):
    if jsonstr is None:
        raise AssertionError('None json string!')

    return json.loads(jsonstr)

def _random_string(length=None):
    if length is None:
        raise AssertionError('None length')

    return ''.join(random.choices(string.ascii_letters, k=length))

def _get_uuidv4():
    return str(uuid.uuid4())

def _sorted_vertexs_to_list(vertexs=None,space_x=None,space_y=None):
    texts = sorted(vertexs, key=lambda item: ((item.bounding_poly.vertices[0].y*10000)+item.bounding_poly.vertices[0].x))
    last_y = texts[1].bounding_poly.vertices[0].y
    sorted_vertex = [[]]
    count = 0
    for i in range(1,len(texts)):
        if abs(texts[i].bounding_poly.vertices[0].y - last_y) > int(space_y):
            sorted_vertex.append([texts[i]])
            count = count + 1
        else:
            sorted_vertex[count].append(texts[i])
        last_y = texts[i].bounding_poly.vertices[0].y
    for i in range(len(sorted_vertex)):
        sorted_vertex[i] = sorted(sorted_vertex[i], key=lambda item: item.bounding_poly.vertices[0].x)
        last_x = sorted_vertex[i][0].bounding_poly.vertices[2].x
        load_text = ''
        for j in sorted_vertex[i]:
            if j.bounding_poly.vertices[0].x - last_x > int(space_x):
                load_text = load_text +"||"+ j.description
            else:
                load_text = load_text + " "+ j.description
            last_x = j.bounding_poly.vertices[2].x
        sorted_vertex[i] = load_text.strip().split("||")
    return sorted_vertex

def _sorted_vertexs_by_line(vertexs=None,space_y=None):
    texts = sorted(vertexs, key=lambda item: ((item.bounding_poly.vertices[0].y*10000)+item.bounding_poly.vertices[0].x))
    texts.pop(0)
    last_y = texts[0].bounding_poly.vertices[0].y
    sorted_vertex = [[]]
    count = 0
    for i in range(0,len(texts)):
        if abs(texts[i].bounding_poly.vertices[0].y - last_y) > int(space_y):
            sorted_vertex.append([texts[i]])
            count = count + 1
        else:
            sorted_vertex[count].append(texts[i])
        last_y = texts[i].bounding_poly.vertices[0].y
    for i in range(len(sorted_vertex)):
        sorted_vertex[i] = sorted(sorted_vertex[i], key=lambda item: item.bounding_poly.vertices[0].x)
    result = []
    for i in sorted_vertex:
        for j in i:
            result.append(j)
    return result

