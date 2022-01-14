# Imports
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fb_data import get_email

# Display the details of the suppliers in each city for 1 business type at a time
def display(company,address,phone_no,items_list,link):
    for i in range(len(company)):
        print("Company: ",company[i])
        print("Link: ",link[i])
        print("Address: ",address[i])
        print("Phone Number: ",phone_no[i])        
        print("Items List: ",items_list[i])

# Writes retrieved data into .csv files 
def writeCSV(company, address, phone_no, items_list, link,city,product,bus):
    cities_temp = ["Ahmedabad","Agra","Bengaluru","Bhopal","Chennai","Chandigarh","Delhi","Firozabad","Gwalior","Guwahati","Gurgaon","Hyderabad","Jaipur","Kanchipuram","Kolkata"] 
    cities = [i.lower() for i in cities_temp]
    if city.lower() in cities:
        if len(company)>10:
            email,fb = get_email(company[:10])
            supplier_det = pd.DataFrame({
                'Company': company[:10],
                'Address': address[:10],
                'Website Link': link[:10],
                'Phone_no': phone_no[:10],
                'Items': items_list[:10],
                'City': [city for _ in range(10)],
                'Category': [bus[0] for _ in range(10)],
                'FB_Page':fb[:10],
                'Email': email[:10]
            })
        else:
            email,fb = get_email(company)
            supplier_det = pd.DataFrame({
                'Company': company,
                'Address': address,
                'Website Link':link,
                'Phone_no': phone_no,
                'Items': items_list,
                'City': [city for _ in range(len(company))],
                'Category': [bus[0] for _ in range(len(company))],
                'FB_Page':fb[:len(company)],
                'Email': email[:len(company)]
            })
    else:
        supplier_det = pd.DataFrame({
                'Company': company,
                'Address': address,
                'Website Link':link,
                'Phone_no': phone_no,
                'Items': items_list,
                'City': [city for _ in range(len(company))],
                'Category': [bus[0] for _ in range(len(company))]
            })

    if not os.path.exists("./data/"+product):
        os.makedirs("./data/"+product)
    supplier_det.to_csv("./data/"+product+"/"+city+"_"+bus[0]+".csv")

# Search for a given product using inbuilt search-engine of IndiaMart 
# Returns 1 -> successful retrieval of data, 0 -> blank html page, -1 -> page not found 
def searchRlt(city,product,bus):
    timeout=10
    items_list = []
    # Product to be searched along with city and business type in URL format 
    response = requests.get("https://dir.indiamart.com/search.mp?ss="+product+"&"+bus[1]+"&cq="+city)
    # To tackle page not found http reply
    if response.status_code==404:
        return -1
    # To tackle too many requests http reply
    while (response.status_code==429 and timeout>0):
        time.sleep(1)
        timeout-=1
        response = requests.get("https://dir.indiamart.com/search.mp?ss="+product+"&"+bus[1]+"&cq="+city)
        if response.status_code==404:
            return -1
    
    # Read html page of the above mentioned URL
    soup=BeautifulSoup(response.text,'html.parser')
    suppliers = soup.find_all(class_="prd-bottom imgc fww flx100 ase rdhvr")
    parents = soup.find_all(class_="lst_cl")
    if len(suppliers)==0:
        return 0

    # Finding classes corresponding to the requirement fields(Company names,address,phone_no) and data retrieval 
    company_temp = [supplier.find(class_ = "clr3 fs12 fwn rsrc") for supplier in suppliers if supplier.find(class_ = "clr3 fs12 fwn rsrc")]
    company = [t.getText() for t in company_temp]
    link = [t.get('href') for t in company_temp]   
    address_temp = [supplier.find(class_ = "tac") for supplier in suppliers if supplier.find(class_ = "tac")]
    address = [t.getText() for t in address_temp]
    phone_no = [p.find(class_="pns_h duet fwb").getText() for p in parents]
    phone_no = [t.replace("Ext ","-") for t in phone_no]

    # List of items sold by each company  
    for supplier in parents:
        if supplier.find_all(class_ = "prd-name"):
            items=[]
            for item in  supplier.find_all(class_ = "prd-name"):
                items.append(item.getText())
            items_list.append(list(set(items)))

    # Uncomment the next line to display the contents only if necessary
    #display(company, address, phone_no, items_list, link)
    writeCSV(company, address, phone_no, items_list, link,city,product,bus)
    return 1

# Search for a given product using predefined http request format
# Returns 1 -> successful retrieval of data
def dataFind(city,product,bus):
    timeout=10
    data_print=1
    items_list = []
    # Product to be searched along with city and business type in URL format
    response = requests.get("https://dir.indiamart.com/"+city+"/"+product+"-all.html?"+bus[1])
    # To tackle page not found http reply
    if response.status_code==404:
        data_print=0    
        searchRlt(city,product,bus)
    # To tackle too many requests http reply
    while (response.status_code==429 and timeout>0):
        time.sleep(1)
        timeout-=1
        response = requests.get("https://dir.indiamart.com/"+city+"/"+product+"-all.html"+bus[1])
        if response.status_code==404:
            data_print=0    
            searchRlt(city,product,bus)

    # Read html page of the above mentioned URL
    soup=BeautifulSoup(response.text,'html.parser')
    suppliers = soup.find_all( class_ = "lst_cl" )
    if len(suppliers)==0:
        data_print=0 
        searchRlt(city,product,bus)

    # Finding classes corresponding to the requirement fields(Company names,address,phone_no) and data retrieval 
    company_temp = [supplier.find(class_ = "gcnm") for supplier in suppliers if supplier.find(class_ = "gcnm")]
    company = [t.getText() for t in company_temp]
    link = [t.get('href') for t in company_temp]
    address_temp = [supplier.find(class_ = "cty-t") for supplier in suppliers if supplier.find(class_ = "cty-t")]
    address = [t.getText() for t in address_temp]
    temp = [supplier.select(".bo") for supplier in suppliers if supplier.select(".bo")]
    phone_no = [str(t[0].getText()[4:]).replace(",","-") for t in temp]

    # List of items sold by each company  
    for supplier in suppliers:
        if supplier.find_all(class_ = "cp5"):
            items=[]
            for item in  supplier.find_all(class_ = "cp5"):
                items.append(item.getText())
            items_list.append(list(set(items)))

    # Uncomment the next line to display the contents only if necessary
    #display(company, address, phone_no, items_list, link) 
    if(data_print==1):
        writeCSV(company, address, phone_no, items_list, link,city,product,bus)
    return 1