import csv
import json
import pickle
import datetime

import requests


def collect_data(category=76):
    """ """

    curr_time = datetime.datetime.now().strftime("%m_%m_%Y %H:%M")

    cookies = {
        'store': 'default_ua',
        '__uzma': '8d43ec21-7086-411e-a36d-73211e0b9036',
        '__uzmb': '1668630874',
        '__uzme': '9661',
        'frontend': '6ce64df767184718861b15976eb08594',
        'is_bot': '0',
        'detect_mobile_type': '0',
        '_gcl_au': '1.1.997059443.1668630876',
        '__ssds': '2',
        '__utmc': '45757819',
        '__utmz': '45757819.1668630877.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'sc': 'BBC84696-547D-C629-CB45-9AFAC0FE1783',
        '__ssuzjsr2': 'a9be0cd8e',
        '__uzmaj2': '0c78cd6d-750b-4c35-a911-357ffe9b2977',
        '__uzmbj2': '1668630876',
        '_ga': 'GA1.2.26768741.1668630877',
        '_gid': 'GA1.2.871365318.1668630877',
        '_fbp': 'fb.1.1668630876833.1434635192',
        '__exponea_etc__': '70ae1551-1cd9-4f8d-86b6-25f37cb341cc',
        '__exponea_time2__': '-0.03090834617614746',
        'frontend_hash': 'oWqS3Q6ce64df767184718861b15976eb08594aKq3rv',
        '_tt_enable_cookie': '1',
        '_ttp': '697733dc-4cf7-4ac0-bf40-02141a80c50e',
        'protocol': 'https',
        'city_id': '4',
        'scCart': '0a5f2767-1701-a233-1332-63627d996208',
        '__utma': '45757819.26768741.1668630877.1668630877.1668634341.2',
        '__utmt': '1',
        '__insp_wid': '1964961402',
        '__insp_nv': 'true',
        '__insp_targlpu': 'aHR0cHM6Ly9hbGxvLnVhL3VhL3BsYW5zaGV0eS1pLWdhZHpoZXR5Lw%3D%3D',
        '__insp_targlpt': '0J%2FQu9Cw0L3RiNC10YLQuCwg0L3QvtGD0YLQsdGD0LrQuCDRgtCwINCf0Jog0LrRg9C%2F0LjRgtC4INCyINCa0LjRlNCy0ZYsINCj0LrRgNCw0ZfQvdGWIHwgQUxMTzog0YbRltC90Lgg0LIg0LzQsNCz0LDQt9C40L3Rlg%3D%3D',
        '__insp_norec_sess': 'true',
        '__utmb': '45757819.16.9.1668636770362',
        '__uzmcj2': '461439133945',
        '__uzmdj2': '1668636833',
        '__insp_slim': '1668636835832',
        'private_content_version': '60cd3bbac57595f0a78adc0e6e2238ab',
        't_s_c_f_l': '0%3A2%3A1048d8daad79a8cc%3AjR3zSgkClCpnKXQgcgn8Lw%3D%3D',
        '__uzmc': '5678846681061',
        '__uzmd': '1668636839',
        '_gat_UA-63509214-1': '1',
    }

    headers = {
        'authority': 'allo.ua',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
        'content-type': 'text/plain',
        'referer': 'https://allo.ua/ua/products/notebooks/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'stacktrace': 'You can check it in Chrome or Safari',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-use-nuxt': '1',
    }

    response = requests.get(
        f'https://allo.ua/ua/catalog/category/update/?toolbar=%7B%22dir%22:%22desc%22,%22order%22:%22product_top_weight%22,%22mode%22:%22grid%22%7D&category_id={category}&qty=28&p=1&isAjax=1&currentLocale=uk_UA',
        cookies=cookies, headers=headers)

    pagination = response.json()['product_list']['pagination']['items_per_page']

    all_data = []
    for i in range(1, pagination + 1):
        response = requests.get(
            f'https://allo.ua/ua/catalog/category/update/?toolbar=%7B%22dir%22:%22desc%22,%22order%22:%22product_top_weight%22,%22mode%22:%22grid%22%7D&category_id={category}&qty=28&p={i}',
            cookies=cookies, headers=headers)
        items = response.json()['product_list']['items']

        for item in items:
            stock_status = item['stock_status']
            if stock_status == 1:
                item_id = item['id']
                try:
                    brand = item['brand']
                except Exception as ex:
                    brand = None
                name = item['name']
                try:
                    old_price = item['price']['old_price']
                except Exception as ex:
                    old_price = None
                try:
                    price = item['price']['price']
                except Exception as ex:
                    price = None

                url = item['url']
                try:
                    description_attributes = item['description_attributes']

                    attributes = []
                    for description_attribute in description_attributes:
                        attribute = description_attribute['value']
                        attributes.append(attribute)
                except Exception as ex:
                    attributes = None
                all_data.append(
                    [item_id, brand, name, attributes, url, old_price, price]
                )
        print(f"[INFO] Page {i} completed")
    with open(f"table_{curr_time}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'id',
                'brand',
                'name',
                'attributes',
                'url',
                'old_price',
                'price'
            )
        )
        writer.writerows(all_data)

    return "Done ..."


def main():
    print(collect_data())


if __name__ == '__main__':
    main()