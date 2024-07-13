from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

class pixel:
    x = None
    y = None
    def __init__(self,x,y):
        self.x = x
        self.y = y

class vertices:
    vertices = None
    def __init__(self,idexlist):
        self.vertices = [pixel(idexlist[0][0],idexlist[0][1]),pixel(idexlist[1][0],idexlist[1][1]),pixel(idexlist[2][0],idexlist[2][1]),pixel(idexlist[3][0],idexlist[3][1])]

class OCR_format:
    description = None
    bounding_poly = None
    def __init__(self,description,idexlist):
        self.description = description
        self.bounding_poly = vertices(idexlist)

def _azure_ocr_text_with_vertex(api_key=None,endpoint=None,file_path=None):
    result_list = []
    credentials = CognitiveServicesCredentials(api_key)
    client = ComputerVisionClient(endpoint, credentials)
    with open(file_path, "rb") as image_stream:
        result = client.recognize_printed_text_in_stream(image_stream)
        for region in result.regions:
            for line in region.lines:
                for word in line.words:
                    x = int(str(word.bounding_box).split(',')[0])
                    y = int(str(word.bounding_box).split(',')[1])
                    w = int(str(word.bounding_box).split(',')[2])
                    h = int(str(word.bounding_box).split(',')[3])
                    ocr_format = OCR_format(word.text,[[x,y],[x+w,y],[x+w,y+h],[x,y+h]])
                    result_list.append(ocr_format)
    return result_list
