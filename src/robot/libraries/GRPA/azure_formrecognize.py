from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import datetime
import os
import sys
from PyPDF2 import PdfWriter, PdfReader

#def _hello_func(var1,var2):
#    result_num = int(var1) + int(var2)
#    result = f"Hello world : {result_num}"
#    return result

def _azure_formrecognize_invoice(a_endpoint,a_key,doc_path,doc_fields):
    invoice_field = {
        "VendorName": "No Data",
        "VendorAddress": "No Data",
        "VendorAddressRecipient": "No Data",
        "CustomerName": "No Data",
        "CustomerId": "No Data",
        "CustomerAddress": "No Data",
        "CustomerAddressRecipient": "No Data",
        "InvoiceId": "No Data",
        "InvoiceDate": "No Data",
        "InvoiceTotal": "No Data",
        "DueDate": "No Data",
        "PurchaseOrder": "No Data",
        "BillingAddress": "No Data",
        "BillingAddressRecipient": "No Data",
        "ShippingAddress": "No Data",
        "ShippingAddressRecipient": "No Data",
        "SubTotal": "No Data",
        "TotalTax": "No Data",
        "PreviousUnpaidBalance": "No Data",
        "AmountDue": "No Data",
        "ServiceStartDate": "No Data",
        "ServiceEndDate": "No Data",
        "ServiceAddress": "No Data",
        "ServiceAddressRecipient": "No Data",
        "RemittanceAddress": "No Data",
        "RemittanceAddressRecipient": "No Data",
        "Description": "No Data",
        "Quantity": "No Data",
        "Unit": "No Data",
        "UnitPrice": "No Data",
        "ProductCode": "No Data",
        "Date": "No Data",
        "Tax": "No Data",
        "Amount": "No Data",
        }
        
    reccord_items = []
    document_analysis_client = DocumentAnalysisClient(
    endpoint=a_endpoint, credential=AzureKeyCredential(a_key)
    )
    with open(doc_path, "rb") as f:
       poller = document_analysis_client.begin_analyze_document(
           "prebuilt-invoice", document=f, locale="th-TH"
       )
    #poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", document=outputStream, locale="en-US")
    invoices = poller.result()
    for idx, invoice in enumerate(invoices.documents):
        record_item = ""
        #print("-------- Page {} ----------".format(i + 1))
        #print("--------Recognizing invoice #{}--------".format(idx + 1))
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            # print(
            #     "Vendor Name: {} has confidence: {}".format(
            #         vendor_name.value, vendor_name.confidence
            #     )
            # )
            invoice_field["VendorName"] = vendor_name.value + "|"
            #print(record_item)
        else:
            invoice_field["VendorName"] = invoice_field["VendorName"] + "|"
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            # print(
            #     "Vendor Address: {} has confidence: {}".format(
            #         vendor_address.value, vendor_address.confidence
            #     )
            # )
            vendor_address_string = ' '.join(str(vendor_address.value.to_dict()[x]) for x in vendor_address.value.to_dict()).replace(" None","").replace("None ","")
            #print(vendor_address_string)
            #for z in vendor_address.value.to_dict():
            #    print(str(z) + " : " + str(vendor_address.value.to_dict()[z]) + "\n")

            invoice_field["VendorAddress"] = vendor_address_string + "|"
            #print(record_item)
        else:
            invoice_field["VendorAddress"] = invoice_field["VendorAddress"] + "|"
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            # print(
            #     "Vendor Address Recipient: {} has confidence: {}".format(
            #         vendor_address_recipient.value, vendor_address_recipient.confidence
            #     )
            # )
            invoice_field["VendorAddressRecipient"] = vendor_address_recipient.value + "|"
            #record_item = record_item + "vendor_address_recipient.value" + "|"
            #print(record_item)
        else:
            invoice_field["VendorAddressRecipient"] = invoice_field["VendorAddressRecipient"] + "|"
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            # print(
            #     "Customer Name: {} has confidence: {}".format(
            #         customer_name.value, customer_name.confidence
            #     )
            # )
            invoice_field["CustomerName"] = customer_name.value + "|"
            #print(record_item)
        else:
            invoice_field["CustomerName"] = invoice_field["CustomerName"] + "|"
        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            # print(
            #     "Customer Id: {} has confidence: {}".format(
            #         customer_id.value, customer_id.confidence
            #     )
            # )
            invoice_field["CustomerId"] = customer_id.value + "|"
            #print(record_item)
        else:
            invoice_field["CustomerId"] = invoice_field["CustomerId"] + "|"
        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            # print(
            #     "Customer Address: {} has confidence: {}".format(
            #         customer_address.value, customer_address.confidence
            #     )
            # )
            customer_address_string = ' '.join(str(customer_address.value.to_dict()[x]) for x in customer_address.value.to_dict()).replace(" None","").replace("None ","")
            invoice_field["CustomerAddress"] = customer_address_string + "|"
            #record_item = record_item + "{}".format(customer_address.value) + "|"
            #record_item = record_item + "customer_address.value" + "|"
            #print(record_item)
        else:
            invoice_field["CustomerAddress"] = invoice_field["CustomerAddress"] + "|"
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            # print(
            #     "Customer Address Recipient: {} has confidence: {}".format(
            #         customer_address_recipient.value,
            #         customer_address_recipient.confidence,
            #     )
            # )
            invoice_field["CustomerAddressRecipient"] = customer_address_recipient.value + "|"
            #record_item = record_item + "customer_address_recipient.value" + "|"
            #print(record_item)
        else:
            invoice_field["CustomerAddressRecipient"] = invoice_field["CustomerAddressRecipient"] + "|"
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            # print(
            #     "Invoice Id: {} has confidence: {}".format(
            #         invoice_id.value, invoice_id.confidence
            #     )
            # )
            invoice_field["InvoiceId"] = invoice_id.value + "|"
            #print(record_item)
        else:
            invoice_field["InvoiceId"] = invoice_field["InvoiceId"] + "|"
        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            # print(
            #     "Invoice Date: {} has confidence: {}".format(
            #         invoice_date.value, invoice_date.confidence
            #     )
            # )
            invoice_field["InvoiceDate"] = invoice_date.value.strftime('%d/%m/%Y') + "|"
            #print(record_item)
        else:
            invoice_field["InvoiceDate"] = invoice_field["InvoiceDate"] + "" + "|"
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            # print(
            #     "Invoice Total: {} has confidence: {}".format(
            #         invoice_total.value, invoice_total.confidence
            #     )
            # )
            invoice_field["InvoiceTotal"] = "{}".format(invoice_total.value) + "|"
            #print(record_item)
        else:
            invoice_field["InvoiceTotal"] = invoice_field["InvoiceTotal"] + "|"
        due_date = invoice.fields.get("DueDate")
        if due_date:
            # print(
            #     "Due Date: {} has confidence: {}".format(
            #         due_date.value, due_date.confidence
            #     )
            # )
            invoice_field["DueDate"] = "{}".format(due_date.value) + "|"
            #print(record_item)
        else:
            invoice_field["DueDate"] = invoice_field["DueDate"] + "|"
        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            # print(
            #     "Purchase Order: {} has confidence: {}".format(
            #         purchase_order.value, purchase_order.confidence
            #     )
            # )
            invoice_field["PurchaseOrder"] = purchase_order.value + "|"
            #print(record_item)
        else:
            invoice_field["PurchaseOrder"] = invoice_field["PurchaseOrder"] + "|"
        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            # print(
            #     "Billing Address: {} has confidence: {}".format(
            #         billing_address.value, billing_address.confidence
            #     )
            # )
            billing_address_string = ' '.join(str(billing_address.value.to_dict()[x]) for x in billing_address.value.to_dict()).replace(" None","").replace("None ","")
            invoice_field["BillingAddress"] = billing_address_string + "|"
            #record_item = record_item + billing_address.value + "|"
            #record_item = record_item + "billing_address.value" + "|"
            #print(record_item)
        else:
            invoice_field["BillingAddress"] = invoice_field["BillingAddress"] + "|"
        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            # print(
            #     "Billing Address Recipient: {} has confidence: {}".format(
            #         billing_address_recipient.value,
            #         billing_address_recipient.confidence,
            #     )
            # )
            invoice_field["BillingAddressRecipient"] = billing_address_recipient.value + "|"
            #record_item = record_item + "billing_address_recipient.value" + "|"
            #print(record_item)
        else:
            invoice_field["BillingAddressRecipient"] = invoice_field["BillingAddressRecipient"] + "|"
        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            # print(
            #     "Shipping Address: {} has confidence: {}".format(
            #         shipping_address.value, shipping_address.confidence
            #     )
            # )
            shipping_address_string = ' '.join(str(shipping_address.value.to_dict()[x]) for x in shipping_address.value.to_dict()).replace(" None","").replace("None ","")
            invoice_field["ShippingAddress"] = shipping_address_string + "|"
            #record_item = record_item + "{}".format(shipping_address.value) + "|"
            #record_item = record_item + "shipping_address.value" + "|"
            #print(record_item)
        else:
            invoice_field["ShippingAddress"] = invoice_field["ShippingAddress"] + "" + "|"
        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            # print(
            #     "Shipping Address Recipient: {} has confidence: {}".format(
            #         shipping_address_recipient.value,
            #         shipping_address_recipient.confidence,
            #     )
            # )
            invoice_field["ShippingAddressRecipient"] = shipping_address_recipient.value + "|"
            #record_item = record_item + "shipping_address_recipient.value" + "|"
            #print(record_item)
        else:
            invoice_field["ShippingAddressRecipient"] = invoice_field["ShippingAddressRecipient"] + "|"
        #print(record_item)    
        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            # print(
            #     "Subtotal: {} has confidence: {}".format(
            #         subtotal.value, subtotal.confidence
            #     )
            # )
            invoice_field["SubTotal"] = "{}".format(subtotal.value) + "|"
        else:
            invoice_field["SubTotal"] = invoice_field["SubTotal"] + "" + "|"
        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            # print(
            #     "Total Tax: {} has confidence: {}".format(
            #         total_tax.value, total_tax.confidence
            #     )
            # )
            invoice_field["TotalTax"] = "{}".format(total_tax.value) + "|"
        else:
            invoice_field["TotalTax"] = invoice_field["TotalTax"] + "|"
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            # print(
            #     "Previous Unpaid Balance: {} has confidence: {}".format(
            #         previous_unpaid_balance.value, previous_unpaid_balance.confidence
            #     )
            # )
            invoice_field["PreviousUnpaidBalance"] = "{}".format(previous_unpaid_balance.value) + "|"
        else:
            invoice_field["PreviousUnpaidBalance"] = invoice_field["PreviousUnpaidBalance"] + "|"
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            # print(
            #     "Amount Due: {} has confidence: {}".format(
            #         amount_due.value, amount_due.confidence
            #     )
            # )
            invoice_field["AmountDue"] = "{}".format(amount_due.value) + "|"
        else:
            invoice_field["AmountDue"] = invoice_field["AmountDue"] + "" + "|"
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            # print(
            #     "Service Start Date: {} has confidence: {}".format(
            #         service_start_date.value, service_start_date.confidence
            #     )
            # )
            invoice_field["ServiceStartDate"] = "{}".format(service_start_date.value) + "|"
        else:
            invoice_field["ServiceStartDate"] = invoice_field["ServiceStartDate"] + "|"
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            # print(
            #     "Service End Date: {} has confidence: {}".format(
            #         service_end_date.value, service_end_date.confidence
            #     )
            # )
            invoice_field["ServiceEndDate"] = "{}".format(service_end_date.value) + "|"
        else:
            invoice_field["ServiceEndDate"] = invoice_field["ServiceEndDate"] + "|"
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            # print(
            #     "Service Address: {} has confidence: {}".format(
            #         service_address.value, service_address.confidence
            #     )
            # )
            service_address_string = ' '.join(str(service_address.value.to_dict()[x]) for x in service_address.value.to_dict()).replace(" None","").replace("None ","")
            invoice_field["ServiceAddress"] = service_address_string + "|"
            #record_item = record_item + service_address.value + "|"
            #record_item = record_item + "service_address.value" + "|"
        else:
            invoice_field["ServiceAddress"] = invoice_field["ServiceAddress"] + "|"
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            # print(
            #     "Service Address Recipient: {} has confidence: {}".format(
            #         service_address_recipient.value,
            #         service_address_recipient.confidence,
            #     )
            # )
            invoice_field["ServiceAddressRecipient"] = service_address_recipient.value + "|"
            #record_item = record_item + "service_address_recipient.value" + "|"
        else:
            invoice_field["ServiceAddressRecipient"] = invoice_field["ServiceAddressRecipient"] + "|"
        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            # print(
            #     "Remittance Address: {} has confidence: {}".format(
            #         remittance_address.value, remittance_address.confidence
            #     )
            # )
            remittance_address_string = ' '.join(str(remittance_address.value.to_dict()[x]) for x in remittance_address.value.to_dict()).replace(" None","").replace("None ","")
            invoice_field["RemittanceAddress"] = remittance_address_string + "|"
            #record_item = record_item + remittance_address.value + "|"
            #record_item = record_item + "remittance_address.value" + "|"
        else:
            invoice_field["RemittanceAddress"] = invoice_field["RemittanceAddress"] + "|"
        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            # print(
            #     "Remittance Address Recipient: {} has confidence: {}".format(
            #         remittance_address_recipient.value,
            #         remittance_address_recipient.confidence,
            #     )
            # )
            invoice_field["RemittanceAddressRecipient"] = remittance_address_recipient.value + "|"
            #record_item = record_item + "remittance_address_recipient.value" + "|"
        else:
            invoice_field["RemittanceAddressRecipient"] = invoice_field["RemittanceAddressRecipient"] + "|"

        print("Invoice items:")
        #csv_file = open("csv_file.csv", "w")
        try:
            for idx, item in enumerate(invoice.fields.get("Items").value):
                #print("...Item #{}".format(idx + 1))
                record_item0 = ""
                item_description = item.value.get("Description")
                if item_description:
                    # print(
                    #     "......Description: {} has confidence: {}".format(
                    #         item_description.value, item_description.confidence
                    #     )
                    # )
                    invoice_field["Description"] = item_description.value + "|"
                else:
                    invoice_field["Description"] = "No Data|"
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    # print(
                    #     "......Quantity: {} has confidence: {}".format(
                    #         item_quantity.value, item_quantity.confidence
                    #     )
                    # )
                    invoice_field["Quantity"] = "{}".format(item_quantity.value) + "|"
                else:
                    invoice_field["Quantity"] = "No Data|"
                unit = item.value.get("Unit")
                if unit:
                    # print(
                    #     "......Unit: {} has confidence: {}".format(
                    #         unit.value, unit.confidence
                    #     )
                    # )
                    invoice_field["Unit"] = unit.value + "|"
                else:
                    invoice_field["Unit"] = "No Data|"
                unit_price = item.value.get("UnitPrice")
                if unit_price:
                    # print(
                    #     "......Unit Price: {} has confidence: {}".format(
                    #         unit_price.value, unit_price.confidence
                    #     )
                    # )
                    invoice_field["UnitPrice"] = "{}".format(unit_price.value) + "|"
                else:
                    invoice_field["UnitPrice"] = "No Data|"
                product_code = item.value.get("ProductCode")
                if product_code:
                    # print(
                    #     "......Product Code: {} has confidence: {}".format(
                    #         product_code.value, product_code.confidence
                    #     )
                    # )
                    invoice_field["ProductCode"] = product_code.value + "|"
                else:
                    invoice_field["ProductCode"] = "No Data|"
                item_date = item.value.get("Date")
                if item_date:
                    # print(
                    #     "......Date: {} has confidence: {}".format(
                    #         item_date.value, item_date.confidence
                    #     )
                    # )
                    invoice_field["Date"] = "{}".format(item_date.value) + "|"
                else:
                    invoice_field["Date"] = "No Data|"
                tax = item.value.get("Tax")
                if tax:
                    # print(
                    #     "......Tax: {} has confidence: {}".format(tax.value, tax.confidence)
                    # )
                    invoice_field["Tax"] = tax.value + "|"
                else:
                    invoice_field["Tax"] = "No Data|"
                amount = item.value.get("Amount")
                if amount:
                    # print(
                    #     "......Amount: {} has confidence: {}".format(
                    #         amount.value, amount.confidence
                    #     )
                    # )
                    invoice_field["Amount"] = "{}".format(amount.value) + "|"
                else:
                    invoice_field["Amount"] = "No Data|"
                #record_item0 = record_item0.replace("\n", "")
                #record_item = record_item.replace("\n", "")
                record_item = ""
                for field in doc_fields.split(','):
                    try:
                        field_data = invoice_field[field].replace("\n", "")
                        record_item = record_item + invoice_field[field].replace("\n", "")
                    except:
                        record_item = record_item + "No Data|"
                
                reccord_items.append(record_item)
                #print(record_item)
                #csv_file = open(filein.replace(".pdf",".csv"), "a")
                #csv_file.write(record_item+record_item0+"|%s\n" % i)
                #csv_file.close()
            # csv_file = open("csv_file.csv", "w")
            # csv_file.write(record_item+record_item0+"\n")
            # csv_file.close()
            print("----------------------------------------")
        except:
            print("------ No Item -------")
            record_item0 = "||||||||"
            record_item = record_item.replace("\n", "")
            reccord_items.append(record_item+record_item0)
            print(record_item+record_item0)
            #csv_file = open(filein.replace(".pdf",".csv"), "a")
            #csv_file.write(record_item+record_item0+"|%s\n" % i)
            #csv_file.close()
    return reccord_items


