import json
import requests
import time
from fpdf import FPDF
import pprint
import xlsxwriter


def read_id(key ,cast, lat, lng, npage):
    path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    if npage == False:
        params = {
        'key' : key,
        'keyword' : cast,
        'location' : str(lat) + "," + str(lng),
        'radius' : "40000",
        }
    else:
        print("Token: '" + npage + "'")
        params = {
        'key' : key,
        'pagetoken' : npage, 
        }
       
    print("+Sending Request To Google Api")
    print("-Parameters:", params)
    print("-Return Type: json")
    print("")
    response = requests.get(path,params)
    print("Request:")
    print(response.request.url)
    print("+Response: " + str(response.status_code))
    place_ids = json.loads(response.text)
    del params
    try:
        return place_ids, response.status_code, place_ids['status'], place_ids['next_page_token']
    except:
        return place_ids, response.status_code, place_ids['status'], False

def read_data(key, plid):
    path = "https://maps.googleapis.com/maps/api/place/details/json?"
    params = {
    'key' : key,
    'place_id' : plid,
    'fields' : "name,formatted_address,formatted_phone_number,website"
    }
    print("+Sending Request To Google Api")
    print("-Parameters:", params)
    print("-Return Type: json")
    print("")
    response = requests.get(path,params)
    place = json.loads(response.text)
    print("Request:")
    print(response.request.url)
    print("+Response: " + str(response.status_code)) 
    return place,place['status']


def save_id(data, name):
    plidfile = open(name, 'a')
    for item in data['results']:
        plidfile.write(item['place_id'] + "\n")
    plidfile.close()

def generate_pdf(data, filename):
    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font("DejaVu", '', size=12)
    for item in data:
        txt=item['result']['name'] + "     " + item['result']['formatted_phone_number'] + "  /  " + item['result']["formatted_address"] + " # " + item['result']['website']
        pdf.write(8,txt)
        pdf.ln(8)
    pdf.output(filename)

def generate_xlsx(data, filename):
    out_dict = {'name' : [], 'phone' : [], 'address' : [], 'website' : []}
    for item in data:
        try:
            out_dict['name'].append(item['result']['name'])
        except:
            out_dict['name'].append("None")
        try:    
            out_dict['phone'].append(item['result']['formatted_phone_number'])
        except:
            out_dict['phone'].append("None")
        try:
            out_dict['address'].append(item['result']['formatted_address'])
        except:
            out_dict['address'].append("None")
        try:
            out_dict['website'].append(item['result']['website'])
        except:
            out_dict['website'].append("None")
    row = 0
    col = 0
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    
    for col, item in enumerate(out_dict.values()):
        for row, value in enumerate(item):
            worksheet.write(row, col, value)
    
    workbook.close()
