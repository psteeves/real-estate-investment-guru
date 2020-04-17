import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re
import datetime
from tqdm import tqdm


def get_all_property_urls(browser):
    property_urls = []
    mls_ids = []
    browser.get(
        "https://www.centris.ca/en/properties~for-rent?uc=2&view=Thumbnail"
    )
    time.sleep(7)

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
            time.sleep(2)

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

    if "sale" in property_type:
        raise ValueError("Property is for sale. We are concerned with properties to rent.")
    else:
        property_type = property_type.replace("for rent", "").strip()

    num_bedrooms = soup.find('div', text=re.compile('bedroom')).text
    num_bedrooms = int("".join([c for c in num_bedrooms if c.isdigit()]))
    num_bathrooms = soup.find('div', text=re.compile('bathroom')).text
    num_bathrooms = int("".join([c for c in num_bathrooms if c.isdigit()]))

    # Date
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Full Address
    full_address = soup.find("h2", itemprop="address")
    full_address = full_address.text
    address_parts = full_address.split(",")
    city = address_parts[2]
    if "apt" in city:
        city = address_parts[3]
    neighborhood = [part for part in address_parts if "Neighbourhood" in part]
    if neighborhood:
        neighborhood = neighborhood[0].replace("Neighbourhood", "").strip()
    else:
        if "(" in city:
            neighborhood = city[city.find("(") + 1 : city.find(")")]
        else:
            neighborhood = None
    # Area
    area = find_carac_title_element_text(
        soup, "Gross area", 4
    )
    if area is None:
        area = find_carac_title_element_text(
            soup, "Net area", 4
        )
    if area is not None:
        area = area.replace(" sqft", "")
        area = area.replace(",", "")
        area = float(area)

    # Year Built
    year_built = find_carac_title_element_text(soup, "Year built", 4)
    if year_built is not None:
        year_built = "".join([c for c in year_built if c.isdigit()])
        if not year_built:
            # Empty year means it's something like "under construction"
            year_built = 2020
        else:
            year_built = int(year_built)

    # Additional Features
    extra_features = find_carac_title_element_text(soup, "Additional features", 4)
    description = soup.find("div", itemprop="description")
    if description is not None:
        description = description.text.replace("\r\n", "").strip()

    rent = soup.find('span', id='BuyPrice')
    rent = rent["content"]
    rent = float(rent)

    # Unique ID (Date+MLS)
    unique_id = date + "-" + str(mls_id)

    return {
        "rent": rent,
        "full_address": full_address,
        "city": city,
        "neighborhood": neighborhood,
        "year_built": year_built,
        "extra_features": extra_features,
        "num_bathrooms": num_bathrooms,
        "num_bedrooms": num_bedrooms,
        "area": area,
        "unique_id": unique_id,
        "property_type": property_type,
        "description": description,
        "url": property_url,
        "mls_id": mls_id
    }


def main():
    browser = webdriver.Chrome("./chromedriver")
    property_urls, mls_ids = get_all_property_urls(browser)
    data = []
    errors = []
    for url, mls_id in tqdm(list(zip(property_urls, mls_ids))):
        try:
            info = get_property_info(url, mls_id)
        except Exception as e:
            print(url)
            print(e, "\n")
            errors.append(url)
        else:
            data.append(info)

    print(f"Successfully extracted {len(data)} / {len(data) + len(errors)} properties")
    # Enter values in DF
    df_sale_plexes = pd.DataFrame(data)
    df_sale_plexes.to_csv("rent.csv", index=False)
    with open("error_log.csv", "w") as f:
        f.write(",\n".join(errors))


if __name__ == "__main__":
    main()
