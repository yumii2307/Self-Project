import requests, json, folium, os
import pandas as pd
from urllib.parse import quote

def get_coord(addr):
    with open('static/data/roadapikey.txt') as f:
        road_key = f.read()
    base_url = 'https://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
    params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10&resultType=json'
    url = f'{base_url}?{params1}&keyword={quote(addr)}'
    result = requests.get(url)
    if result.status_code == 200:
        res = json.loads(result.text[1:-1])
        load_addr = res['results']['juso'][0]['roadAddr']

    with open('static/data/kakaoapikey.txt') as f:
        kakao_key = f.read()
    base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    header = {'Authorization': f'KakaoAK {kakao_key}'}
    url = f'{base_url}?query={quote(load_addr)}'
    result = requests.get(url, headers=header).json()
    lat = float(result['documents'][0]['y'])
    lng = float(result['documents'][0]['x'])

    return lat, lng

def hot_places(places, app):
    # 도로명 주소 구하기
    with open('static/data/roadapikey.txt') as f:
        road_key = f.read()
    road_addr_list = []
    for place in places:
        base_url = 'https://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
        params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10&resultType=json'
        url = f'{base_url}?{params1}&keyword={quote(place)}'
        result = requests.get(url)
        if result.status_code == 200:
            res = json.loads(result.text[1:-1])
            road_addr_list.append(res['results']['juso'][0]['roadAddr'])
        else:
            print(result.status_code)
    df = pd.DataFrame({'place':places, 'addr':road_addr_list})

    with open('static/data/kakaoapikey.txt') as f:
        kakao_key = f.read()
    base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    header = {'Authorization': f'KakaoAK {kakao_key}'}
    lat_list, lng_list = [], []
    for i in df.index:
        url = f'{base_url}?query={quote(df.addr[i])}'
        result = requests.get(url, headers=header).json()
        lat_list.append(float(result['documents'][0]['y']))
        lng_list.append(float(result['documents'][0]['x']))
    df['위도'] = lat_list
    df['경도'] = lng_list

    # 맵 그리기
    map = folium.Map(location=[df.위도.mean(), df.경도.mean()], zoom_start=13)

    for i in df.index:
        folium.Marker(
            location=[df.위도[i], df.경도[i]],
            popup=folium.Popup(df.addr[i], max_width=200),
            tooltip=df.place[i]
        ).add_to(map)
    filename = os.path.join(app.static_folder, 'img/hotplaces.html')
    map.save(filename)