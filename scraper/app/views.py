from itertools import count
from django.shortcuts import render
from django.http import HttpResponse
from requests import get


def index(request):

    def load_chunk(page):
        URL = r'http://avtoparts.com.ua/Search/ComponentsByCategory'
        HEADERS = {
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
        return get(URL, headers=HEADERS, data=data)

    def parse_chunk(data):
        return data

    def parse_page():
        for page in count():
            parsed = parse_chunk(load_chunk(page))
            if not parsed:
                return
            yield parsed

    return HttpResponse(load_data(5))