def _azure_formrecognize_invoice1(a_endpoint,a_key,doc_path):
    reccord_items = []
    document_analysis_client = DocumentAnalysisClient(
    endpoint=a_endpoint, credential=AzureKeyCredential(a_key)
    )
    with open(doc_path, "rb") as f:
       poller = document_analysis_client.begin_analyze_document(
           "prebuilt-invoice", document=f, locale="th-TH"
       )
    #poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", document=outputStream, locale="en-US")
    invoices = poller.result()
    for idx, invoice in enumerate(invoices.documents):
        record_item = ""
        #print("-------- Page {} ----------".format(i + 1))
        #print("--------Recognizing invoice #{}--------".format(idx + 1))
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            # print(
            #     "Vendor Name: {} has confidence: {}".format(
            #         vendor_name.value, vendor_name.confidence
            #     )
            # )
            record_item = vendor_name.value + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            # print(
            #     "Vendor Address: {} has confidence: {}".format(
            #         vendor_address.value, vendor_address.confidence
            #     )
            # )
            vendor_address_string = ' '.join(str(vendor_address.value.to_dict()[x]) for x in vendor_address.value.to_dict()).replace(" None","").replace("None ","")
            record_item = record_item + vendor_address_string + "|"
            #record_item = record_item + "{}".format(vendor_address.value.to_dict()) + "|"
            #record_item = record_item + "vendor_address.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            # print(
            #     "Vendor Address Recipient: {} has confidence: {}".format(
            #         vendor_address_recipient.value, vendor_address_recipient.confidence
            #     )
            # )
            record_item = record_item + vendor_address_recipient.value + "|"
            #record_item = record_item + "vendor_address_recipient.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            # print(
            #     "Customer Name: {} has confidence: {}".format(
            #         customer_name.value, customer_name.confidence
            #     )
            # )
            record_item = record_item + customer_name.value + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            # print(
            #     "Customer Id: {} has confidence: {}".format(
            #         customer_id.value, customer_id.confidence
            #     )
            # )
            record_item = record_item + customer_id.value + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            # print(
            #     "Customer Address: {} has confidence: {}".format(
            #         customer_address.value, customer_address.confidence
            #     )
            # )
            customer_address_string = ' '.join(str(customer_address.value.to_dict()[x]) for x in customer_address.value.to_dict()).replace(" None","")
            record_item = record_item + customer_address_string + "|"
            #record_item = record_item + "{}".format(customer_address.value) + "|"
            #record_item = record_item + "customer_address.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            # print(
            #     "Customer Address Recipient: {} has confidence: {}".format(
            #         customer_address_recipient.value,
            #         customer_address_recipient.confidence,
            #     )
            # )
            record_item = record_item + customer_address_recipient.value + "|"
            #record_item = record_item + "customer_address_recipient.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            # print(
            #     "Invoice Id: {} has confidence: {}".format(
            #         invoice_id.value, invoice_id.confidence
            #     )
            # )
            record_item = record_item + invoice_id.value + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            # print(
            #     "Invoice Date: {} has confidence: {}".format(
            #         invoice_date.value, invoice_date.confidence
            #     )
            # )
            record_item = record_item + invoice_date.value.strftime('%d/%m/%Y') + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            # print(
            #     "Invoice Total: {} has confidence: {}".format(
            #         invoice_total.value, invoice_total.confidence
            #     )
            # )
            record_item = record_item + "{}".format(invoice_total.value) + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        due_date = invoice.fields.get("DueDate")
        if due_date:
            # print(
            #     "Due Date: {} has confidence: {}".format(
            #         due_date.value, due_date.confidence
            #     )
            # )
            record_item = record_item + "{}".format(due_date.value) + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            # print(
            #     "Purchase Order: {} has confidence: {}".format(
            #         purchase_order.value, purchase_order.confidence
            #     )
            # )
            record_item = record_item + purchase_order.value + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            # print(
            #     "Billing Address: {} has confidence: {}".format(
            #         billing_address.value, billing_address.confidence
            #     )
            # )
            billing_address_string = ' '.join(str(billing_address.value.to_dict()[x]) for x in billing_address.value.to_dict()).replace(" None","")
            record_item = record_item + billing_address_string + "|"
            #record_item = record_item + billing_address.value + "|"
            #record_item = record_item + "billing_address.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            # print(
            #     "Billing Address Recipient: {} has confidence: {}".format(
            #         billing_address_recipient.value,
            #         billing_address_recipient.confidence,
            #     )
            # )
            record_item = record_item + billing_address_recipient.value + "|"
            #record_item = record_item + "billing_address_recipient.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            # print(
            #     "Shipping Address: {} has confidence: {}".format(
            #         shipping_address.value, shipping_address.confidence
            #     )
            # )
            shipping_address_string = ' '.join(str(shipping_address.value.to_dict()[x]) for x in shipping_address.value.to_dict()).replace(" None","")
            record_item = record_item + shipping_address_string + "|"
            #record_item = record_item + "{}".format(shipping_address.value) + "|"
            #record_item = record_item + "shipping_address.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            # print(
            #     "Shipping Address Recipient: {} has confidence: {}".format(
            #         shipping_address_recipient.value,
            #         shipping_address_recipient.confidence,
            #     )
            # )
            record_item = record_item + shipping_address_recipient.value + "|"
            #record_item = record_item + "shipping_address_recipient.value" + "|"
            #print(record_item)
        else:
            record_item = record_item + "" + "|"
        #print(record_item)    
        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            # print(
            #     "Subtotal: {} has confidence: {}".format(
            #         subtotal.value, subtotal.confidence
            #     )
            # )
            record_item = record_item + "{}".format(subtotal.value) + "|"
        else:
            record_item = record_item + "" + "|"
        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            # print(
            #     "Total Tax: {} has confidence: {}".format(
            #         total_tax.value, total_tax.confidence
            #     )
            # )
            record_item = record_item + "{}".format(total_tax.value) + "|"
        else:
            record_item = record_item + "" + "|"
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            # print(
            #     "Previous Unpaid Balance: {} has confidence: {}".format(
            #         previous_unpaid_balance.value, previous_unpaid_balance.confidence
            #     )
            # )
            record_item = record_item + previous_unpaid_balance.value + "|"
        else:
            record_item = record_item + "" + "|"
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            # print(
            #     "Amount Due: {} has confidence: {}".format(
            #         amount_due.value, amount_due.confidence
            #     )
            # )
            record_item = record_item + "{}".format(amount_due.value) + "|"
        else:
            record_item = record_item + "" + "|"
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            # print(
            #     "Service Start Date: {} has confidence: {}".format(
            #         service_start_date.value, service_start_date.confidence
            #     )
            # )
            record_item = record_item + "{}".format(service_start_date.value) + "|"
        else:
            record_item = record_item + "" + "|"
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            # print(
            #     "Service End Date: {} has confidence: {}".format(
            #         service_end_date.value, service_end_date.confidence
            #     )
            # )
            record_item = record_item + service_end_date.value + "|"
        else:
            record_item = record_item + "" + "|"
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            # print(
            #     "Service Address: {} has confidence: {}".format(
            #         service_address.value, service_address.confidence
            #     )
            # )
            service_address_string = ' '.join(str(service_address.value.to_dict()[x]) for x in service_address.value.to_dict()).replace(" None","")
            record_item = record_item + service_address_string + "|"
            #record_item = record_item + service_address.value + "|"
            #record_item = record_item + "service_address.value" + "|"
        else:
            record_item = record_item + "" + "|"
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            # print(
            #     "Service Address Recipient: {} has confidence: {}".format(
            #         service_address_recipient.value,
            #         service_address_recipient.confidence,
            #     )
            # )
            record_item = record_item + service_address_recipient.value + "|"
            #record_item = record_item + "service_address_recipient.value" + "|"
        else:
            record_item = record_item + "" + "|"
        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            # print(
            #     "Remittance Address: {} has confidence: {}".format(
            #         remittance_address.value, remittance_address.confidence
            #     )
            # )
            remittance_address_string = ' '.join(str(remittance_address.value.to_dict()[x]) for x in remittance_address.value.to_dict()).replace(" None","")
            record_item = record_item + remittance_address_string + "|"
            #record_item = record_item + remittance_address.value + "|"
            #record_item = record_item + "remittance_address.value" + "|"
        else:
            record_item = record_item + "" + "|"
        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            # print(
            #     "Remittance Address Recipient: {} has confidence: {}".format(
            #         remittance_address_recipient.value,
            #         remittance_address_recipient.confidence,
            #     )
            # )
            record_item = record_item + remittance_address_recipient.value + "|"
            #record_item = record_item + "remittance_address_recipient.value" + "|"
        else:
            record_item = record_item + "" + "|"

        print("Invoice items:")
        #csv_file = open("csv_file.csv", "w")
        try:
            for idx, item in enumerate(invoice.fields.get("Items").value):
                #print("...Item #{}".format(idx + 1))
                record_item0 = ""
                item_description = item.value.get("Description")
                if item_description:
                    # print(
                    #     "......Description: {} has confidence: {}".format(
                    #         item_description.value, item_description.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + item_description.value + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    # print(
                    #     "......Quantity: {} has confidence: {}".format(
                    #         item_quantity.value, item_quantity.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + "{}".format(item_quantity.value) + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                unit = item.value.get("Unit")
                if unit:
                    # print(
                    #     "......Unit: {} has confidence: {}".format(
                    #         unit.value, unit.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + unit.value + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                unit_price = item.value.get("UnitPrice")
                if unit_price:
                    # print(
                    #     "......Unit Price: {} has confidence: {}".format(
                    #         unit_price.value, unit_price.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + "{}".format(unit_price.value) + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                product_code = item.value.get("ProductCode")
                if product_code:
                    # print(
                    #     "......Product Code: {} has confidence: {}".format(
                    #         product_code.value, product_code.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + product_code.value + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                item_date = item.value.get("Date")
                if item_date:
                    # print(
                    #     "......Date: {} has confidence: {}".format(
                    #         item_date.value, item_date.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + "{}".format(item_date.value) + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                tax = item.value.get("Tax")
                if tax:
                    # print(
                    #     "......Tax: {} has confidence: {}".format(tax.value, tax.confidence)
                    # )
                    record_item0 = record_item0 + tax.value + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                amount = item.value.get("Amount")
                if amount:
                    # print(
                    #     "......Amount: {} has confidence: {}".format(
                    #         amount.value, amount.confidence
                    #     )
                    # )
                    record_item0 = record_item0 + "{}".format(amount.value) + "|"
                else:
                    record_item0 = record_item0 + "" + "|"
                record_item0 = record_item0.replace("\n", "")
                record_item = record_item.replace("\n", "")
                reccord_items.append(record_item+record_item0)
                print(record_item+record_item0)
                #csv_file = open(filein.replace(".pdf",".csv"), "a")
                #csv_file.write(record_item+record_item0+"|%s\n" % i)
                #csv_file.close()
            # csv_file = open("csv_file.csv", "w")
            # csv_file.write(record_item+record_item0+"\n")
            # csv_file.close()
            print("----------------------------------------")
        except:
            print("------ No Item -------")
            record_item0 = "||||||||"
            record_item = record_item.replace("\n", "")
            reccord_items.append(record_item+record_item0)
            print(record_item+record_item0)
            #csv_file = open(filein.replace(".pdf",".csv"), "a")
            #csv_file.write(record_item+record_item0+"|%s\n" % i)
            #csv_file.close()
    return reccord_items


#result =   _azure_formrecognize_invoice("https://formrecogtestapi.cognitiveservices.azure.com/","d2ba74e3b23f4072b6ed4e1085a33ca7","/Users/mondmalt/Downloads/ocr/PO3.pdf","VendorName,VendorAddress,VendorAddressRecipient,CustomerName,CustomerId,CustomerAddress,CustomerAddressRecipient,InvoiceId,InvoiceDate,InvoiceTotal,DueDate,TestAddOnField,ShippingAddress,ShippingAddressRecipient,Description,Quantity,TestAddOnField,Date,Unit,Amount")
#print(result)