import csv

def _write_list_to_csv(file_name=None,data=None):
    with open(file_name, 'w', encoding='utf-8-sig',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)