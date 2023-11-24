from google.cloud import vision
from datetime import datetime
import csv,os,json,fitz,re

def rectangle_match(start,end,start_vertices,end_vertices):
    if start["x"] <= start_vertices.x and start["y"] <= start_vertices.y and end["x"] >= end_vertices.x and end["y"] >= end_vertices.y:
        return True
    else :
        return False
    
def match_area(texts=None,labels=None):
    grpa_label_response = {}
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

def _logistics_min_aik_ocr(api_key=None,pdf_path=None,img_path=None,output_path=None,output_format=None,class_label=None,min1_in_label=None,min1_pa_label=None,min2_in_label=None,min2_pa_label=None,min3_in_label=None,qnit=None,origin_match=None,package_match=None):
    ori_match = json.loads(origin_match)
    unit_match = json.loads(qnit)
    pack_match = json.loads(package_match)
    classifly_label = json.loads(class_label)
    min1_invoice_label = json.loads(min1_in_label)
    min1_packing_label = json.loads(min1_pa_label)
    min2_invoice_label = json.loads(min2_in_label)
    min2_packing_label = json.loads(min2_pa_label)
    min3_invoice_label = json.loads(min3_in_label)
    result = {}
    error_message = ''
    error_list = []
    write_csv = True
    if output_format == 'NETBay_WD':
        csv_list = [['//','//','Invoice no.','Invoice Date','Product code','','EN Des.','EN Des.2','Qty Inv.  / Qty. ใบขน','Qty unit','Unit price','Amount','packageAmount','packageUnit','Purchase order No','Origin','','Marks','netWeight','itemGrossWeight']]
    else:
        csv_list = [['Invoice No.','Date','Origin','Purchase Order No','Shipping Terms','Shipped By','Part No.','Description','Net Weight','Gross Weight','Quantity','Quantity Unit','Unit Price','Total','Shipping Mark']]
    page_count = 0
    usage_count = 0

    # Convert pdf to image step
    pdf = fitz.open(pdf_path)
    mat = fitz.Matrix(300/72, 300/72)
    count = 0
    for p in pdf:
        count += 1
    for i in range(count):
        page = pdf.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(img_path+"img"+str(i)+'.jpg')
    pdf.close()

    # List img file in folder
    files = os.listdir(img_path)
    files = [os.path.join(img_path, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))

    # Classify and get label data
    for file_path in files:
        try:
            page_count = page_count + 1
            client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            grpa_respones = match_area(texts,classifly_label)
            if grpa_respones['MIN AIK1'] != None :
                if grpa_respones['MIN AIK1'][0] == 'MIN':
                    if grpa_respones['header1'][0] == 'INVOICE':
                        grpa_respones = match_area(texts,min1_invoice_label)
                        invoice = ''
                        for i in grpa_respones['invoice']:
                            invoice = invoice+str(i)
                        if result.get(invoice) == None:
                            result[invoice] = {}
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 1
                        else:
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 1
                    elif grpa_respones['header1'][0] == 'PACKING':
                        grpa_respones = match_area(texts,min1_packing_label)
                        invoice = ''
                        for i in grpa_respones['invoice']:
                            invoice = invoice+str(i)
                        if result.get(invoice) == None:
                            result[invoice] = {}
                            result[invoice]['packing'] = grpa_respones
                        else:
                            result[invoice]['packing'] = grpa_respones
                else:
                    error_list.append(page_count)
            elif grpa_respones['MIN AIK2'] != None :
                if grpa_respones['MIN AIK2'][0] == 'MIN':
                    if grpa_respones['header2'][0] == 'INVOICE':
                        grpa_respones = match_area(texts,min2_invoice_label)
                        invoice = ''
                        for i in grpa_respones['invoice']:
                            invoice = invoice+str(i)
                        if result.get(invoice) == None:
                            result[invoice] = {}
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 2
                        else:
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 2
                    elif grpa_respones['header2'][0] == 'PACKING':
                        grpa_respones = match_area(texts,min2_packing_label)
                        invoice = ''
                        for i in grpa_respones['invoice']:
                            invoice = invoice+str(i)
                        if result.get(invoice) == None:
                            result[invoice] = {}
                            result[invoice]['packing'] = grpa_respones
                        else:
                            result[invoice]['packing'] = grpa_respones
                else:
                    error_list.append(page_count)
            elif grpa_respones['MIN AIK3'] != None :
                if grpa_respones['MIN AIK3'][0] == 'MIN':
                    if grpa_respones['header3'][0] == 'INVOICE':
                        grpa_respones = match_area(texts,min3_invoice_label)
                        invoice = ''
                        for i in grpa_respones['invoice']:
                            invoice = invoice+str(i)
                        if result.get(invoice) == None:
                            result[invoice] = {}
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 3
                        else:
                            result[invoice]['invoice'] = grpa_respones
                            result[invoice]['template'] = 3
                    elif grpa_respones['header3'][0] == 'PACKING':
                        pass
                else:
                    error_list.append(page_count)
            else:
                error_list.append(page_count)
            usage_count = usage_count+1
        except Exception as ex:
            pass

    # Write error message
    if len(error_list) == len(files):
        write_csv = False
        error_message = str(pdf_path).split('/')[-1]+' invalid format'+"\n"
    elif len(error_list) > 0:
        error_message = str(pdf_path).split('/')[-1]+' invalid format at page '+','.join(map(str,error_list))+"\n"
    
    # Get output data
    for invoice in result:
        indate = ''
        origin = ''
        pono = ''
        shipterm = ''
        shipby = ''
        partno = ''
        desc = ''
        desc2 = ''
        nw = ''
        gw = ''
        shipmark = ''
        quantity = ''
        qunit = ''
        unit = ''
        total = ''
        pa = ''
        pu = ''
        marks = ''
        error_missing_column_list = []
        if result[invoice]['template'] < 3:
            if result[invoice]['invoice']['date'] != None:
                for i in result[invoice]['invoice']['date']:
                    indate = indate + i
            else:
                error_missing_column_list.append('Invoice date')
            if result[invoice]['invoice']['unit price'] != None:
                for i in result[invoice]['invoice']['unit price']:
                    unit = unit + i
            else:
                error_missing_column_list.append('Unit price')
            if result[invoice]['invoice']['total'] != None:
                for i in result[invoice]['invoice']['total']:
                    if str(i).replace(',','').replace('.','').isnumeric():
                        total = total + i
                        break
            else:
                error_missing_column_list.append('Amount')
            if result[invoice]['invoice']['quantity'] != None:
                for i in result[invoice]['invoice']['quantity']:
                    quantity = quantity + i
            else:
                error_missing_column_list.append('Quantity')
                error_missing_column_list.append('Quantity unit')
            if result[invoice]['invoice']['po no'] != None:
                for i in result[invoice]['invoice']['po no']:
                    pono = pono + i
            else:
                error_missing_column_list.append('Purchase order no.')
            if result[invoice]['invoice']['description'] != None:
                for i in result[invoice]['invoice']['description']:
                    desc = desc + i + ' '
                if 'P / N #' in desc:
                    partno = desc.split("P / N #")[1]
                    desc = desc.split("P / N #")[0]
                elif 'P/N#' in desc:
                    partno = desc.split("P/N#")[1]
                    desc = desc.split("P/N#")[0]
            else:
                error_missing_column_list.append('Description')
                error_missing_column_list.append('Part no.')
            fulltext = str(result[invoice]['invoice']['full text']).split("\n")
            check_line = False
            for line in fulltext:
                if check_line:
                    shipmark = line.strip()
                    check_line = False
                if 'Country Of Origin' in line:
                    origin = line.replace('Country Of Origin','')
                    origin = origin.replace(':','').strip()
                if 'MADE IN' in line:
                    origin = line.replace('MADE IN','').strip()
                if 'SHIPPING MARKS' in line:
                    shipmark = line.replace('SHIPPING MARKS','')
                    shipmark = shipmark.replace(':','').strip()
                if 'SHIPPING MARK:' == line.strip():
                    check_line = True
            if origin == '':
                error_missing_column_list.append('Origin')
            if result[invoice].get('packing') == None:
                error_missing_column_list.append('Package Amount')
                error_missing_column_list.append('Package Unit')
                error_missing_column_list.append('Net weight')
                error_missing_column_list.append('Gross weight')
            else:
                if result[invoice]['packing']['nw'] != None:
                    nw = result[invoice]['packing']['nw'][0]
                else:
                    error_missing_column_list.append('Net weight')
                if result[invoice]['packing']['gw'] != None:
                    gw = result[invoice]['packing']['gw'][0]
                else:
                    error_missing_column_list.append('Gross weight')
                fulltext = str(result[invoice]['packing']['full text']).split("\n")
                regexp = re.compile(r'\((\d+)\)')
                for line in fulltext:
                    if regexp.search(str(line).replace(' ','')):
                        full_string = str(line).strip()
                        startChar = full_string.index('(')
                        endChar = full_string.index(')')
                        lastSpace = full_string.rindex(' ')
                        pa = full_string[startChar+1:endChar]
                        pu = full_string[endChar+2:lastSpace]
                        try:
                            pu = pack_match[pu.upper()]
                        except Exception as ex:
                            error_missing_column_list.append('Package unit')
                if pa == '':
                    error_missing_column_list.append('Package Amount')
                if pu == '':
                    error_missing_column_list.append('Package Unit')
            if quantity != '':
                lchar = -1
                fchar = -1
                count = 0
                trigger = False
                for i in str(quantity):
                    if i.isalpha():
                        if not trigger:
                            fchar = count
                        lchar = count
                        trigger = True
                    elif trigger and not i.isalpha():
                        break
                    count = count+1
                quantity = quantity[0:lchar+1]
                qunit = quantity[fchar:lchar+1]
                quantity = quantity[0:fchar]
            if partno != '':
                partno = partno.replace(' ','').replace('O','0').replace('o','0')
                if partno.startswith('0F') or partno.startswith('0B') :
                    partno = partno[0:7]
            if indate != '':
                if len(indate.split('-')[-1]) > 2:
                    indate = datetime.strptime(str(indate).replace(':',''),'%d-%b-%Y').strftime('%d/%m/%Y')
                else:
                    indate = datetime.strptime(str(indate).replace(':',''),'%d-%b-%y').strftime('%d/%m/%Y')
            if output_format == 'NETBay_WD':
                um = ''
                om = ''
                try:
                    um = unit_match[str(qunit).upper()]
                except Exception as ex:
                    error_missing_column_list.append('Quantity unit')  
                try:
                    om = ori_match[str(origin).upper()]
                except Exception as ex:
                    error_missing_column_list.append('Quantity unit') 
                csv_list.append(['','',str(invoice).replace('O','0'),indate,partno,'',desc,'',quantity,um,unit.replace('PRICE',''),total,pa,pu,pono,om,'','',nw,gw])                   
            else:
                csv_list.append([invoice,indate,origin,pono,shipterm,shipby,partno,desc,nw,gw,quantity,qunit,unit,total,shipmark])
        else:
            if result[invoice]['invoice']['date'] != None:
                for i in result[invoice]['invoice']['date']:
                    indate = indate + i
                indate = datetime.strptime(str(indate).replace(':',''),'%d.%b,%Y').strftime('%d/%m/%Y')
            else:
                error_missing_column_list.append('Invoice date')
            if result[invoice]['invoice']['marks'] != None:
                for i in result[invoice]['invoice']['marks']:
                    marks = marks + i + ' '
            else:
                error_missing_column_list.append('Marks')
            if result[invoice]['invoice']['description'] != None:
                for i in result[invoice]['invoice']['description']:
                    desc = desc + i + ' '
                partno = desc
            else:
                error_missing_column_list.append('Part no.')
                error_missing_column_list.append('Description')
            if result[invoice]['invoice']['description2'] != None:
                for i in result[invoice]['invoice']['description2']:
                    desc2 = desc2 + i
            else:
                error_missing_column_list.append('Description2')
            if result[invoice]['invoice']['quantity'] != None:
                for i in result[invoice]['invoice']['quantity']:
                    quantity = quantity + i
            else:
                error_missing_column_list.append('Quantity')
                error_missing_column_list.append('Quantity unit')
            if result[invoice]['invoice']['unit price'] != None:
                for i in result[invoice]['invoice']['unit price']:
                    unit = unit + i
                unit = unit.replace('USD','')
            else:
                error_missing_column_list.append('Unit price')
            if result[invoice]['invoice']['total'] != None:
                for i in result[invoice]['invoice']['total']:
                    total = total + i
                total = total.replace('USD','')
            else:
                error_missing_column_list.append('Amount')
            if quantity != '':
                lchar = -1
                fchar = -1
                count = 0
                trigger = False
                for i in str(quantity):
                    if i.isalpha():
                        if not trigger:
                            fchar = count
                        lchar = count
                        trigger = True
                    elif trigger and not i.isalpha():
                        break
                    count = count+1
                quantity = quantity[0:lchar+1]
                qunit = quantity[fchar:lchar+1]
                quantity = quantity[0:fchar]
            if output_format == 'NETBay_WD':
                um = ''
                try:
                    um = unit_match[str(qunit).upper()]
                except Exception as ex:
                    error_missing_column_list.append('Quantity unit') 
                csv_list.append(['','',str(invoice).replace('O','0'),indate,partno,'',desc,desc2,quantity,um,unit,total,'','','','','',marks,'',''])                   
            else:
                csv_list.append([invoice,indate,origin,pono,shipterm,shipby,partno,desc,nw,gw,quantity,qunit,unit,total,shipmark])
        if len(error_missing_column_list) > 0:
            error_message = error_message+str(pdf_path).split('/')[-1]+': '+str(invoice)+' missing '+','.join(map(str,error_missing_column_list))+"\n"
   
    # Write CSV file8
    if write_csv:
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)

    if error_message == '' or error_message == None:
        return [page_count,None,"true",usage_count]
    else:
        if write_csv:
            return [page_count,error_message,"true",usage_count]
        else:
            return [page_count,error_message,"false",usage_count]
