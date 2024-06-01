import json
import time
import random
import requests
from bs4 import BeautifulSoup


def get_data(url):
    cookies = {
        'csrftoken': 'WlTWPSGCerzWM2QNQOJlHzX7I686MsXfwDbmsyRXIauwHiayCRDdETRO2TeRNz2i',
        'sessionid': 'mbmm5ultvfr8oendho6u5u4q7e942mhh',
        'clientinfo': '1440:900:1',
        'site-version': 'desktop',
        '_ym_uid': '1716920592357400667',
        '_ym_d': '1716920592',
        'tmr_lvid': '5fa1953690173a6f91f88da9b4c3b558',
        'tmr_lvidTS': '1716920591778',
        'domain_sid': '1EcSswu28EdTYnqUDfVs3%3A1716920592307',
        '_ga': 'GA1.2.1243218862.1716920592',
        '_gid': 'GA1.2.869263453.1716920592',
        'cookies-notice': 'close',
        '_ym_isad': '2',
        '_gat': '1',
        '_ym_visorc': 'w',
        'tmr_detect': '0%7C1717003453416',
        '_ga_3DNPT3SKF2': 'GS1.2.1717003451.2.1.1717003464.47.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9',
        # 'cookie': 'csrftoken=WlTWPSGCerzWM2QNQOJlHzX7I686MsXfwDbmsyRXIauwHiayCRDdETRO2TeRNz2i; sessionid=mbmm5ultvfr8oendho6u5u4q7e942mhh; clientinfo=1440:900:1; site-version=desktop; _ym_uid=1716920592357400667; _ym_d=1716920592; tmr_lvid=5fa1953690173a6f91f88da9b4c3b558; tmr_lvidTS=1716920591778; domain_sid=1EcSswu28EdTYnqUDfVs3%3A1716920592307; _ga=GA1.2.1243218862.1716920592; _gid=GA1.2.869263453.1716920592; cookies-notice=close; _ym_isad=2; _gat=1; _ym_visorc=w; tmr_detect=0%7C1717003453416; _ga_3DNPT3SKF2=GS1.2.1717003451.2.1.1717003464.47.0.0',
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

    # response = requests.get(url, cookies=cookies, headers=headers)

    with open("index.html") as file:
          src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    product_cards = soup.find_all('div', class_='catalog-item-content clearfix')

    products_urls = []
    for product_url in product_cards:
        url = product_url.find('a').get('href')
        products_urls.append('https://home-pizza.com/'+ url)

    projects_data_list = []
    count = 0

    for url in products_urls:
        req = requests.get(url, headers=headers, cookies=cookies)
        fail_name = url.split('/')[-2]

        # with open(f'src/{fail_name}.html', 'w') as file:
        #     file.write(req.text)
        # print('Processed in' + url)
        # time.sleep(random.randrange(3, 5))

        with open(f'src/{fail_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        count += 1

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

        projects_data_list.append({
            'Название пиццы': product_name,
            'Наполнение': product_filling
        })
        print(product_name)
        print(product_filling)
        print('*'*10)
        # print(f'{count}/{len(products_urls)}')

    # with open("data/projects_data.json", "a", encoding="utf-8") as file:
    #     json.dump(projects_data_list, file, indent=4, ensure_ascii=False)



def main():
    get_data('https://home-pizza.com/type1/')

if __name__=='__main__':
    main()