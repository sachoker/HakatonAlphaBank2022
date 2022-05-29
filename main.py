from bs4 import BeautifulSoup
from requests import get
import pandas as pd

frame = pd.DataFrame(columns=['mall_lat', 'mall_lng'])
city = {'spb': 6, 'nizhniy-novgorod': 2, 'ekaterinburg': 2, 'novosibirsk': 1}
for j in city.keys():
    for i in range(1, city[j] + 1):
        data = get(f"https://www.malls.ru/city/spb.shtml?PAGEN_2={i}")
        soup = BeautifulSoup(data.text, features="html.parser")
        res = soup.find_all('span', class_='green')
        for i in res:
            s = get('https://graphhopper.com/api/1/geocode',
                    params={'key': 'bba5abd0-6b35-446f-807e-574371b84e71', 'q': i}).json()
            try:
                s = s['hits'][0]['point']
            except IndexError:
                print(s)
                continue
            lat = s['lat']
            lon = s['lng']
            frame = frame.append({'mall_lat': lat, 'mall_lng': lon}, ignore_index=True)

frame.to_csv('mall_coord')
