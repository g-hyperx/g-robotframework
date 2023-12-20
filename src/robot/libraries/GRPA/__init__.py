from datetime import datetime
import json
import socket
import requests
from robot.api.deco import keyword, library
from robot.version import VERSION
import threading
from robot.api.logger import console
from requests import put, post
from .constant import HOST
from robot.libraries.GRPA.google_vision import _google_vision_get_ocr_text, _google_vision_get_ocr_text_with_vertex, _match_area, _google_vision_get_OCR_text_with_label
from robot.libraries.GRPA.csv import _write_list_to_csv
from robot.libraries.GRPA.api_request import _logistics_api_request_download_file, _logistics_api_request_upload_file, _logistics_api_request_send_success, _logistics_api_request_send_page_count, _logistics_api_request_get_upload_detail, _logistics_api_request_send_fail_message, _logistics_api_request_create_transaction
from robot.libraries.GRPA.pdf import _convert_pdf_to_img,_get_pdf_full_text,_get_pdf_full_text_by_page
from robot.libraries.GRPA.common import _get_file_sorted_modified_date, _join_list, _json_to_dict, _sorted_vertexs_to_list,_sorted_vertexs_by_line, _get_uuidv4, _random_string
from robot.libraries.GRPA.assets import _get_asset_string_variable, _get_asset_integer_variable, _get_asset_float_variable
from robot.libraries.GRPA.min_aik import _logistics_min_aik_ocr
from robot.libraries.GRPA.kuenhe import _logistics_kuenhe_ocr1,_logistics_kuenhe_ocr2

