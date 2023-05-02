from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

def data_crawlers(request):
    chrome_driver_path = r"chromedriver.exe"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    errorMessage = print("Something went wrong, please check terminal console for more details.")

    try :
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
    except:
        errorMessage

    ############## End of place crawler ###################
    # dictionary
    try:
        foodID_list =[]
        userID_Rlist = []
        name_list = []
        stars_Rlist = []
        duration_list = []

        placeURL_list = (pd.read_csv("google_place.csv")['URL Link'])
        food_list = (pd.read_csv("google_place.csv")['Food ID'])
        foodPlace_dict = dict(zip(placeURL_list, food_list))

        for url, food in foodPlace_dict.items():
            driver.get(url)
            time.sleep(5)

            #click review tab
            driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]').click()
            time.sleep(1)

            #click Sort button
            driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[7]/div[2]/button').click()
            time.sleep(1)

            #click sort by newest
            driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]').click()

            time.sleep(5)

            SCROLL_PAUSE_TIME = 1

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            number = 0

            while True:
                number = number + 1

                # Scroll down to bottom

                ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')

                driver.execute_script('arguments[0].scrollBy(0, 8000);', ele)

                # Wait to load page

                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                print(f'last height: {last_height}')

                ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')

                new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

                print(f'new height: {new_height}')

                if number == 2:
                    break

                if new_height == last_height:
                    break

                print('cont')
                last_height = new_height

            item = driver.find_elements(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]')

            time.sleep(3)

            for i in item:
                userID = i.find_elements(By.CLASS_NAME, "WEBjve")
                name = i.find_elements(By.CLASS_NAME, "d4r55")
                stars = i.find_elements(By.CLASS_NAME, "kvMYJc")
                duration = i.find_elements(By.CLASS_NAME, "rsqaWe")

                for j,k,l,p in zip(userID, name, stars, duration):
                    foodID_list.append(food)
                    userID_Rlist.append(j.get_attribute('href'))
                    name_list.append(k.text)
                    stars_Rlist.append(l.get_attribute("aria-label"))
                    duration_list.append(p.text)

        #transform
        userID_list =re.findall(r'\d+', str(userID_Rlist))
        stars_list =re.findall(r'\d+', str(stars_Rlist))

        dfTwo = pd.DataFrame(list(zip(foodID_list,userID_list, name_list, stars_list, duration_list)),
                                columns=['Food ID','userID', 'name', 'rating', 'duration'])
        print(dfTwo)

        dfTwo["userid;name"] = dfTwo['userID'] +";"+ dfTwo["name"]

        dfTwo.to_excel(r'google_review.xlsx',index=False)
        dfTwo["userid;name"].to_excel(r'UserID.xlsx',index=False)
    except:
        errorMessage
        
    return df, dfTwo



    