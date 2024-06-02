import os
import shutil
import json
import time
import random
import requests
from bs4 import BeautifulSoup


def get_data(url):
    cookies = {
        'csrftoken': 'bdsDAP8uOnXUQqmFWnBLBFpy6QLYx7ocXK2NSoPoyybP4TZCpjspDCmQ9NRh23Jg',
        'sessionid': '8iwo68kpbqsdje4c2itugzxokg2xe7do',
        'clientinfo': '1440:900:1',
        'tmr_lvid': '00470fd2404bfc4aaff95d52702c2064',
        'tmr_lvidTS': '1716304688055',
        '_ym_uid': '1716304688188119596',
        '_ym_d': '1716304688',
        '_ga': 'GA1.2.653363696.1716304689',
        'site-version': 'desktop',
        'cookies-notice': 'close',
        '_ym_isad': '2',
        '_gid': 'GA1.2.1376756221.1717295761',
        '_gat': '1',
        '_ym_visorc': 'w',
        'domain_sid': 'QQ_0sZh_mmeJEBx7NdGgv%3A1717295763033',
        '_ga_3DNPT3SKF2': 'GS1.2.1717295763.5.1.1717295771.52.0.0',
        'tmr_detect': '0%7C1717295773927',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'csrftoken=bdsDAP8uOnXUQqmFWnBLBFpy6QLYx7ocXK2NSoPoyybP4TZCpjspDCmQ9NRh23Jg; sessionid=8iwo68kpbqsdje4c2itugzxokg2xe7do; clientinfo=1440:900:1; tmr_lvid=00470fd2404bfc4aaff95d52702c2064; tmr_lvidTS=1716304688055; _ym_uid=1716304688188119596; _ym_d=1716304688; _ga=GA1.2.653363696.1716304689; site-version=desktop; cookies-notice=close; _ym_isad=2; _gid=GA1.2.1376756221.1717295761; _gat=1; _ym_visorc=w; domain_sid=QQ_0sZh_mmeJEBx7NdGgv%3A1717295763033; _ga_3DNPT3SKF2=GS1.2.1717295763.5.1.1717295771.52.0.0; tmr_detect=0%7C1717295773927',
        'priority': 'u=0, i',
        'referer': 'https://home-pizza.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    with open('index.html', 'w') as file:
        file.write(response.text)

    with open("index.html") as file:
          src = file.read()

    data_soup = BeautifulSoup(src, 'lxml')

    product_cards = data_soup.find_all('div', class_='catalog-item-content clearfix')

    products_urls = []
    for product_url in product_cards:
        url = product_url.find('a').get('href')
        products_urls.append('https://home-pizza.com/' + url)

    projects_data_list = []

    os.remove('index.html')
    os.mkdir('src')

    for url in products_urls:
        req = requests.get(url, headers=headers, cookies=cookies)
        fail_name = url.split('/')[-2]

        with open(f'src/{fail_name}.html', 'w') as file:
            file.write(req.text)
        print('Processed in item:' + fail_name)
        time.sleep(random.randrange(3, 5))

        with open(f'src/{fail_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            product_name = soup.find('div', class_='catalog-detail-info__title').text
        except Exception:
            product_name = 'No product name'

        try:
            product_filling = soup.find('p').text
        except Exception:
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
        except Exception:
            product_filling = 'No product prise'

        try:
            product_name = soup.find('div', class_='catalog-detail-info__title').text
        except Exception:
            product_name = 'No product name'

        try:
            product_filling = soup.find('p').text
        except Exception:
            product_filling = 'No product filling'

        try:
            product_size_weight_price = (
                soup.find('div', class_='catalog-detail-info__option-inner').
                find_all('li', class_='catalog-detail-info__option-item')
            )
            total_info_prod_size_weight_price = []
            iter = 0
            for prod in product_size_weight_price:
                try:
                    product_size = (prod.find('label', class_='catalog-detail-info__option-item-text').
                                    text.split('/')[0].strip())
                except Exception:
                    product_size = None

                try:
                    product_weight = (prod.find('label', class_='catalog-detail-info__option-item-text').
                                      text.split('/')[1].strip().replace('г', 'гр'))
                except Exception:
                    product_weight = None

                try:
                    product_price = prod.find('label', class_='catalog-detail-info__option-item-text').get(
                        'data-price') + 'р'
                except Exception:
                    product_price = None
                total_info_prod_size_weight_price.append([product_size, product_weight, product_price])
                if prod.get('data-prices-group') == '1':
                    total_info_prod_size_weight_price[iter][0] = '30 см | Сырный борт'
                iter += 1

        except Exception:
            print('product size weight price not find')

        try:
            energy_value_bloc = soup.find('catalog-detail-info__energy')
            energy_value_parms_bloc = (
                soup.find('div', class_='catalog-detail-info__energy').
                find_all('li', class_='catalog-detail-info__energy-list-item')
            )
            energy_value_parms = []
            for parm in energy_value_parms_bloc:
                energy_value_parms.append(' '.join(parm.text.strip().split()[1:]))
        except Exception:
            print('energy value bloc not find')

        try:
            url_img = (
                    'https://home-pizza.com/' +
                    soup.find('div', class_='catalog-detail').find('img').get('src')
            )
        except Exception:
            url_img = 'img not find'

        while len(total_info_prod_size_weight_price) < 4:
            total_info_prod_size_weight_price.append([None, None, None])

        projects_data_list.append({
            'Название пиццы': product_name,
            'Наполнение': product_filling,
            total_info_prod_size_weight_price[0][0]: {
                'Вес': total_info_prod_size_weight_price[0][1],
                'Цена': total_info_prod_size_weight_price[0][2],
            },
            total_info_prod_size_weight_price[1][0]: {
                'Вес': total_info_prod_size_weight_price[1][1],
                'Цена': total_info_prod_size_weight_price[1][2],
            },
            total_info_prod_size_weight_price[2][0]: {
                'Вес': total_info_prod_size_weight_price[2][1],
                'Цена': total_info_prod_size_weight_price[2][2],
            },
            total_info_prod_size_weight_price[3][0]: {
                'Вес': total_info_prod_size_weight_price[3][1],
                'Цена': total_info_prod_size_weight_price[3][2],
            },
            'Энергетическая ценность в 100 граммах': {
                'Белки': energy_value_parms[0],
                'Жиры': energy_value_parms[1],
                'Углеводы': energy_value_parms[2],
                'Калории': energy_value_parms[3]
            },
            'Ссылка на изображене': url_img
        })
        with open("projects_data.json", "a", encoding="utf-8") as file:
            json.dump(projects_data_list, file, indent=4, ensure_ascii=False)





def main():
    get_data('https://home-pizza.com/type1/')

if __name__=='__main__':
    main()
    shutil.rmtree('src')