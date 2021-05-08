import re
import csv
import time
import urllib.request
import urllib.parse
from urllib.request import urlopen
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from cocoman_recommender.config.config import BASE_DIR
from cocoman_recommender.schemas.actor import ActorRepository, Actor
from cocoman_recommender.schemas.contents import ContentsRepository, Contents
from cocoman_recommender.schemas.director import DirectorRepository, Director
from cocoman_recommender.schemas.genre import GenreRepository, Genre
from cocoman_recommender.schemas.ott import OttRepository, Ott

target_ott = {
    'netflix': 'nfx',
    'watcha': 'wac',
    'wavve': 'wav',
    'naver-store': 'nvs',
}

field_names = ['title', 'year', 'actors', 'directors', 'story', 'genres', 'running_time', 'poster_path', 'grade_rate',
               'rating']
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('--kiosk')


class JustWatchCrawler:
    def __init__(self, ott_repository: OttRepository, contents_repository: ContentsRepository,
                 actor_repository: ActorRepository, director_repository: DirectorRepository,
                 genre_repository: GenreRepository):
        self.ott_repository = ott_repository
        self.contents_repository = contents_repository
        self.actor_repository = actor_repository
        self.director_repository = director_repository
        self.genre_repository = genre_repository

    def save_data_csv(self, data, lang: str = 'kr'):
        with open(BASE_DIR + '/datasets/justwatch_' + lang + '.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)

    def save_data_database(self, _target, data):
        for d in data:
            ott = self.ott_repository.get_by_name(_target)
            if ott is None:
                ott = Ott(name=_target, image_path='')
                ott = self.ott_repository.create(ott)

            actor_set = []
            for actor_name in d["actors"]:
                actor = self.ott_repository.get_by_name(actor_name)
                if actor is None:
                    actor = Actor(name=actor_name, image_path="")
                    actor = self.actor_repository.create(actor)
                actor_set.append(actor)

            director_set = []
            for director_name in d["directors"]:
                director = self.director_repository.get_by_name(director_name)
                if director is None:
                    director = Director(name=director_name, image_path="")
                    director = self.director_repository.create(director)
                director_set.append(director)

            genre_set = []
            for genre_name in d["genres"]:
                genre = self.genre_repository.get_by_name(genre_name)
                if genre is None:
                    genre = Genre(name=genre_name)
                    genre = self.genre_repository.create(genre)
                genre_set.append(genre)

            content = Contents(title=d["title"], year=d["year"], country="", running_time=int(d['running_time']),
                               broadcaster=_target, open_date="", broadcast_date="", story=d['story'],
                               poster_path=d['poster_path'], ott=ott, actors=actor_set, directors=director_set,
                               genres=genre_set)
            self.contents_repository.create(content)

    def crawling_justwatch(self, _target: str, lang: str = 'kr'):
        BASE_SEARCH_URL = '동영상서비스'
        base_encode = urllib.parse.quote(BASE_SEARCH_URL)

        BASE_URL = 'https://www.justwatch.com/' + lang + '/'
        BASE_ENCODED_URL = f'{base_encode}/'

        driver = webdriver.Chrome('./chromedriver', options=options)
        contents_info = []
        driver.get(BASE_URL + BASE_ENCODED_URL + _target)

        # wait to load page
        time.sleep(7)

        contents_urls = []
        exit_flag = True

        while exit_flag:
            try:
                contents_a = driver.find_elements_by_class_name('title-list-grid__item--link')
                urls = [contents_a[i].get_attribute('href') for i in range(len(contents_a))]
                for url in urls:
                    if not (url in contents_urls):
                        contents_urls.append(url)
                        driver.get(url)
                        time.sleep(1)

                        # get information of content
                        title = driver.find_element_by_xpath('//div[@class="title-block"]/h1').text
                        title = title.split(" (")
                        year = re.sub("\)", "", title[1])
                        title = title[0]
                        actors_name = []
                        actors_name_element = driver.find_elements_by_xpath(
                            '//div[@class="title-credits__actor"]/a[@class="title-credit-name"]')
                        for actor_name_e in actors_name_element:
                            actors_name.append(actor_name_e.get_attribute('textContent'))
                        story = driver.find_element_by_xpath(
                            '//p[@class="text-wrap-pre-line mt-0"]/span').get_attribute(
                            'textContent')

                        genres = []
                        directors = []
                        grade_rate = ""
                        running_time = ""
                        justwatch_rating = 0.0
                        imdb_rating = 0.0

                        extra_label = driver.find_elements_by_xpath(
                            '//div[@class="detail-infos__subheading label"]')
                        extra_element = driver.find_elements_by_xpath(
                            '//div[@class="detail-infos__detail--values"]')

                        for index in range(len(extra_label) // 2):
                            label = extra_label[index].get_attribute('textContent')
                            value = extra_element[index].get_attribute('textContent')
                            if label == " 재생 시간 ":
                                if "min" in value:
                                    running_time = re.sub("min", "", value)
                                elif "시간" in value:
                                    value = re.sub("분", "", value)
                                    time_set = str(value).split("시간")
                                    hour = int(time_set[0])
                                    minute = int(time_set[1])
                                    running_time = str(hour * 60 + minute)
                            elif label == "연령 등급":
                                grade_rate = value
                            elif label == "평점":
                                ratings = str(value).split(' ')
                                for rating in ratings:
                                    if rating == '':
                                        ratings.remove('')
                                if len(ratings) >= 1:
                                    ratings[0] = re.sub("%", "", ratings[0])
                                    justwatch_rating = float(ratings[0]) / 100
                                if len(ratings) >= 2:
                                    imdb_rating = float(ratings[1]) / 10
                            elif label == "장르":
                                value = re.sub(" ", "", value)
                                genres = str(value).split(',')
                            elif label == "감독":
                                value = re.sub(" ", "", value)
                                directors = str(value).split(',')

                        picture = driver.find_elements_by_xpath(
                            '//div[@class="title-poster title-poster--no-radius-bottom"]/picture[@class="picture-comp title-poster__image"]/img[@class="picture-comp__img"]'
                        )[0]
                        imgUrl = picture.get_attribute('src')
                        file_name = re.sub(" ", "", title)
                        poster_path = '/img/' + _target + '_' + file_name + '.jpg'
                        with urlopen(imgUrl) as f:
                            with open(BASE_DIR + poster_path, 'wb') as h:
                                img = f.read()
                                h.write(img)

                        content_info = {
                            "title": title,
                            "year": year,
                            "actors": actors_name,
                            "directors": directors,
                            "story": story,
                            "genres": genres,
                            "running_time": running_time,
                            "poster_path": poster_path,
                            "grade_rate": grade_rate,
                            "rating": {
                                "justwatch": justwatch_rating,
                                "imdb": imdb_rating,
                            },
                        }

                        contents_info.append(content_info)

                        driver.back()
                        time.sleep(2)
                    else:
                        exit_flag = False

                scroll_element = driver.find_element_by_tag_name('ion-content')
                driver.execute_script('arguments[0].scrollToBottom(10);', scroll_element)
                time.sleep(2)
            except NoSuchElementException:
                break

        self.save_data_csv(contents_info, lang)
        self.save_data_database(_target, contents_info)
