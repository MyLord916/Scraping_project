import requests
from bs4 import BeautifulSoup

url = 'https://home-pizza.com//product/258/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

product_name = soup.select_one('div.catalog-detail-info__title').get_text()

product_filling = soup.select_one('p').get_text()

product_size_weight_price = soup.select('li.catalog-detail-info__option-item')

total_info_prod_size_weight_price = []
for prod in product_size_weight_price:
    prod_label = prod.select_one('label')
    product_size_wight = prod_label.get_text().strip().split(' / ')
    product_size = product_size_wight[0].split()[0]
    if prod['data-prices-group'] == '1':
        product_size += '_cheese'
    product_wight = product_size_wight[1].split()[0] + 'g'
    product_price = prod_label['data-price'] + 'r'
    total_info_prod_size_weight_price.append([product_size, product_wight, product_price])

energy_value_params_bloc = soup.select_one('div.catalog-detail-info__energy').select('li.catalog-detail-info__energy-list-item')
additional_info = []
for el in energy_value_params_bloc:
    energy_info = el.get_text().strip().split()[1:]
    print(energy_info)
    additional_info.append(
        {el.select_one('span')['data-energy-key']: {'value': energy_info[0], 'unit': energy_info[1]}}
    )
img_url = 'https://home-pizza.com' + soup.select_one('img.catalog-detail-image__image')['src']

print(product_name)
print(product_filling)
print(total_info_prod_size_weight_price)
print(additional_info)
print(img_url)

