import os
from google.cloud import vision
import json


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

def _match_area(vertexs=None,labels=None,skipx=0,skipy=0):
    labels=json.loads(labels)
    response = {}
    for vertex in vertexs:
        for label in labels:
            if label["start"]["x"]+skipx <= vertex.bounding_poly.vertices[0].x and label["start"]["y"]+skipy <= vertex.bounding_poly.vertices[0].y and label["end"]["x"]+skipx >= vertex.bounding_poly.vertices[2].x and label["end"]["y"]+skipy >= vertex.bounding_poly.vertices[2].y:
                if response.get(label["label"]) == None:
                    response[label["label"]] = [vertex.description]
                else:
                    response[label["label"]].append(vertex.description)
    for label in labels:
        if response.get(label["label"]) == None:
            response[label["label"]] = None
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


