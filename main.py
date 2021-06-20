from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time


FORMLINK = 'https://docs.google.com/forms/d/e/1FAIpQLSebudGjSlTEP2R3Gdp739ISV88nq5hG1uuqTb4O7TZKGscJ7w/viewform?usp=sf_link'
ZILLOWLISTINGS = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'




# TODO: Use BeautifulSoup/Requests to scrape all the listings from the Zillow web address
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

response = requests.get(ZILLOWLISTINGS, headers=req_headers)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)



# TODO: Create a list of links for all the listings you scraped. e.g.
# Example Link
# <a href="https://www.zillow.com/homedetails/345-Green-St-APT-3-San-Francisco-CA-94133/2112230369_zpid/" class="list-card-link list-card-link-top-margin" tabindex="0"><address class="list-card-addr">345 Green St APT 3, San Francisco, CA 94133</address></a>

address_links = soup.find_all('a', class_="list-card-link")
address_link_list = [address['href'] for address in address_links]


# TODO: clean address links removing anything not https
temporary_address_link_list = []
for link in address_link_list:
    if 'https' in link:
        clean_link = link
    temporary_address_link_list.append(clean_link)

final_address_link_list = []
loop_count = 0
for link in temporary_address_link_list:
    if loop_count%2 ==0:
        final_link = link
        final_address_link_list.append(final_link)
    loop_count+=1
print(final_address_link_list)

'''Check number of links returned against prices and addresses'''
count_links = 0
for link in final_address_link_list:
    count_links+=1
print(count_links)




# TODO: Create a list of prices for all the listings you scraped. e.g.
# Example Price
# <div class="list-card-price">$2,995/mo</div>
address_prices = soup.find_all(class_="list-card-price")
price_list = [price.text for price in address_prices]
print(price_list)
# TODO: clean up list values to return numbers only
price_list_numbers = []
for price in price_list:
    no_comma = price.replace(',','')
    new_price = re.findall(r'\d+',no_comma)
    final_price = int(new_price[0])
    price_list_numbers.append(final_price)
print(price_list_numbers)


'''Check number of prices returned against links and addresses'''
count_prices = 0
for price in price_list_numbers:
    count_prices +=1
print(count_prices)



# TODO: Create a list of addresses for all the listings you scraped. e.g.
# Example address
# <address class="list-card-addr">345 Green St APT 3, San Francisco, CA 94133</address>
addresses = soup.find_all(class_="list-card-addr")
address_list = [address.text for address in addresses]
print(address_list)

'''Check number of addresses returned against links and prices'''
count_addresses = 0
for address in address_list:
    count_addresses +=1
print(count_addresses)

# TODO: Create a dictionary of the three inputs to make form data inputs easier

# zillow_dictionary = {}
# for i in range(len(address_list)):
#     zillow_dictionary[i] = {
#         'link': final_address_link_list[i],
#         'price': price_list_numbers[i],
#         'address': address_list[i],
#     }
# print(zillow_dictionary)

# TODO: Use Selenium to fill in the form you created (step 1,2,3 above). Each listing should have its price/address/link added to the form. You will need to fill in a new form for each new listing. e.g.
chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(FORMLINK)

address_x_path = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
price_x_path = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
link_x_path = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

for i in range(len(address_list)):
    print(address_list[i])
    time.sleep(2)
    address_entry = driver.find_element_by_xpath(address_x_path)
    address_entry.send_keys(address_list[i])
    price_entry = driver.find_element_by_xpath(price_x_path)
    price_entry.send_keys(price_list_numbers[i])
    link_entry = driver.find_element_by_xpath(link_x_path)
    link_entry.send_keys(final_address_link_list[i])

    time.sleep(2)
    submit_button_click = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit_button_click.click()
    time.sleep(2)

    submitanother = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submitanother.click()
    time.sleep(2)

driver.close()

# TODO: After all data entered manually click 'Sheet' icon to create a Google Sheet from the responses to the Google Form

