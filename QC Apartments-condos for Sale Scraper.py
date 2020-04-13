import requests
import math
import re
import itertools
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import seaborn as sns
import datetime
import openpyxl
sns.set()

# Setup lists to prep for DataFrame ------------------------------------------#
Price=[]
URLs=[]
URL_2=[]
Full_Address=[]
Civic_no=[]
Street=[]
Apt=[]
Neighborhood=[]
Region=[]
Property_Area=[]
Lot_Area =[]
Bedrooms=[]
Bathrooms=[]
Year=[]
Date=[]
MLS=[]
MLS_2=[]
Rent_SQFT=[]
Latitude =[]
Longitude =[]
ExtraFeatures =[]
Property_Type =[]
NumberOfUnits =[]
TypeOfUnits =[]
Claimed_Revenue =[]
Description =[]
Parking =[]
Pool =[]
UNIQUE_ID_list =[]



# Crawler: Open page and go to first property-------------------------#

#chrome_options = Options()
#chrome_options.add_argument("--headless")

#browser = webdriver.Chrome('C:/Users/nemanja.zarkovic/PycharmProjects/Env/chromedriver.exe', options=chrome_options)  # Optional argument, if not specified will search path.

browser = webdriver.Chrome('C:/Users/nemanja.zarkovic/PycharmProjects/Env/chromedriver.exe')  # Optional argument, if not specified will search path.
browser.get('https://www.centris.ca/en/condos~for-sale?uc=1&view=Thumbnail')
time.sleep(2)


# get into first property page
#browser.find_element_by_xpath('//div[@class="thumbnail property-thumbnail"]').click()
#time.sleep(1)

#Loop Length

no_galpages_total = browser.find_element_by_xpath('//li[@class="pager-current"]').text
no_galpages_total = no_galpages_total.split("/")[1]
no_galpages_total = no_galpages_total.replace(",","")
no_galpages_total = int(no_galpages_total)
no_galpages_total


# LOOKUP URLS for each property
for page in range(0,no_galpages_total):

    # FIND THE NUMBER OF PROPERTIES SHOWED IN GALLERY PAGE
    PropPerGallery = len(browser.find_elements_by_xpath('//div[@data-id="templateThumbnailItem"]'))

    for i in range(0, PropPerGallery):
        # SKU - MLS id
        try:
            sku = browser.find_elements_by_xpath('//meta[@itemprop="sku"]')[i]
            mls_id_2 = sku.get_attribute('content')
            MLS_2.append(mls_id_2)
            print(mls_id_2)
        except:
            browser.refresh()
            time.sleep(10)
            try:
                sku = browser.find_elements_by_xpath('//meta[@itemprop="sku"]')[i]
                mls_id_2 = sku.get_attribute('content')
                MLS_2.append(mls_id_2)
                print(mls_id_2)
            except:
                mls_id_2 = float("nan")
                MLS_2.append(mls_id_2)


        # Prop URL
        try:
            link = browser.find_element_by_xpath("//a[@data-mlsnumber='" + mls_id_2 + "']")
            url_prop_2 = link.get_attribute('href')
            URL_2.append(url_prop_2)
            print(url_prop_2)
        except:
            browser.refresh()
            time.sleep(10)
            try:
                link = browser.find_element_by_xpath("//a[@data-mlsnumber='" + mls_id_2 + "']")
                url_prop_2 = link.get_attribute('href')
                URL_2.append(url_prop_2)
                print(url_prop_2)
            except:
                pass


    # Status completion %
    print(round((page/no_galpages_total),3),"%")


    # go to next page and restart
    try:
        browser.find_element_by_xpath('//li[@class="next"]').click()
        time.sleep(1)

    except:
        print("Break")
        break

# Close and Quit Browser to delete memory
browser.close()
browser.quit()

# Get data from each property via URLS
        #loop_divider = 4
        #loop_save = int(round(no_galpages_total/loop_divider,0))

n_pages = 0

