from itertools import count
from django.shortcuts import render
from django.http import HttpResponse
from requests import get
from lxml import html


def index(request):
    def load_chunk(page):
        url = r'http://avtoparts.com.ua/Search/ComponentsByCategory'
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = {
            'page': str(page),

            'category': '39',
            'addInfo': 'true',
            'price_S': 'false',
            'price_F': 'false',
            'price_R': 'false',
            'price_UD': 'false',
        }
        return get(url, headers=headers, data=data)

    def parse_row(row):
        result = {
            'id': row[0][1],
            'name': row[1],
            'brand': row[2],
            'available': row[3][0],
            'reserved': row[4][0],
            'price': row[6][0],
            'discount_price': row[7][0],
            'notes': row[8][0],
        }
        for key, value in result.items():
            if value.text is None:
                result[key] = ''
            else:
                result[key] = value.text.strip()
        return result

    def parse_chunk(data):
        data_rows = html.fragments_fromstring(data.text)
        return [parse_row(row) for row in data_rows]

    def parse_page():
        for page in count():
            parsed = parse_chunk(load_chunk(page))
            if not parsed:
                return
            yield parsed

    return HttpResponse('')
