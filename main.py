# Imports
import os
from webscraper import dataFind

# Read cities.txt file and format it according to the http request
def get_cities():
    a_file = open("cities.txt", "r")
    cities = []
    for line in a_file:
        stripped_line = line.strip()
        line_list = (stripped_line.replace(' ', '-')).lower()
        cities.append(line_list)
    a_file.close()
    return cities

# Read business.txt file and format it according to the http request
def get_business():
    a_file = open("business.txt", "r")
    business = []
    for line in a_file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        business.append(line_list)
    return business

# Read products.txt file and format it according to the http request
def get_products():
    a_file = open("products.txt", "r")
    products = []
    for line in a_file:
        stripped_line = line.strip()
        line_list = (stripped_line.replace(' ', '-')).lower()
        products.append(line_list)
    a_file.close()
    return products

# Main function
def main():
    cities = get_cities()
    businesses = get_business()
    products = get_products()
    flag = 1
    no_business_found = open("no_business_found.csv","w")
    product_found = open("product_found.csv","w")
    error_404 = open("error_404.csv","w")
    i,j = 0,0
    
    # Each product can be found in any of the 126 cities and in each city there are 4 business types
    for product in products:
        i+=1
        flag = 1
        j=0
        for city in cities:
            j+=1
            if j%10 == 0:
                os.system('cls')
            print(i,": ",product,"count_cities: ",j)
            for business in businesses:
                temp = dataFind(city,product,business)
                if(temp == 1):
                    product_found.write(city+","+product+","+business[0]+"\n")
                elif(temp == 0):
                    no_business_found.write(city+","+product+","+business[0]+"\n")
                else:
                    error_404.write(product+"\n")
                    flag = 0        
                    break
            if (not flag):
                break
    
    no_business_found.close()
    product_found.close()
    error_404.close()

if __name__=="__main__":
    main()
