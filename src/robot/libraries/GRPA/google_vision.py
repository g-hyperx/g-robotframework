import os
from google.cloud import vision
import json
import math


def rectangle_match(start,end,start_vertices,end_vertices):
    if start["x"] <= start_vertices.x and start["y"] <= start_vertices.y and end["x"] >= end_vertices.x and end["y"] >= end_vertices.y:
        return True
    else :
        return False

def _google_vision_get_ocr_text(api_key=None,file_path=None):
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    with open(file_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description.split("\n")

def _google_vision_get_ocr_text_with_vertex(api_key=None,file_path=None):
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    with open(file_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def _match_area(vertexs=None,labels=None,skipx=0,skipy=0,full_response=False):
    labels=json.loads(labels)
    response = {}
    for vertex in vertexs:
        for label in labels:
            if label["start"]["x"]+skipx <= vertex.bounding_poly.vertices[0].x and label["start"]["y"]+skipy <= vertex.bounding_poly.vertices[0].y and label["end"]["x"]+skipx >= vertex.bounding_poly.vertices[2].x and label["end"]["y"]+skipy >= vertex.bounding_poly.vertices[2].y:
                if response.get(label["label"]) == None:
                    if full_response:
                        response[label["label"]] = [vertex]
                    else:
                        response[label["label"]] = [vertex.description]
                else:
                    if full_response:
                        response[label["label"]].append(vertex)
                    else:
                        response[label["label"]].append(vertex.description)
    for label in labels:
        if response.get(label["label"]) == None:
            response[label["label"]] = None
    if full_response:
        response['full text'] = vertexs[0]
    else:
        response['full text'] = vertexs[0].description
    return response

def _google_vision_get_OCR_text_with_label(api_key=None,img_path=None,labels=None):
    grpa_label_response = {}
    labels=json.loads(labels)
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    with open(img_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        for label in labels:
            if rectangle_match(label["start"], label["end"], text.bounding_poly.vertices[0], text.bounding_poly.vertices[2]) :
                if grpa_label_response.get(label["label"]) == None:
                    grpa_label_response[label["label"]] = [text.description]
                else:
                    grpa_label_response[label["label"]].append(text.description)
    grpa_label_response["full text"] = texts[0].description

    for label in labels:
        if grpa_label_response.get(label["label"]) == None:
            grpa_label_response[label["label"]] = None
    return grpa_label_response

def _ocr_text_concat_with_space_size(vertexs=None,space_x=None,newline=None):
    result = ''
    last_x = -1
    for vertex in vertexs:
        if last_x < 0:
            result = vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
        elif vertex.bounding_poly.vertices[0].x - last_x < space_x:
            if vertex.bounding_poly.vertices[0].x < last_x:
                if newline == None:
                    result = result + ' ' + vertex.description 
                else:
                    result = result + str(newline) + vertex.description 
            else:
                result = result + vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
        else:
            result = result + ' ' + vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
    result = result.strip()
    return result

def _ocr_text_concat_average_size(vertexs=None):
    result = ''
    last_x = -1
    space_list = []
    for vertex in vertexs:
        if last_x < 0:
            last_x = vertex.bounding_poly.vertices[1].x
        else:
            space_list.append(vertex.bounding_poly.vertices[0].x - last_x)
            last_x = vertex.bounding_poly.vertices[1].x
    last_x = -1
    space_x = math.ceil(sum(space_list)/len(space_list))        
    for vertex in vertexs:
        if last_x < 0:
            result = vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
        elif vertex.bounding_poly.vertices[0].x - last_x < space_x:
            if vertex.bounding_poly.vertices[0].x < last_x:
                result = result + ' ' + vertex.description 
            else:
                result = result + vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
        else:
            result = result + ' ' + vertex.description
            last_x = vertex.bounding_poly.vertices[1].x
    result = result.strip()
    return result
