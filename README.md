# PaRatesScraper
### Scrape for electricity rates in the PPL service region


## Instructions:
Residential service rates: ```python3 RatesScraper.py```  
General Service 3 rates (for small businesses) ```python3 GS3-Scraper.py```

## Approach 

1. Open database or CSV file located in a directory (This serves as our data repository)
2. Enumerate through zip codes in the PPL service region
3. For each Zip code:
4. Navigate to papowerswitch.com
5. Submit a requests for each Zip code 
6. View all results
7. Download csv results file to directory
8. Copy csv results file into a dataframe
9. Append a Zipcode and Date column
10. Append dataframe to data repository
11. Save resulting data as a CSV with the Date as the naming convention

## Contacts:
[Alberto Lamadrid, Ph.D.](https://business.lehigh.edu/directory/alberto-j-lamadrid) ,  Lehigh University, Economics, Associate Professor

[Henry Eaton](hhe223@lehigh.edu), Student, Lehigh University

### References:
[Selenium WebDriver Documentation](https://www.selenium.dev/documentation/webdriver/)

[Link to updated list of zip codes in PPL Electric Region](https://www.pplelectric.com/-/media/PPLElectric/At-Your-Service/Docs/General-Supplier-Reference-Information/PPLServicingArea-Zipcodes.xls)
