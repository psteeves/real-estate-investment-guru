import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import datetime
from tqdm import tqdm


def get_all_property_urls(browser):
    property_urls = []
    mls_ids = []
    browser.get(
        "https://www.centris.ca/en/multi-family-properties~for-sale?view=Thumbnail"
    )
    time.sleep(5)

    num_pages = browser.find_element_by_xpath('//li[@class="pager-current"]').text
    num_pages = int(num_pages.split("/")[1].replace(",", ""))

    # LOOKUP URLS for each property
    for i in tqdm(range(num_pages)):
        skus = browser.find_elements_by_xpath('//meta[@itemprop="sku"]')

        for sku in skus:
            mls_id = sku.get_attribute("content")
            mls_ids.append(mls_id)

            # Prop URL
            link = browser.find_element_by_xpath(
                "//a[@data-mlsnumber='" + mls_id + "']"
            )
            url_prop_2 = link.get_attribute("href")
            property_urls.append(url_prop_2)

        # go to next page and restart
        try:
            browser.find_element_by_xpath('//li[@class="next"]').click()
        except:
            break
        else:
            time.sleep(1)

    # Close and Quit Browser to delete memory
    browser.close()
    browser.quit()
    return property_urls, mls_ids


def find_carac_title_element_text(soup, search_text, num_elements):
    element = soup.find("div", class_="carac-title", text=search_text)
    if element is not None:
        for _ in range(num_elements):
            element = element.next_element
        text = element.text
    else:
        text = None
    return text


def get_property_info(property_url, mls_id):
    # make a GET request to fetch the raw HTML content
    html_content_property = requests.get(property_url).text

    # parse the html content with BS
    soup = BeautifulSoup(html_content_property, "lxml")

    # Property Type
    property_type = soup.find("h1", itemprop="category").text
    property_type = property_type.replace("\n", "")
    property_type = property_type.replace("\xa0", " ")

    unit_details = soup.find_all("span", attrs={"data-id": "NbUniteFormatted"})
    unit_description = [detail.text for detail in unit_details if "(" in detail.text][0]
    num_units = "".join([c for c in unit_description if c.isdigit()])
    unit_type = "".join([c for c in unit_description if c.isalpha()])

    main_unit_description = [
        detail.text for detail in unit_details if "room" in detail.text
    ]
    if main_unit_description:
        _, num_bedrooms, num_bathrooms = main_unit_description[0].split(",")
        num_bedrooms = int("".join([c for c in num_bedrooms if c.isdigit()]))
        num_bathrooms = int("".join([c for c in num_bathrooms if c.isdigit()]))
    else:
        num_bathrooms = None
        num_bedrooms = None

    claimed_revenue = find_carac_title_element_text(soup, "Potential gross revenue", 4)
    if claimed_revenue is not None:
        claimed_revenue = claimed_revenue.replace("$", "")
        claimed_revenue = claimed_revenue.replace(",", "")
        claimed_revenue = float(claimed_revenue)

    latitude = float(soup.find(id="PropertyLat").string)

    # Longitude
    longitude = float(soup.find(id="PropertyLng").string)

    # Price
    price = float(soup.find("span", id="BuyPrice")["content"])

    # Date
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Full Address
    full_address = soup.find("h2", itemprop="address")
    full_address = full_address.text
    address_parts = full_address.split(",")
    city = address_parts[2]
    neighborhood = [part for part in address_parts if "Neighbourhood" in part]
    if neighborhood:
        neighborhood = neighborhood[0].replace("Neighbourhood", "").strip()
    else:
        if "(" in city:
            neighborhood = city[city.find("(") + 1 : city.find(")")]
        else:
            neighborhood = None
    # Area
    building_area = find_carac_title_element_text(
        soup, "Building area (at ground level)", 4
    )
    if building_area is not None:
        building_area = building_area.replace(" sqft", "")
        building_area = building_area.replace(",", "")
        building_area = float(building_area)

    lot_area = find_carac_title_element_text(soup, "Lot area", 4)
    if lot_area is not None:
        lot_area = lot_area.replace(" sqft", "")
        lot_area = lot_area.replace(",", "")
        lot_area = float(lot_area)

    # Year Built
    year_built = find_carac_title_element_text(soup, "Year built", 4)

    # Additional Features
    extra_features = find_carac_title_element_text(soup, "Additional features", 4)
    parking = find_carac_title_element_text(soup, "Parking", 4)
    pool = find_carac_title_element_text(soup, "Pool", 3)
    description = soup.find("div", itemprop="description")
    if description is not None:
        description = description.text.replace("\r\n", "").strip()

    # Unique ID (Date+MLS)
    unique_id = date + "-" + str(mls_id)[:-2]

    return {
        "price": price,
        "latitude": latitude,
        "longitude": longitude,
        "num_units": num_units,
        "unit_type": unit_type,
        "claimed_revenue": claimed_revenue,
        "full_address": full_address,
        "city": city,
        "neighborhood": neighborhood,
        "year_built": year_built,
        "extra_features": extra_features,
        "num_bathrooms": num_bathrooms,
        "num_bedrooms": num_bedrooms,
        "building_area": building_area,
        "lot_area": lot_area,
        "parking": parking,
        "pool": pool,
        "unique_id": unique_id,
        "property_type": property_type,
        "description": description,
    }


def main():
    browser = webdriver.Chrome("/home/psteeves/project-real-estate/chromedriver")
    property_urls, mls_ids = get_all_property_urls(browser)

    data = []
    errors = []
    for url, mls_id in tqdm(list(zip(property_urls, mls_ids))):
        try:
            data.append(get_property_info(url, mls_id))
        except Exception as e:
            print(url)
            print(e, "\n")
            errors.append(url)

    print(f"Successfully extracted {len(data)} / {len(data) + len(errors)} properties")
    # Enter values in DF
    df_sale_plexes = pd.DataFrame(data)
    df_sale_plexes.to_csv("test.csv", index=False)
    with open("error_log.csv", "w") as f:
        f.write(",\n".join(errors))


if __name__ == "__main__":
    main()
