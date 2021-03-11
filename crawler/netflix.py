"""
<Netflix secret code>
액션 & 어드벤처 : 1365
애니메이션 : 7424
어린이 & 가족 : 783
고전 : 31574
코미디 : 6548
컬트 : 7627
다큐멘터리 : 6839
드라마 : 5763
신앙 : 26835
게이 & 레즈비언 : 5977
호러 : 8711
인디 : 7077
음악: 1701
로맨스 : 8883
SF & 판타지 : 1492
스포츠 : 4370
스릴러 : 8933
TV : 83
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup


def crawling():
    SEARCH_URL = 'https://www.netflix.com/kr/browse/genre/'
    DETAIL_SEARCH_URL = 'https://www.netflix.com/kr/title/'

    contents_info = []

    contents_code = [1365, 7424, 783, 31574, 6548, 7627, 6839, 5763, 26835,
                     5977, 8711, 7077, 1701, 8883, 1492, 4370, 8933, 83]

    for code in contents_code:
        page = requests.get(SEARCH_URL + str(code))
        soup = BeautifulSoup(page.content, 'html.parser')
        contents = soup.find_all('img', {'class': 'nm-collections-title-img'})
        contents_ids = []
        for c in contents:
            contents_ids.append(c.attrs['data-title-id'])

        for c_id in contents_ids:
            page = requests.get(DETAIL_SEARCH_URL + c_id)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find('h1', {'class': 'title-title'}).string
            synop = soup.find('div', {'class': 'title-info-synopsis'}).string
            genres = soup.find_all('a', {'class': 'more-details-item item-genres'})
            genres_text = ''
            for g in genres:
                genres_text = genres_text + ',' + g.text
            info = [title, synop, genres_text[1:]]
            contents_info.append(info)

    df = pd.DataFrame(contents_info, ['title', 'synopsis', 'genre'])
    df.to_csv('netflix_kr.csv')