for i in range(0,len(URL_2)):
    n_pages += 1

    # parse property page HTML with Beautiful Soup
    URL_Prop = URL_2[i]
    URLs.append(URL_Prop)
    print(URL_Prop)

    # make a Get request to fetch the raw HTML content
    html_content_property = requests.get(URL_Prop).text

    # parse the html content with BS
    soup = BeautifulSoup(html_content_property, "lxml")

    # MLS ID
    mls_id = MLS_2[i]
    MLS.append(mls_id)
    print(mls_id)

    # Unique ID (Date+MLS)
    unique_ID = str(date_prop) + "-" + str(mls_id)
    UNIQUE_ID_list.append(unique_ID)
    print(unique_ID)

    # Property Type
    prop_type = soup.find('h1', itemprop="category").text
    prop_type = prop_type.replace("\n","")
    prop_type = prop_type.replace("\xa0"," ")
    Property_Type.append(prop_type)
    print(prop_type)

    # Number of Units and type of units (for Plexes)
    try:
        units_details = soup.find_all('span', attrs={"data-id":"NbUniteFormatted"})
        units_number = units_details[0].text
        unit_type = units_details[1].text
        NumberOfUnits.append(units_number)
        TypeOfUnits.append(unit_type)
    except:
        units_number = float("nan")
        unit_type = float("nan")
        NumberOfUnits.append(units_number)
        TypeOfUnits.append(unit_type)


    # Claimed Potential Gross Revenue (for plexes)
    try:
        claimed_rev = soup.find('div',class_="carac-title", text="Potential gross revenue")
        claimed_rev = claimed_rev.next_element
        claimed_rev = claimed_rev.next_element
        claimed_rev = claimed_rev.next_element
        claimed_rev = claimed_rev.next_element
        claimed_rev = claimed_rev.text
        claimed_rev = claimed_rev.replace("$","")
        claimed_rev = claimed_rev.replace(",","")
        Claimed_Revenue.append(claimed_rev)
    except:
        claimed_rev = float("nan")
        Claimed_Revenue.append(claimed_rev)


    # Latitude
    try:
        Latitude_prop = soup.find(id='PropertyLat')
        Latitude_prop = Latitude_prop.string
        Latitude.append(Latitude_prop)
        print(Latitude_prop)
    except:
        Latitude_prop = float("nan")
        Latitude.append(Latitude_prop)

    # Longitude
    try:
        Longitude_prop = soup.find(id="PropertyLng")
        Longitude_prop = Longitude_prop.string
        Longitude.append(Longitude_prop)
        print(Longitude_prop)
    except:
        Longitude_prop = float("nan")
        Longitude.append(Longitude_prop)

    # Price
    try:
        prop_price = soup.find('span', id='BuyPrice')
        prop_price = prop_price["content"]
        prop_price = float(prop_price)
        Price.append(prop_price)
        print(prop_price)
    except:
        prop_price = float("nan")
        Rent.append(prop_price)

    # Date
    if math.isnan(prop_price) == True:
        print("no date")
        pass
    else:
        date_prop = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        print(date_prop)
        Date.append(date_prop)

    # Full Address
    try:
        prop_address = soup.find('h2', itemprop="address")
        prop_address = prop_address.text
        Full_Address.append(prop_address)
        print(prop_address)
    except:
        prop_address = float("nan")
        Full_Address.append(prop_address)

    # Civic No
    try:
        civic_no = prop_address.split(",", )[0]
        Civic_no.append(civic_no)
    except:
        civic_no = float("nan")
        Civic_no.append(civic_no)

    # Street Name
    try:
        Street_name = prop_address.split(",", )[1]
        Street.append(Street_name)
    except:
        Street_name = float("nan")
        Street.append(Street_name)

    # Apartment
    try:
        Apt_no = prop_address.split(",", )[2]
        Apt.append(Apt_no)
    except:
        Apt_no = float("nan")
        Apt.append(Apt_no)

    # Neighborhood
    try:
        hood = prop_address.split(",", )[-1]
        hood = hood.replace(" Neighbourhood","")
        Neighborhood.append(hood)
    except:
        hood = float("nan")
        Neighborhood.append(hood)

    # Region
    try:
        if math.isnan(prop_address) == True:
            adr_elements = float("nan")
        else:
            pass
    except:
        adr_elements = prop_address.count(",") + 1
        adr_elements = float(adr_elements)

    try:
        if math.isnan(adr_elements) == True:
            prop_region = float("nan")
            Region.append(prop_region)

        else:
            if adr_elements == 5:
                prop_region = prop_address.split(",", )[3]
                prop_region = prop_region.replace(" Neighbourhood","")
                Region.append(prop_region)
            else:
                prop_region = prop_address.split(",", )[-1]
                prop_region = prop_region.replace(" Neighbourhood","")
                Region.append(prop_region)
    except:
        prop_region = float("nan")
        Region.append(prop_region)

    # Year Built
    try:
        prop_year = soup.find('div',class_="carac-title", text='Year built')
        prop_year = prop_year.next_element
        prop_year = prop_year.next_element
        prop_year = prop_year.next_element
        prop_year = prop_year.next_element
        prop_year = prop_year.text
        Year.append(prop_year)
        print(prop_year)
    except:
        prop_year = float("nan")
        Year.append(prop_year)

    # Additional Features
    try:
        add_features = soup.find('div',class_="carac-title", text="Additional features")
        add_features = add_features.next_element
        add_features = add_features.next_element
        add_features = add_features.next_element
        add_features = add_features.next_element
        add_features = add_features.text
        ExtraFeatures.append(add_features)
    except:
        add_features = float("nan")
        ExtraFeatures.append(add_features)

    # Bathrooms
    try:
        baths = soup.find('div', text=re.compile('bathroom')).text
        baths = baths.replace("\r","")
        baths = baths.replace("\n","")
        baths = baths.replace(" ","")
        baths = baths[0]
        Bathrooms.append(baths)
        print(baths)
    except:
        baths = float("nan")
        Bathrooms.append(baths)

    # Bedrooms
    try:
        beds = soup.find('div', text=re.compile('bedroom')).text
        beds = beds.replace("\r", "")
        beds = beds.replace("\n", "")
        beds = beds.replace(" ", "")
        beds = beds[0]
        Bedrooms.append(beds)
        print(beds)
    except:
        beds = float("nan")
        Bedrooms.append(beds)

    # Property Area
    try:
        prop_Area = soup.find('div',class_="carac-title", text="Net area")
        prop_Area = prop_Area.next_element
        prop_Area = prop_Area.next_element
        prop_Area = prop_Area.next_element
        prop_Area = prop_Area.next_element
        prop_Area = prop_Area.text
        prop_Area = prop_Area.replace(" sqft","")
        prop_Area = prop_Area.replace(",","")
        prop_Area = int(prop_Area)
        Property_Area.append(prop_Area)
    except:
        try:
            prop_Area = soup.find('div',class_="carac-title", text="Gross area")
            prop_Area = prop_Area.next_element
            prop_Area = prop_Area.next_element
            prop_Area = prop_Area.next_element
            prop_Area = prop_Area.next_element
            prop_Area = prop_Area.text
            prop_Area = prop_Area.replace(" sqft", "")
            prop_Area = prop_Area.replace(",", "")
            prop_Area = int(prop_Area)
            Property_Area.append(prop_Area)
        except:
            prop_Area = float("nan")
            Property_Area.append(prop_Area)

    # Lot Area
    try:
        lot_area = soup.find('div',class_="carac-title", text="Lot area")
        lot_area = lot_area.next_element
        lot_area = lot_area.next_element
        lot_area = lot_area.next_element
        lot_area = lot_area.next_element
        lot_area = lot_area.text
        lot_area = lot_area.replace(" sqft","")
        lot_area = lot_area.replace(",","")
        Lot_Area.append(lot_area)
    except:
        lot_area = float("nan")
        Lot_Area.append(lot_area)

    # Parking
    try:
        prop_parking = soup.find('div', class_="carac-title", text=re.compile('Parking'))
        prop_parking = prop_parking.next_element
        prop_parking = prop_parking.next_element
        prop_parking = prop_parking.next_element
        prop_parking = prop_parking.next_element
        prop_parking = prop_parking.text
        Parking.append(prop_parking)
    except:
        prop_parking = float("nan")
        Parking.append(prop_parking)

    # Pool
    try:
        prop_pool = soup.find('div', class_="carac-title", text=re.compile('Pool'))
        prop_pool = prop_pool.next_element
        prop_pool = prop_pool.next_element
        prop_pool = prop_pool.next_element
        prop_pool = prop_pool.text
        Pool.append(prop_pool)
    except:
        prop_pool = float("nan")
        Pool.append(prop_pool)

    # Description
    try:
        desc = soup.find('div', itemprop='description').text
        desc = desc.replace("\r\n","")
        desc = desc.lstrip()
        Description.append(desc)
    except:
        desc = float("nan")
        Description.append(desc)

    # Status completion %
    print(round(i / len(URL_2),2),"%")


   # Enter values in DF
   df_sale = pd.DataFrame(
       {"Date": Date, "URLs": URLs, "MLS ID": MLS,"Unique_ID":UNIQUE_ID_list,"Property_Type": Property_Type, "Number_of_Units(for plexes)":NumberOfUnits, "Type_of_Units(Plexes)":TypeOfUnits ,"Latitude": Latitude,"Longitude": Longitude, "Full_Address": Full_Address,"Civic_No":Civic_no, "Street": Street, "Apt": Apt,
        "Neighborhood": Neighborhood, "Region": Region, "Year": Year,"Parking":Parking,"Pool":Pool, "Extra_Features": ExtraFeatures, "Property_Area(sqft)": Property_Area,"Lot_Area(sqft)":Lot_Area, "Bathrooms": Bathrooms,"Bedrooms": Bedrooms,"Price": Price,"Claimed_Potential_Revenue":Claimed_Revenue, "Description":Description})




# Setup to Export Df to Excel
# name files and tabs
sheet_name_today = "prop_sale " + str(datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S"))
sheet_name_recent = "RECENT_prop_sale"
out_path_hist = "C:/Users/nemanja.zarkovic/PycharmProjects/Env/Project_RE_App/Databases/All for Sale/AllForSale_Hist_Data.xlsx"
out_path_mostrecent = "C:/Users/nemanja.zarkovic/PycharmProjects/Env/Project_RE_App/Databases/All for Sale/AllForSale_Most_Recent_Data.xlsx"

# Add current DF to Historical Data base as NEW sheet
writer_master_hist = pd.ExcelWriter(out_path_hist, engine="openpyxl")
workbook_master = openpyxl.load_workbook(out_path_hist)
writer_master_hist.book = workbook_master
df_sale.to_excel(writer_master_hist, sheet_name=sheet_name_today, index=None)
writer_master_hist.save()
writer_master_hist.close()

# write this recent df in different Excel Doc named "Most Recent Condos"
df_sale.to_excel(out_path_mostrecent, sheet_name=sheet_name_today)
