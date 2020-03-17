import requests
from lxml import html
import json
from requests.exceptions import HTTPError


def get_site_1_json():
    try:
        page = requests.get('https://www.mebelshara.ru/contacts')
        page.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        tree = html.fromstring(page.content)
        phone = tree.cssselect('.phone-num.zphone')[0].text
        cities = tree.cssselect('.city-item')
        shop_list = []
        for city in cities:
            city_name = city.cssselect('.js-city-name')[0].text
            shops = city.cssselect('.shop-list > div')
            for shop in shops:
                attributes = shop.attrib
                name = attributes['data-shop-name']
                address = city_name + ', ' + attributes['data-shop-address']
                if attributes['data-shop-mode1'] == 'Без выходных:':
                    working_hours = ['пн-вс ' + attributes['data-shop-mode2']]
                else:
                    working_hours = [attributes['data-shop-mode1'], attributes['data-shop-mode2']]
                latlon = [attributes['data-shop-latitude'], attributes['data-shop-longitude']]
                shop_json = json.dumps(
                    {'address': address, 'latlon': latlon, 'name': name, 'phones': phone,
                     'working_hours': working_hours},
                    ensure_ascii=False)
                shop_list.append(shop_json)
        print("Success 1")
        return shop_list


def get_site_2_json():
    try:
        page = requests.get(
            'https://www.tui.ru/api/office/list/?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all'
            '&toBeOpenOnHolidays=false')
        page.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        offices_json_full = page.json()
        office_list = []
        for office in offices_json_full:
            address = office['address']
            latlon = [office['latitude'], office['longitude']]
            name = office['name']
            phones = []
            for phone in office['phones']:
                phones.append(phone['phone'])
            hours_of_operation = office['hoursOfOperation']
            if not hours_of_operation['sunday']['isDayOff']:
                sunday = hours_of_operation['sunday']['startStr'] + ' - ' + hours_of_operation['sunday']['endStr']
            if not hours_of_operation['workdays']['isDayOff']:
                workdays = hours_of_operation['workdays']['startStr'] + ' - ' + hours_of_operation['workdays']['endStr']
            if not hours_of_operation['saturday']['isDayOff']:
                saturday = hours_of_operation['saturday']['startStr'] + ' - ' + hours_of_operation['saturday']['endStr']
            if not hours_of_operation['workdays']['isDayOff']:
                working_hours = ['пн-пт ' + workdays]
            if not hours_of_operation['saturday']['isDayOff']:
                if workdays == saturday:
                    working_hours = ['пн-сб ' + workdays]
                else:
                    working_hours = ['пн-пт ' + workdays, 'сб ' + saturday]
            if not hours_of_operation['sunday']['isDayOff']:
                if workdays == saturday and saturday == sunday:
                    working_hours = ['пн-вс  ' + workdays]
                elif workdays == saturday:
                    working_hours = ['пн-сб ' + workdays, 'вс ' + sunday]
                elif saturday == sunday:
                    working_hours = ['пн-пт ' + workdays, 'сб-вс ' + sunday]
                else:
                    working_hours = ['пн-пт ' + workdays, 'сб ' + saturday, 'вс ' + sunday]
            office_json = json.dumps(
                {'address': address, 'latlon': latlon, 'name': name, 'phones': phones, 'working_hours': working_hours},
                ensure_ascii=False)
            office_list.append(office_json)
        print("Success 2")
        return office_list
