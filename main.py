import json
import requests
from bs4 import BeautifulSoup


web_url = 'https://home-pizza.com/'
projects_data_list = []


def load_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def get_product_pages(url):
    soup = load_page(url)

    product_cards = soup.find_all('div', class_='catalog-item-content clearfix')

    products_urls = []
    for product_url in product_cards:
        url = product_url.find('a').get('href')
        products_urls.append(web_url + url)
    return products_urls


def parse_page(content):
    soup = load_page(content)

    try:
        product_name = soup.find('div', class_='catalog-detail-info__title').text
    except AttributeError:
        product_name = 'No product name'

    try:
        product_filling = soup.find('p').text
    except AttributeError:
        product_filling = 'No product filling'

    try:
        product_size_weight_price = (
            soup.find_all('div', class_='catalog-detail-info__option-inner').
            find('li', class_='catalog-detail-info__option-item').
            find('label', class_='catalog-detail-info__option-item-text')
        )
        for prod in product_size_weight_price:
            product_size = prod.text.split('/')[0].strip()
            product_weight = prod.text.split('/')[1].replace('г', 'гр').strip()
            product_price = prod.get('data-price') + 'р'
            print(product_size, product_weight, product_price)
    except AttributeError:
        product_filling = 'No product prise'

    try:
        product_name = soup.find('div', class_='catalog-detail-info__title').text
    except AttributeError:
        product_name = 'No product name'

    try:
        product_filling = soup.find('p').text
    except AttributeError:
        product_filling = 'No product filling'

    try:
        product_size_weight_price = (
            soup.find('div', class_='catalog-detail-info__option-inner').
            find_all('li', class_='catalog-detail-info__option-item')
        )
        total_info_prod_size_weight_price = []
        el = 0
        for prod in product_size_weight_price:
            try:
                product_size = (prod.find('label', class_='catalog-detail-info__option-item-text').
                                text.split('/')[0].strip()).split()[0]
            except AttributeError:
                product_size = None

            try:
                product_weight = (prod.find('label', class_='catalog-detail-info__option-item-text').
                                  text.split('/')[1].strip().replace('г', 'гр')).split()
            except AttributeError:
                product_weight = None

            try:
                product_price = (prod.find('label', class_='catalog-detail-info__option-item-text').get(
                    'data-price') + ' р').split()
            except AttributeError:
                product_price = None
            total_info_prod_size_weight_price.append([product_size, product_weight, product_price])
            if prod.get('data-prices-group') == '1':
                total_info_prod_size_weight_price[el][0] = '30_cheese'
            el += 1

    except AttributeError:
        print('product size weight price not find')

    try:
        energy_value_bloc = soup.find('catalog-detail-info__energy')
        energy_value_params_bloc = (
            soup.find('div', class_='catalog-detail-info__energy').
            find_all('li', class_='catalog-detail-info__energy-list-item')
        )
        energy_value_params = []
        for parm in energy_value_params_bloc:
            energy_value_params.append(parm.text.strip().split()[1:])
    except AttributeError:
        print('energy value bloc not find')

    try:
        url_img = (
                web_url[:-1] +
                soup.find('div', class_='catalog-detail').find('img').get('src')
        )
    except AttributeError:
        url_img = 'img not find'

    projects_data_list.append({
        'product_name': product_name,
        'ingredients': product_filling,
    })
    for i in range(len(total_info_prod_size_weight_price)):
        projects_data_list.append({
            total_info_prod_size_weight_price[i][0]: {
                'weight': {'value': total_info_prod_size_weight_price[i][1][0],
                           'unit': total_info_prod_size_weight_price[i][1][1]},
                'price': {'value': total_info_prod_size_weight_price[i][2][0],
                          'unit': total_info_prod_size_weight_price[i][2][1]}
            }})
    projects_data_list.append({
        'additional_info': {
            'proteins': {'value': energy_value_params[0][0], 'unit': energy_value_params[0][1]},
            'fats': {'value': energy_value_params[1][0], 'unit': energy_value_params[1][1]},
            'carbo': {'value': energy_value_params[2][0], 'unit': energy_value_params[2][1]},
            'calories': {'value': energy_value_params[3][0], 'unit': energy_value_params[3][1]}
        },
        'img_souce': url_img
    })


def save_data_to_json(data: list):
    with open("projects_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    product_pages = get_product_pages(web_url + 'type1/')
    for product_page in product_pages[:-3]:
        parse_page(product_page)
    save_data_to_json(projects_data_list)


if __name__ == '__main__':
    main()
