# Imports
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Email ID scraping from FB accounts
def get_email(company_list):

    # Provide user id and password of the facebook account (Its better to use an account other than your personal one)
    usr= 'ENTER YOUR FACEBOOK ACCOUNT USERNAME HERE'
    pwd = 'ENTER YOUR FACEBOOK ACCOUNT PASSWORD HERE'
    
    # Login to facebook using above credentials
    fb_list=[]
    timeout = 2
    email_id_list=[]
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://www.facebook.com/')
    sleep(1)
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(usr)
    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd)
    login_box = driver.find_element_by_name('login')
    login_box.click()

    # Avoiding Exceptions 
    try:
        element_present = EC.presence_of_element_located((By.ID, 'MANIFEST_LINK'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        return [],[]

    # Seperating FB links from FB pages
    for company_name in company_list:
        flg=0
        anchor_attribute=[]
        http_formatted_company_name=company_name.replace(" ","%20")
        driver.get("https://www.facebook.com/search/?q="+http_formatted_company_name)
        sleep(2)
        html = driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        temp_list_1=soup.find_all("a")
        for i in temp_list_1:
                if str('aria-label="'+company_name+'"') in str(i):
                    anchor_attribute.append(i)
        if(anchor_attribute!=[]):
            temp=str(anchor_attribute)[str(anchor_attribute).find("href")+6:]
            index1=temp.find('"')
            fb_links=temp[:index1]
            fb_list.append(fb_links)
            flg=1
        else:
            temp_list_2=soup.find_all("a")
            fb_posts_list=[]
            for i in temp_list_2:
                if "oajrlxb2 g5ia77u1" in str(i):
                    fb_posts_list.append(i)
            for item in fb_posts_list:
                if company_name in item.getText():
                    temp=str(item)[str(item).find("href")+6:]
                    index1=temp.find('"')
                    fb_links=temp[:index1]
                    fb_list.append(fb_links)
                    flg=1
                    break
        if flg==0:
            fb_list.append("")

    # Seperating email ids from FB pages
    for link in fb_list:
        flg=0
        if link!="":
            try:
                driver.get(link)
                sleep(2)
            except Exception:
                email_id_list.append("")
                flg=1
            if flg==0:
                html = driver.page_source
                soup=BeautifulSoup(html,'html.parser')
                temp_list_2=soup.find_all("a")
                for item in temp_list_2:
                    if "@" in item.getText():
                        if 'role="link"' in str(item):
                            if "oajrlxb2" in str(item):
                                email_id_list.append(item.getText())
                                flg=1
                                break
        if(flg==0):
            email_id_list.append("")

    # Logout of your FB account
    driver.quit()
    return email_id_list,fb_list