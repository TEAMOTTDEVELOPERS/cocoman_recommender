import csv
import time
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

target_ott = {
    'netflix': 'netflix',
    'watcha': 'watcha',
    'wavve': 'wavve',
    'naver-store': 'naver-store',
}

field_names = ['title', 'actors', 'roles', 'synopsis', 'genres', 'rating']

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('--kiosk')


def crawling(_target: str):
    BASE_SEARCH_URL = '동영상서비스'
    base_encode = urllib.parse.quote(BASE_SEARCH_URL)

    BASE_URL = 'https://www.justwatch.com/kr/'
    BASE_ENCODED_URL = f'{base_encode}/'

    driver = webdriver.Chrome('chromedriver', options=options)
    contents_info = []
    driver.get(BASE_URL + BASE_ENCODED_URL + target_ott[_target])

    # wait to load page
    time.sleep(7)

    contents_urls = []
    exit_flag = False

    while True:
        try:
            contents_a = driver.find_elements_by_class_name('title-list-grid__item--link')
            urls = [contents_a[i].get_attribute('href') for i in range(len(contents_a))]
            for url in urls:
                print(url)
                if not (url in contents_urls):
                    contents_urls.append(url)
                    driver.get(url)
                    time.sleep(1)

                    # get information of content
                    title = driver.find_element_by_xpath('//div[@class="title-block"]/h1').text
                    actors_name = []
                    actors_name_element = driver.find_elements_by_xpath('//div[@class="title-credits__actor"]/a[@class="title-credit-name"]')
                    for actor_name_e in actors_name_element:
                        actors_name.append(actor_name_e.get_attribute('textContent'))
                    roles_name = []
                    roles_name_element = driver.find_elements_by_xpath('//div[@class="title-credits__actor--role--name"]/strong')
                    for role_name_e in roles_name_element:
                        roles_name.append(role_name_e.get_attribute('textContent'))
                    synopsis = driver.find_element_by_xpath('//p[@class="text-wrap-pre-line mt-0"]/span').get_attribute('textContent')
                    genres = []
                    genres_element = driver.find_elements_by_xpath('//div[@class="detail-infos__detail--values"]/span')
                    for index in range(len(genres_element) // 2):
                        genres.append(genres_element[index].get_attribute('textContent'))

                    rating_element = driver.find_elements_by_xpath('//div[@class="jw-scoring-listing__rating"]/a')
                    justwatch_rating = rating_element[0].get_attribute('textContent')
                    if len(rating_element) == 2:
                        imdb_rating = rating_element[1].get_attribute('textContent')
                    else:
                        imdb_rating = "0"

                    content_info = {
                        "title": title,
                        "actors": actors_name,
                        "roles": roles_name,
                        "synopsis": synopsis,
                        "genres": genres,
                        "rating": {
                            "justwatch": justwatch_rating,
                            "imdb": imdb_rating,
                        },
                    }

                    contents_info.append(content_info)

                    driver.back()
                    time.sleep(2)
                else:
                    exit_flag = True
                    break

            if exit_flag:
                break

            scroll_element = driver.find_element_by_tag_name('ion-content')
            driver.execute_script('arguments[0].scrollToBottom(10);', scroll_element)
            time.sleep(2)
        except NoSuchElementException:
            break

    with open('justwatch_' + _target + '.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(contents_info)


if __name__ == "__main__":
    crawling('netflix')
