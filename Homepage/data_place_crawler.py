from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import pandas as pd




def data_place_crawler():
    
    chrome_driver_path = 'chromedriver.exe'

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    errorMessage = print("Something went wrong, please check terminal console for more details.")

    dfPlace = []


    #time.sleep(100)
    foodID_list =[]
    businessName_list =[]
    url_list =[]

    food_list = (pd.read_csv("place_url.csv")['foodid'])
    placeURL_list = (pd.read_csv("place_url.csv")['placeURL'])
    foodPlace_dict = dict(zip(food_list, placeURL_list))

    for food, url in foodPlace_dict.items():
        driver.get(url)
        time.sleep(3)

        #Find scroll layout
        scrollable_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
        #Scroll as many times as necessary to load all reviews
        for i in range(0,2):
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                        scrollable_div)
                time.sleep(3)


        businessDetail = driver.find_elements(By.CLASS_NAME, "hfpxzc")

        for lnk in businessDetail:
            foodID_list.append(food)
            businessName_list.append(lnk.get_attribute('aria-label'))
            url_list.append(lnk.get_attribute('href'))

    df = pd.DataFrame(list(zip(foodID_list,businessName_list, url_list)),
                    columns=['Food ID','Business Name', 'URL Link'])
    
    print(df)
    df.to_csv(r'google_place.csv',index=False)

    dfPlace = df.values.tolist()
    messageComplete = "Completed!"

    return dfPlace , messageComplete




    