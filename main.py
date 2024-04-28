import json
import requests
import folium
from geopy import distance
from pprint import pprint
from flask import Flask


apikey = 'e3d06fc1-b2f8-4a74-98f3-08cf609fdae9'
address = input('Введите ваш адрес: ')


def get_coffi(coffi):
    return coffi['distance']


def fetch_coordinates(apikey, address):
    with open('D:\Хуйня\Python school\Урок_8\coffee.json', 'r', encoding='CP1251') as my_file:
        file_content = my_file.read()
    capitails = json.loads(file_content)
    
    coffis = []
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })

    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")

    for i in capitails:
        cof = dict()
        title = i['Name']
        latitude = i['Latitude_WGS84']
        longitude = i['Longitude_WGS84']
        newport_ri = (latitude, longitude)
        cleveland_oh = (lat, lon)
        cof['title'] = title
        cof['distance'] = distance.distance(newport_ri, cleveland_oh).km
        cof['latitude'] = latitude
        cof['longitude'] = longitude
        coffis.append(cof)
    
    mincoffis = sorted(coffis, key=get_coffi)
    map(lon, lat, mincoffis)
    return lon, lat, mincoffis


def map(lon, lat, mincoffis):
    m = folium.Map([lat, lon], zoom_start=16)
    folium.Marker(
    location=[lat, lon],
    tooltip="It's you",
    popup="You location",
    icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    for i in mincoffis[:5]:
        late = i['latitude']
        lone = i['longitude']
        title = i['title']
        group_1 = folium.FeatureGroup("first group").add_to(m)
        folium.Marker((late, lone), tooltip=(title),icon=folium.Icon("green")).add_to(group_1)
    folium.LayerControl().add_to(m)
    m.save("map.html")
    app = Flask(__name__)
    app.add_url_rule('/', 'hello', hello_world)
    app.run('0.0.0.0')


def hello_world():
    with open('map.html', encoding='utf8') as file:
        return file.read()


def main():
    fetch_coordinates(apikey, address)


if __name__ == '__main__':
    main()
