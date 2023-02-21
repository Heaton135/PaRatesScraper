import os
from pickle import TRUE
import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
from pathlib import Path  
from selenium.common.exceptions import NoSuchElementException
import colorama
from colorama import Fore


# Sets our default browser to chrome, passing in specific options such as download directory
driver = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
# Change download directory to wherever this program is on your machine
cwd = os.getcwd()

# Set our preferred options for chrome webdriver
prefs = {'download.default_directory' : cwd}
chrome_options.add_experimental_option('prefs', prefs)

# This dataframe will serve as our repository for all data until we are ready to export all results at the end
global fullData 
fullData = pd.DataFrame(columns = ['Price', 'Supplier', 'Type', 'Cancellation Fee', 'Discounts available?',
       'Introductory price?', 'More info', 'Service Type', 'Rate type',
       'Term Length', 'PA wind', 'Renewable Energy', 'Term End Date',
       'Enrollment Fee', 'Monthly service fee amount', 'date', 'zipcode'])

# Pass in our custom options to chrome
driver = webdriver.Chrome(chrome_options=chrome_options)

def main():
    print("---------------------------------")
    print("\nWelcome to PA rates scraper!..")
    print("Gathering Zip Codes...\n")

    # Gets zip codes 
    # zips = getZips()
    # Setting a global variable to hold all of our data.
    global fullData
    print("\n-------- Begin Scraping ---------\n")
    
    # Test dataset
    zips = ['19501','18015','18016','18109']

    # first flag to handle tutorial iteration
    first = True
    fullTime = 0    # tracks the full time elapsed (s)
    count = 0       # tracks the number of zip codes processed
    total = len(zips)   # total # of zips to be processed 


    # Loop through zip codes and run scraper  (.iloc[:10] to run only first 10 elements)
    # for x in zips['19501']:
    for x in zips:
        print("Getting data for zip: "+ str(x))
        tic = time.perf_counter()
        getRates(x,first)
        first = False
        fullData = importResults(x,fullData)
        count += 1
        toc = time.perf_counter()
        fullTime += toc-tic
        print("Processed zip: "+x+f" data in {toc - tic:0.4f} seconds   (",count,"/",total,")")

    print("\n--------- Done Scraping ---------\n")
    print(f"Full time elapsed: {fullTime:0.4f} s")
    print(f"Avg. time per zipcode: {fullTime/count:0.4f} s\n")
    # Close our chrome window
    driver.close()
    print("Closing Browser Window....")
    print("Exporting results to csv....")

    # Exporting data to CSV output file:
    filepath = Path('Output-Files/'+date.today().strftime('%Y-%m-%d')+'-GS3.csv')
    fullData.to_csv(filepath)


    print("Exporting done. Process Finished.")
    print("---------------------------------")

    return

def getZips():
    zips = pd.read_csv("ZipCodes.csv")
    zips = zips.astype(str)
    zips = zips.drop_duplicates(subset=['19501'])
    print(len(zips), " zip codes retrieved...")
    return zips

#This function takes the passed in Zipcode and Navigates to Papowerswitch.com and downloads the desired results
def getRates(zipcode, isFirst):

    # Navigate to website using zipcode
    url = 'https://www.papowerswitch.com/shop-for-electricity/shop-for-your-small-business/'
    driver.get(url)
    time.sleep(0.5)

    edit_zip = driver.find_element(By.ID,'edit-zipcode')
    edit_zip.send_keys(zipcode)
    driver.find_element(By.ID,'edit-submit-residential-rate-search2').click()
    #Multi-Distributor home Case
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, "//a[@data-id='27513']").click()
    except NoSuchElementException:
        pass

    # Handles multiple General Service type case
    try:
        driver.find_element(By.XPATH, "//a[@data-id='27516']").click()
    except NoSuchElementException:
        pass

    if(isFirst == True):
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-skipbutton"))).click()
        except:
            pass

    time.sleep(0.5)
    # Download / Export csv results
    try:
        driver.find_element(By.ID,"export-results").click()
    except NoSuchElementException:
        print("Error downloading results for: " + zipcode)
        return


# This function opens the downloaded csv results file, processes the data, 
# adds Date and Zip code, and then appends the new data to our full Dataframe
def importResults(zipcode, fullData):

   
    # This while loop is supposed to wait for the downloaded file to be found until 10 seconds has passed, we assume the file was never downloaded 
    # We need to implement a timer count for the while loop below, If we wait more than X seconds and the file does not exist still, contrinue and return 
    timer_count = 0
    myfile = 'rates.csv'
    while not os.path.exists(myfile):
        time.sleep(1)
        timer_count+=1
        if(timer_count == 10):
            print("No results found for " + zipcode + ". Program will continue...")
            return fullData

    # Read downloaded file and checks if it exists
    if os.path.isfile(myfile):
       data = pd.read_csv(myfile)
    else:
        print("Could not read file: Error: %s file not found" % myfile)
        return

    # Adding the date and zip code column
    data['date'] = date.today().strftime('%Y-%m-%d')
    data['zipcode'] = zipcode

    # Append zip code data to full Dataframe
    fullData = fullData.append(data, ignore_index=True)
    # print(fullData)


    # File operations:
    # If file exists, delete it.
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:
        # If it fails, inform the user.
        print("Error: %s file not found" % myfile)

    # Return our full dataFrame    
    return fullData

main()
