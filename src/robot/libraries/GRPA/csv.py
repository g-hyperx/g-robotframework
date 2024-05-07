import csv

def _write_list_to_csv(file_name=None,data=None,encode=None):
    if str(encode).lower == 'csv':
        with open(file_name, 'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else:
        with open(file_name, 'w', encoding=encode,newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)