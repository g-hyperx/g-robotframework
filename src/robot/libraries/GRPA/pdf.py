import fitz

def _convert_pdf_to_img(pdf_path=None, pages=None, output_path=None, file_name=None, format_file=None, scale=None, rotation=None):
    try:
        pdf = fitz.open(pdf_path)
        mat = fitz.Matrix(scale, scale)
        if pages == '0':
            count = 0
            for p in pdf:
                count += 1
            for i in range(count):
                page = pdf.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                pix.save(output_path+file_name+str(i)+'.'+format_file)
        elif '-' in pages:
            for i in range(int(pages.split('-')[0])-1, int(pages.split('-')[1])):
                page = pdf.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                pix.save(output_path+file_name+str(i)+'.'+format_file)
        elif pages.isdigit():
            page = pdf.load_page(int(pages)-1)
            pix = page.get_pixmap(matrix=mat)
            pix.save(output_path+file_name+'.'+format_file)
        pdf.close()
        return "Success"
    except Exception as ex:
        return ex
