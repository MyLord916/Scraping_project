import json
import requests
from bs4 import BeautifulSoup


web_url = 'https://home-pizza.com'
projects_data_list = []


def load_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def get_product_pages(url) -> dict:
    soup = load_page(url)

    product_cards = soup.find_all('div', class_='catalog-item-content clearfix')

    products_urls = []
    for product_url in product_cards:
        url = product_url.find('a').get('href')
        products_urls.append(web_url + url)
    return products_urls



def get_product_name(soup) -> str:
    try:
        product_name = soup.select_one('div.catalog-detail-info__title').get_text()
    except AttributeError:
        product_name = 'No product name'
    return product_name

def get_product_filling(soup) -> str:
    try:
        product_filling = soup.select_one('p').get_text()
    except AttributeError:
        product_filling = 'No product filling'
    return product_filling

def get_product_size_weight_price(soup) -> dict:
    try:
        product_size_weight_price = soup.select('li.catalog-detail-info__option-item')
        total_info_prod_size_weight_price = []
        for prod in product_size_weight_price:
            prod_label = prod.select_one('label')
            product_size_wight = prod_label.get_text().strip().split(' / ')
            try:
                product_size = product_size_wight[0].split()[0]
                if prod['data-prices-group'] == '1':
                    product_size += '_cheese'
            except AttributeError:
                product_size = None

            try:
                product_weight = product_size_wight[1].split()[0]
            except AttributeError:
                product_weight = None

            try:
                product_price = prod_label['data-price']
            except AttributeError:
                product_price = None

            total_info_prod_size_weight_price.append({
                product_size: {
                    'weight': {'value': int(product_weight),
                               'unit': 'гр'},
                     'price': {'value': int(product_price),
                               'unit': 'р'}
                     }})
    except AttributeError:
        total_info_prod_size_weight_price = None
    return total_info_prod_size_weight_price

def get_energy_value(soup) -> dict:
    try:
        energy_value_params_bloc = (soup.select_one('div.catalog-detail-info__energy').
                                    select('li.catalog-detail-info__energy-list-item'))
        energy_value_params = {
                'additional_info': {
                    'proteins': None,
                    'fats': None,
                    'carbo': None,
                    'calories': None
                }}
        count = 0
        for el in energy_value_params['additional_info']:
            entity_parm = energy_value_params_bloc[count].get_text().strip().split()[1:]
            energy_value_params['additional_info'][el] = {
                'value': float(entity_parm[0].replace(',', '.')),
                'unit': entity_parm[1]}
            count += 1
    except AttributeError:
        energy_value_params = None
    return energy_value_params

def get_img_url(soup):
    try:
        img_url = web_url + soup.select_one('img.catalog-detail-image__image')['src']
    except AttributeError:
        img_url = None
    return img_url

def parse_page(content) -> dict:
    soup = load_page(content)
    data = []
    data.append({'product_name': get_product_name(soup), 'ingredients': get_product_filling(soup)})
    data.append(get_product_size_weight_price(soup))
    data.append(get_energy_value(soup))
    return data

def save_data_to_json(data: list):
    with open("projects_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    product_pages = get_product_pages(web_url + '/type1/')
    for product_page in product_pages[:1]:
        projects_data_list.append(parse_page(product_page))
    save_data_to_json(projects_data_list)


if __name__ == '__main__':
    main()