from datetime import datetime, date

import pandas as pd

from bonjuredv_api import get_category_product_data, get_categories_ids


def _now() -> str:
    """Function returns formatted current time."""

    return datetime.now().strftime("%H:%M:%S")


def _filter_data(category_product_data: dict) -> list[dict]:
    """Function filters category product data, extracts only the necessary
    data and adds some additional data (current date)."""

    result = []
    cur_date = date.today().strftime("%m/%d/%Y")

    while category_product_data['data']:
        product_data = category_product_data['data'].pop(0)

        # Check nested data for null.
        if product_data['category']:
            category_name = product_data['category']['name']
            if isinstance(category_name, str): category_name.strip()
            category_id = product_data['category']['id']
        else:
            category_name = None
            category_id = None

        if product_data['barcode']:
            barcode = product_data['barcode']['value']
        else:
            barcode = None

        if product_data['manufacturer']:
            manufacturer = product_data['manufacturer']['name']
        else:
            manufacturer = None

        if product_data['brand']:
            brand_name = product_data['brand']['name']
        else:
            brand_name = None

        if product_data['default_image']:
            product_image = product_data['default_image']['uri']
            if isinstance(product_image, str): product_image.strip()
        else:
            product_image = None

        product_title = product_data['title']
        if isinstance(product_title, str): product_title.strip()
        product_id = product_data['id']
        offer_price = product_data['offer_price']
        base_price = product_data['base_price']
        discount = int(100 - (offer_price / base_price) * 100)

        filtered_product_data = {
                'date': cur_date,
                'category_name': category_name,
                'category_id': category_id,
                'product_title': product_title,
                'product_image': product_image,
                'product_id': product_id,
                'barcode': barcode,
                'manufacturer': manufacturer,
                'brand_name': brand_name,
                'offer_price': offer_price,
                'base_price': base_price,
                'discount': discount
                    }
        result.append(filtered_product_data)

    return result
                
def main() -> None:
    print(f'{_now()} Start parsing process.')
    #category_restriction_count = 5
    data_to_store = []
    categories_ids = get_categories_ids()
    for category_id in categories_ids:
        #category_restriction_count -= 1
        print(f'{_now()} Parsing category {category_id}...')
        product_data = get_category_product_data(category_id)
        filtered_product_data = _filter_data(product_data)
        data_to_store = data_to_store + filtered_product_data

        #if category_restriction_count == 0:
        #   break

    print(f'{_now()} Parsing process compeleted.')

    df = pd.DataFrame(data_to_store)
    cur_date = datetime.now().strftime('%m%d%Y-%H%M%S')
    file_path = f'./data/products_data_{cur_date}.csv'
    df.to_csv(file_path, encoding='utf-8', sep='\t')
    print(f'{_now()} Data stored to {file_path}.')


if __name__ == "__main__":
    main()

