from google.cloud import vision
import os,csv,fitz

def rectangle_match(start,end,start_vertices,end_vertices,skipx,skipy):
    if start["x"]+skipx <= start_vertices.x and start["y"]+skipy <= start_vertices.y and end["x"]+skipx >= end_vertices.x and end["y"]+skipy >= end_vertices.y:
        return True
    else :
        return False
    
def _logistics_kuenhe_ocr1(api_key=None,pdf_path=None,img_path=None,output_path=None):
    api_key = api_key
    scale = 300/72
    labels = [
    {"label":"invoice","start":{"x":1820.8442517013566,"y":443.88650357435426},"end":{"x":1971.0393102189116,"y":487.8721992830669}},
    {"label":"invoice_date","start":{"x":1822.9898953944644,"y":488.94502112962084},"end":{"x":1972.1121320654656,"y":529.7122512986715}},
    {"label":"payer","start":{"x":271.8864721388416,"y":570.6146673984362},"end":{"x":1092.4699839161433,"y":716.3587787474725}}
    ]
    result_dict = {}

    pdf = fitz.open(pdf_path)
    mat = fitz.Matrix(scale, scale)
    count = 0
    for p in pdf:
        count += 1
    for i in range(count):
        page = pdf.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(img_path+'img'+str(i)+'.'+'jpg')
    pdf.close()

    files = os.listdir(img_path)
    files = [os.path.join(img_path, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    count = 0
    for file in files:
        grpa_label_response = {}
        with open(file, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        full_text_page = texts[0].description
        branch_vertex = ''
        invoice_vertext = ''

        # find branch and invoice vertex
        for text in texts:
            if str(text.description) == 'Branch':
                branch_vertex = text.bounding_poly.vertices[0]
            elif str(text.description) == 'INVOICE':
                invoice_vertext = text.bounding_poly.vertices[0]

        # insert data to labels
        grpa_label_response = {}
        for text in texts:
            for label in labels:
                if label["label"] == 'invoice' or label["label"] == 'invoice_date':
                    if rectangle_match(label["start"], label["end"], text.bounding_poly.vertices[0], text.bounding_poly.vertices[2], invoice_vertext.x-1601,invoice_vertext.y-495) :
                        if grpa_label_response.get(label["label"]) == None:
                            grpa_label_response[label["label"]] = [text.description]
                        else:
                            grpa_label_response[label["label"]].append(text.description)
                else:
                    if rectangle_match(label["start"], label["end"], text.bounding_poly.vertices[0], text.bounding_poly.vertices[2], branch_vertex.x-525,branch_vertex.y-352) :
                        if grpa_label_response.get(label["label"]) == None:
                            grpa_label_response[label["label"]] = [text.description]
                        else:
                            grpa_label_response[label["label"]].append(text.description)
        for label in labels:
            if grpa_label_response.get(label["label"]) == None:
                grpa_label_response[label["label"]] = None

        # get datatable
        texts = response.full_text_annotation
        table = []
        for i in response.full_text_annotation.pages[0].blocks:
            if i.bounding_box.vertices[0].y < (1285+(branch_vertex.y-352)):
                continue
            full_text = ''
            for j in i.paragraphs:
                for k in j.words:
                    for l in k.symbols:
                        full_text = full_text+l.text
                    full_text = full_text+" "
                full_text = full_text+" "
            if 'NET' in full_text and 'GROSS' in full_text:
                table.append({'description':'NET WEIGHT','x':i.bounding_box.vertices[0].x,'y':i.bounding_box.vertices[0].y})
                table.append({'description':'GROSS WEIGHT','x':i.bounding_box.vertices[0].x+100,'y':i.bounding_box.vertices[0].y})
            elif '15 01532-001' in full_text:
                table.append({'description':'15','x':i.bounding_box.vertices[0].x,'y':i.bounding_box.vertices[0].y})
                table.append({'description':'01532-001','x':i.bounding_box.vertices[0].x+100,'y':i.bounding_box.vertices[0].y})
            else:
                table.append({'description':full_text,'x':i.bounding_box.vertices[0].x,'y':i.bounding_box.vertices[0].y})
        table = sorted(table, key=lambda item: (item['y']*1000))
        load = []
        load2 = []
        list_count = 0
        for i in table:
            load.append(i)
            list_count = list_count + 1
            if list_count == 8:
                load = sorted(load, key=lambda item: (item['x']))
                for j in load:
                    load2.append(j)
                load = []
                list_count = 0
        load2 = load2[8:]
        check_end = True
        while check_end:
            if len(load2) > 0:
                if str(load2[0]['description']).strip().isdigit():
                    if result_dict.get(grpa_label_response['invoice'][0]) == None:
                        result_dict[grpa_label_response['invoice'][0]] = []
                    result_dict[grpa_label_response['invoice'][0]].append([str(load2[0]['description']).strip(),grpa_label_response['invoice'][0],grpa_label_response['invoice_date'][0],' '.join(map(str,grpa_label_response['payer'])), \
                                                                        str(load2[1]['description']).strip().replace("  ",""),str(load2[2]['description']).strip().replace("  ",""),str(load2[3]['description']).strip().replace("  ",""),str(load2[4]['description']).strip().replace("  ",""), \
                                                                        str(load2[5]['description']).strip().replace("  ",""),str(load2[6]['description']).strip().replace("  ","")]) 
                    load2 = load2[8:]
                else:
                    check_end = False
            else:
                check_end = False

        # find last page
        if 'TOTAL: PACKAGE:' in full_text_page:
            totalPac = ''
            totalW = ''
            mark = ''
            lines = str(full_text_page).split('\n')
            for line in lines:
                if 'PALLET' in line:
                    totalPac = line
                elif 'KGS' in line:
                    totalW = line
                elif 'MARK&NOS' in line:
                    mark = line.replace("MARK&NOS.:","").strip()
            for i in range(len(result_dict[grpa_label_response['invoice'][0]])):
                result_dict[grpa_label_response['invoice'][0]][i].append(mark)
                result_dict[grpa_label_response['invoice'][0]][i].append(totalPac)
                result_dict[grpa_label_response['invoice'][0]][i].append(totalW)

    # write csv
    csv_list = [['NO','Invoice','Invoice date','Payer','Part no','Description','Qty','Price','Amount','Net weight','Mark & NOS','Total package','Total net weight']]
    for i in result_dict:
        for j in result_dict[i]:
            row = []
            for k in j:
                row.append(k)
            csv_list.append(row)
    
    csv_check = False
    if len(csv_list) > 1:
        csv_check = True
        with open(output_path, 'w', encoding='utf-8-sig',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)       
    return [len(files),csv_check]

def _logistics_kuenhe_ocr2(api_key=None,pdf_path=None,img_path=None,output_path=None):
    scale = 300/72
    pdf = fitz.open(pdf_path)
    mat = fitz.Matrix(scale, scale)
    count = 0
    for p in pdf:
        count += 1
    for i in range(count):
        page = pdf.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(img_path+'img'+str(i)+'.'+'jpg')
    pdf.close()
    labels = [
        {"label":"invoice","start":{"x":1966.6804871126076,"y":348.78680851307564},"end":{"x":2353.5981051317376,"y":448.5708257916933}},
        {"label":"inv date","start":{"x":312.58594999915533,"y":355.3237752560409},"end":{"x":518.7285840439237,"y":425.7558418880035}},
        {"label":"payer","start":{"x":44.60052574095643,"y":530.545014194094},"end":{"x":1104.517235787807,"y":905.0374660420899}},
        {"label":"no","start":{"x":13.679130634241176,"y":1400.8297617214234},"end":{"x":42.679130634241176,"y":1499.4153942045052}},
        {"label":"description","start":{"x":472.34649138385083,"y":1420.3940511540109},"end":{"x":1247.0992243354387,"y":1485.6725519348543}},
        {"label":"des no","start":{"x":472.34649138385083,"y":1480.5189860837345},"end":{"x":1016.9066163187806,"y":1537.2082104460462}},
        {"label":"qty","start":{"x":1336.4276990881715,"y":1375.7298137776443},"end":{"x":1472.1382665009774,"y":1499.4153942045054}},
        {"label":"nw","start":{"x":1678.280900545746,"y":1382.6012349124699},"end":{"x":1827.734310228203,"y":1518.3118023252757}},
        {"label":"price","start":{"x":1850.0664289163863,"y":1380.8833796287636},"end":{"x":2066.516194663393,"y":1499.4153942045054}},
        {"label":"amount","start":{"x":2102.5911556212272,"y":1379.165524345057},"end":{"x":2349.9623164749496,"y":1511.4403811904501}},
        {"label":"fob","start":{"x":2074.67698235803,"y":2373.323744340647},"end":{"x":2360.0103156913624,"y":2425.3237443406465}},
        {"label":"package","start":{"x":374.6769823580295,"y":2441.3237443406465},"end":{"x":645.3436490246961,"y":2494.65707767398}},
        {"label":"total nw","start":{"x":392.0103156913628,"y":2598.65707767398},"end":{"x":670.6769823580294,"y":2646.65707767398}},
        {"label":"origin","start":{"x":408.01031569136285,"y":2647.9904110073135},"end":{"x":649.3436490246961,"y":2701.323744340647}},
        {"label":"mark","start":{"x":1280.0103156913626,"y":2433.3237443406465},"end":{"x":2000.0103156913626,"y":2515.9904110073135}}
    ]
    files = os.listdir(img_path)
    files = [os.path.join(img_path, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    csv_list = [['NO','Invoice','Invoice date','Payer','Description','Description no','Qty','Qty unit','Price','Amount','Net weight','Mark','NOS','Total package','Package unit','Total net weight']]
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    for file in files:
        print(file)
        grpa_label_response = {}
        with open(file, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        full_text_page = texts[0].description
        for text in texts:
            for label in labels:
                if rectangle_match(label["start"], label["end"], text.bounding_poly.vertices[0], text.bounding_poly.vertices[2], 0, 0) :
                    if grpa_label_response.get(label["label"]) == None:
                        grpa_label_response[label["label"]] = [text.description]
                    else:
                        grpa_label_response[label["label"]].append(text.description)
        for label in labels:
            if grpa_label_response.get(label["label"]) == None:
                grpa_label_response[label["label"]] = None
    
        inv = ''
        for i in grpa_label_response['invoice']:
            inv = inv+i
        inv_date = ''
        for i in grpa_label_response['inv date']:
            inv_date = inv_date+i
        payer = ''
        for i in grpa_label_response['payer']:
            payer = payer+str(i)+' '
        no = ''
        for i in grpa_label_response['no']:
            no = no+i
        desc = ''
        for i in grpa_label_response['description']:
            desc = desc+str(i)+' '
        desc_no = ''
        for i in grpa_label_response['des no']:
            desc_no = desc_no+str(i)
        qty = ''
        for i in grpa_label_response['qty']:
            qty = qty+str(i)+' '
        nw = ''
        for i in grpa_label_response['nw']:
            nw = nw+str(i)+' '
        price = ''
        for i in grpa_label_response['price']:
            price = price+str(i)+' '
        amount = ''
        for i in grpa_label_response['amount']:
            amount = amount+str(i)+' '
        fob = ''
        for i in grpa_label_response['fob']:
            fob = fob+str(i)
        package = ''
        for i in grpa_label_response['package']:
            package = package+str(i)+' '
        total_nw = ''
        for i in grpa_label_response['total nw']:
            total_nw = total_nw+str(i)+' '
        origin = ''
        for i in grpa_label_response['origin']:
            origin = origin+str(i)
        mark = ''
        for i in grpa_label_response['mark']:
            mark = mark+str(i)+' '
    
        csv_list.append([no,inv,inv_date,payer,desc,desc_no,qty.strip().split(' ')[1],qty.strip().split(' ')[0],price.replace('USD','').strip(),amount.replace('USD','').strip(),nw.replace('KG','').strip(),mark.strip().split('/')[0],mark.strip().split('/')[1],package.strip().split(' ')[0],package.strip().split(' ')[1],total_nw.replace('KG','').strip()])

    csv_check = False
    if len(csv_list) > 1:
        csv_check = True
        with open(output_path, 'w', encoding='utf-8-sig',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
    return [len(files),csv_check]