# Web_Scraper
A web scraper which extracts supplier infromation for given products from IndiaMart and Facebook

## Brief
This repository consists of the web scraping code which mines supplier information for a given product from <a href="https://my.indiamart.com/">India Mart</a> website. Functions for finding the <a href="https://www.facebook.com/">Facebook</a> accounts of different suppliers are also included.   

## Files:
* main.py - Main python script to run
* webscraper.py - Web Scraping code
* fb_data.py - Facebook page retrieval code 
* city.txt - List of cities
* products.txt - List of products
* business.txt - Types of businesses
  * Wholesaler
  * Manufacturer
  * Exporter
  * Retailer
* chromedriver.exe - Chrome driver (version = 97.0.4692.71) 
* requirements.txt - List of libraries to be installed

## Usage:
* Install the required libraries mentioned in requirements.txt (pip install -r requirements.txt)
* Update the files products.txt and city.txt as per your requirements  
* Run main.py
* The data will be extracted and stored in a new directory named "data"

## Retrieved Data Output:

The output is a directory named data. It contains csv files in the file structure mentioned below.
File structure:
* data
  * product_1
    * city_buisness.csv
  * product_2
    * city_buisness.csv

The csv files consist of the following columns:
* Company name
* Address
* Link
* Phone number
* Items
* City
* Buisness category
* Facebook page link*
* Email ID*

## Notes:
* Download link for Chrome driver: https://chromedriver.chromium.org/downloads
* While updating cities.txt, make sure that white spaces or commas are not included after the city names
* Facebook pages are only retrieved for particular cities (which are listed in fb_data.py)
* For cities not included in fb_data.py, the Facebook and email ID columns will not be present in the csv file  
* Email-Ids are also extracted only if they are present in the facebook page
* In the case where multiple email IDs are present for a single facebook page, the retrieved email IDs could be spurious
* As the code uses selenium for facebook pages, Chrome browser tabs could open up and close automatically to retrieve data.  
* **IMPORTANT: Trying to extract a large amount of data from facebook contiuously, could get your account banned** 
