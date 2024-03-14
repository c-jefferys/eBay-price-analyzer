from bs4 import BeautifulSoup
import requests
import numpy as np
from sys import argv

LINK = argv[1]  # link of ebay search from command line


def get_prices(link):
    # get source page
    r = requests.get(link)
    # parse r
    soup = BeautifulSoup(r.text, "html.parser")
    # find list items from search results
    results = soup.find('ul', {'class':'srp-results'}).find_all('li', {'class':'s-item'})

    prices = []  # all item prices

    for result in results:
        # convert item price to text
        price_text = result.find("span",{"class":"s-item__price"}).text
        try:
            # format price by removing $ and comma
            price = float(price_text[1:].replace(',',''))
        except ValueError:
            continue  # value is something other than a number (can be for various reasons)
        prices.append(price)
    return prices


def remove_outliers(prices):
    data = np.array(prices)
    # remove values more than 2 std dev away from mean
    return data[abs(data - np.mean(data)) < 2 * np.std(data)]


def get_avg(prices):
    return np.mean(prices)


search_prices = get_prices(LINK)
refined_prices = remove_outliers(search_prices)
avg_price = get_avg(refined_prices)
print(f'Prices: {search_prices}')
print(f'Refined: {refined_prices}')
print(f'Average price: ${round(avg_price, 2)}')
