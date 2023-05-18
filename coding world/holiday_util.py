import requests, json

def holiday():
    with open('static/key/opendata.txt') as f:
        data_key = f.read()

    from datetime import datetime
    today = datetime.today().strftime("%Y%m%d")
    toyear = datetime.today().year
    url = (
        f"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear={toyear}&ServiceKey={data_key}"
    )

    result = requests.get(url)
    json_ob = json.loads(result.text)

    holiday = []
    for i in range(len(json_ob['response']['body']['items']['item'])):
        locdate = json_ob['response']['body']['items']['item'][i]['locdate']
        dateName = json_ob['response']['body']['items']['item'][i]['dateName']

        holiday.append({'locdate':locdate, 'dateName':dateName})

    return holiday