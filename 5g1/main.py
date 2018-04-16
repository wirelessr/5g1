#!/usr/bin/env python3

import configparser
import time

import requests

from logger import logger
from constants import (
    API_URL, CONDITIONS, WEB_URL_FORMAT_STR, SETTINGS_PATH, HEADERS,
)

from render import render

from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img = None
    def handle_starttag(self, tag, attrs):
        if ('id', 'hid_imgArr') in attrs:
            for attr, value in attrs:
                if attr == 'value':
                    self.img = value

cache = []


def get_houses(config):
    logger.info('requests 591 API...')
    response = requests.get(API_URL, params=CONDITIONS, headers=HEADERS)
    max_pages = int(config['default']['max_pages'])
    logger.info('total {0}, and retrieve {1}'.format(response.json()['records'], max_pages*30))
    
    for i in range(max_pages):
        CONDITIONS['firstRow'] = i*30
        response = requests.get(API_URL, params=CONDITIONS, headers=HEADERS)

        try:
            data = response.json()['data']
        except KeyError:
            logger.debug("response.json()['data']: {}".format(response.json()['data']))
            logger.error("Cannnot get data from response.json['data']")
        except Exception:
            logger.debug("response: {}".format(response.text))
            raise
        else:
            houses = data.get('data', [])
            logger.info(len(houses))

            for house in houses:
                yield house


def log_house_info(house):
    logger.info(
        "名稱：{}-{}-{}".format(
            house['region_name'],
            house['section_name'],
            house['fulladdress'],
        )
    )
    logger.info("網址：{}".format(WEB_URL_FORMAT_STR.format(house['post_id'])))
    logger.info("租金：{} {}".format(house['price'], house['unit']))
    logger.info("坪數：{} 坪".format(house['area']))
    logger.info("格局：{}".format(house['layout']))
    for url in house['img_url']:
        logger.info("圖片：{}".format(url))
    logger.info("更新時間：{}".format(time.ctime(house['refreshtime'])))
    logger.info("\n")

def get_img_url(house):
    detail = WEB_URL_FORMAT_STR.format(house['post_id'])
    response = requests.get(detail, headers=HEADERS)
    m = MyHTMLParser()
    m.feed(response.text)
    url_list = [url.strip('"') for url in m.img.split(',')]
    house['img_url'] = url_list

def search_houses(config):
    houses = get_houses(config)
    for house in houses:
        get_img_url(house)
        #log_house_info(house)
        cache.append(house)


def main():
    config = configparser.ConfigParser()
    config.read(SETTINGS_PATH)


    search_houses(config)
    print('cache size:', len(cache))
    #time.sleep(int(config['default']['parse_interval_in_seconds']))
    render(cache)

if __name__ == "__main__":
    main()
