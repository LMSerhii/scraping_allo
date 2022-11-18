import csv
import json
import pickle
import datetime
from params import cookies, headers

import requests


def collect_data(category=76):
    """ """

    curr_time = datetime.datetime.now().strftime("%m_%m_%Y %H:%M")

    response = requests.get(
        f'https://allo.ua/ua/catalog/category/update/?toolbar=%7B%22dir%22:%22desc%22,%22order%22:%22product_top_weight%22,%22mode%22:%22grid%22%7D&category_id={category}&qty=28&p=1&isAjax=1&currentLocale=uk_UA',
        cookies=cookies, headers=headers)

    pagination = response.json()['product_list']['pagination']['items_per_page']

    with requests.Session() as session:
        all_data = []
        for i in range(1, pagination + 1):
            response = session.get(
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