@library
class GRPA:

    ROBOT_LIBRARY_VERSION = VERSION

    @keyword("Get Asset String Variable")
    def get_asset_string_variable(self, vname=None):
        return _get_asset_string_variable(vname)

    @keyword("Get Asset Integer Variable")
    def get_asset_integer_variable(self, vname=None):
        return _get_asset_integer_variable(vname)

    @keyword("Get Asset Float Variable")
    def get_asset_float_variable(self, vname=None):
        return _get_asset_float_variable(vname)
    
    @keyword("Json To Dict")
    def json_to_dict(self, jsonstr = None):
        return _json_to_dict(jsonstr)
    
    #OCR

    @keyword("Google Vision Get OCR Text")
    def google_vision_get_ocr_text(self, api_key=None, file_path=None):
        return _google_vision_get_ocr_text(api_key, file_path)

    @keyword("Google Vision Get OCR Text With Vertex")
    def google_vision_get_ocr_text_with_vertex(self, api_key=None, file_path=None):
        return _google_vision_get_ocr_text_with_vertex(api_key, file_path)

    @keyword("Match Area")
    def match_area(self, vertexs=None, labels=None, skipx=0, skipy=0):
        return _match_area(vertexs, labels, skipx, skipy)

    @keyword("Write List To CSV")
    def write_list_to_csv(self, file_name=None, data=None, encode=None):
        return _write_list_to_csv(file_name, data)

    @keyword("Google Vision Get OCR Text With Label")
    def google_vision_get_OCR_text_with_label(self, api_key, img_path, labels):
        return _google_vision_get_OCR_text_with_label(api_key, img_path, labels)

    @keyword("Logistics API Request Download File")
    def api_request_download_file(self, url=None, source_id=None, token=None, path=None):
        return _logistics_api_request_download_file(url, source_id, token, path)

    @keyword("Logistics API Request Upload File")
    def api_request_upload_file(self, url=None, upload_id=None, token=None, company=None, path=None, file_name=None):
        return _logistics_api_request_upload_file(url, upload_id, token, company, path, file_name)

    @keyword("Logistics API Request Send Success")
    def api_request_send_success(self, url=None, upload_id=None, token=None,incompleted=None,remark=None):
        return _logistics_api_request_send_success(url, upload_id, token,incompleted,remark)

    @keyword("Logistics API Request Send Page Count")
    def api_request_send_page_count(self, url=None, upload_id=None, token=None, page_count=None):
        return _logistics_api_request_send_page_count(url, upload_id, token, page_count)

    @keyword("Logistics API Request Get Upload Detail")
    def logistics_api_request_upload_detail(self, url=None, upload_id=None, token=None):
        return _logistics_api_request_get_upload_detail(url, upload_id, token)

    @keyword("Logistics API Request Send Fail Message")
    def logistics_api_request_send_fail_message(self, url=None, upload_id=None, token=None, message=None):
        return _logistics_api_request_send_fail_message(url, upload_id, token, message)
    
    @keyword("Logistics API Request Create Transaction")
    def logistics_api_request_create_transaction(self, url=None, upload_id=None, token=None, user_id=None, directory_id=None, tenant_id=None, remark=None, page_count=None, success=None, transaction_name=None, invalid_format=None):
        return _logistics_api_request_create_transaction(url, upload_id, token, user_id, directory_id, tenant_id, remark, page_count, success, transaction_name, invalid_format)

    @keyword("Convert PDF To Img")
    def convert_pdf_to_img(self, pdf_path, pages, output_path, file_name="img", format_file="jpg", scale=300/72, rotation=0):
        return _convert_pdf_to_img(pdf_path, pages, output_path, file_name, format_file, scale, rotation)
    
    @keyword("Get PDF Full Text")
    def get_pdf_full_text(self,pdf_path=None):
        return _get_pdf_full_text(pdf_path)
    
    @keyword("Get PDF Full Text By Page")
    def get_pdf_full_text_by_page(self,pdf_path=None,page=None):
        return _get_pdf_full_text_by_page(pdf_path,page)


    @keyword("Get Files Sorted Modified Date")
    def get_file_sorted_modified_date(self, path=None):
        return _get_file_sorted_modified_date(path)

    @keyword("Join List")
    def join_list(self, collections=None, center=","):
        return _join_list(collections, center)
    
    @keyword("Logistics MIN AIK OCR")
    def logistics_min_aik_ocr(self,api_key=None,pdf_path=None,img_path=None,output_path=None,output_format=None,class_label=None,min1_in_label=None,min1_pa_label=None,min2_in_label=None,min2_pa_label=None,min3_in_label=None,qnit=None,origin_match=None,package_match=None):
        return _logistics_min_aik_ocr(api_key,pdf_path,img_path,output_path,output_format,class_label,min1_in_label,min1_pa_label,min2_in_label,min2_pa_label,min3_in_label,qnit,origin_match,package_match)
    
    @keyword("Convert Date String Format")
    def convert_date_string_format(self,word=None,oformat=None,nformat=None):
        return datetime.strptime(word,oformat).strftime(nformat)
    
    @keyword("Indexof")
    def indexOf(self,word=None,search=None):
        try:
            index = str(word).index(str(search))
            return index
        except Exception as ex:
            return -1
    
    @keyword("Sorted Vertexs From OCR")
    def sorted_vertexs_from_ocr(self,vertexs=None):
        return sorted(vertexs, key=lambda item: ((item.bounding_poly.vertices[0].y*10000)+item.bounding_poly.vertices[0].x))
    
    @keyword("Sorted Vertexs To List")
    def sorted_vertexs_to_list(self,vertexs=None,space_x=None,space_y=None):
        return _sorted_vertexs_to_list(vertexs,space_x,space_y)
    
    @keyword("Sorted Vertexs By Line")
    def sorted_vertexs_by_line(self,vertexs=None,space_y=None):
        return _sorted_vertexs_by_line(vertexs,space_y)
    
    @keyword("Logistics Kuenhe OCR1")
    def logistics_kuenhe_ocr1(self,api_key=None,pdf_path=None,img_path=None,output_path=None):
        return _logistics_kuenhe_ocr1(api_key,pdf_path,img_path,output_path)
    
    @keyword("Logistics Kuenhe OCR2")
    def logistics_kuenhe_ocr2(self,api_key=None,pdf_path=None,img_path=None,output_path=None):
        return _logistics_kuenhe_ocr2(api_key,pdf_path,img_path,output_path)
    
    @keyword("Starts With")
    def starts_with(self,wording=None,value=None):
        return str(wording).startswith(str(value))
    
    @keyword("Ends With")
    def ends_with(self,wording=None,value=None):
        return str(wording).endswith(str(value))
    
    @keyword("Isnumeric")
    def String_isnumeric(self,wording=None):
        return str(wording).isnumeric()
    
    @keyword("Isalpha")
    def String_isalpha(self,wording=None):
        return str(wording).isalpha()
    
    @keyword("Get UUID")
    def get_uuid(self):
        return _get_uuidv4()

    @keyword("Random String")
    def random_string(self,length=None):
        return _random_string(length)
