"""
Pull down all of the foreclosures for Jefferson County Colorado.
"""

from selenium import webdriver
import pandas as pd

url = "http://gts.co.jefferson.co.us/index.aspx"
# create a new Firefox session
driver = webdriver.Firefox(executable_path='C:/Users/kirst/Downloads/geckodriver-v0.26.0-win64/geckodriver.exe')
driver.implicitly_wait(30)
driver.get(url)

#Accept terms
accept_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnAcceptTerms")
accept_button.click()

#Wait 10 seconds for the load
driver.implicitly_wait(10)

#Select the 'Show All' option
accept_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnShowAll")
accept_button.click()

df = pd.DataFrame(columns = ["FC #", "Owner Name", "Street", "Zip", "Subdivision", "Balance Due", "Status"])
#Flip through all of the records and save them

for n in range(2, 16):
    for i in range(3):
        try:
            mytable = driver.find_element_by_css_selector("table[id='ctl00_ContentPlaceHolder1_gvSearchResults']")
            #Read in all of the data into the dataframe
            for row in mytable.find_elements_by_css_selector('tr'):
                row_list = []
                #Add to dataframe accordingly
                for cell in row.find_elements_by_css_selector('td'):
                    cell_reading = cell.text
                    row_list.append(cell_reading)
                #Add the list as a row, if possible 
                try:
                    a_series = pd.Series(row_list, index = df.columns)
                    df = df.append(a_series, ignore_index=True)
                except:
                    print("Could not append: " + str(row_list))
            break
        except:
            driver.implicitly_wait(5)
    if n%10 == 1:
        #Click second "..." if on greater than page 10
        if n < 20:
            driver.find_elements_by_xpath("//td/a[text()='...']")[0].click()  
        else:
            driver.find_elements_by_xpath("//td/a[text()='...']")[1].click()  
    else:
        driver.find_element_by_xpath("//td/a[text()='" + str(n)+ "']").click()    
    #Wait three seconds so the website doesn't crash
    driver.implicitly_wait(3)

#Write to a csv
df.to_csv("jefferson_county_foreclosures.csv", index= False)