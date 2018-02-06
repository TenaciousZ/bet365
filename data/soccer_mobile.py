# -*- coding:utf-8 -*-

import time
from html.parser import HTMLParser

from selenium import webdriver
from flask import Flask
from pyvirtualdisplay import Display
import json

app = Flask(__name__)
browser = ''
url1 = "mobile.788-sb.com"
url2 = "mobile.356884.com"
url3 = "mobile.365-838.com"
'''
使用selenium 自动化测试的方式会自动的调用本地浏览器
环境准备：
1. python 环境 安装selenium 模块
2. 谷歌浏览器，自动化驱动引擎
3. https://mobile.365-838.com 已经手动进行登陆，并且勾选保持登录
'''


# 获取实时赔率
def get_sport_odd_on_time():
    global browser
    html = str(browser.find_element_by_tag_name('html').get_attribute('innerHTML'))
    rs = getItemList()
    rs.feed(html)
    rs.close()
    print(len(rs.rs))
    return rs.rs


def init_web():
    option = webdriver.ChromeOptions()
    display = Display(visible=0, size=(800, 600))
    display.start()
    # 设置成用户自己的数据目录
    # option.add_argument('--user-data-dir=/home/google/Chrome_data')
    global browser
    # browser = webdriver.Chrome(chrome_options=option)
    browser = webdriver.Chrome()
    # browser = webdriver.Chrome()
    browser.get('https://' + url1 + '/#type=InPlay;key=;ip=1;lng=1')
    time.sleep(5)
    print('refresh')
    browser.refresh()


# 解析页面获取赔率数据
class getItemList(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = -1
        self.key = None
        self.rs = []
        self.com_base = ''
        self.item = {}

    def handle_starttag(self, tag, attrs):
        tag = str(tag)
        if tag == 'div' and len(attrs) == 1 and attrs[0][1] == 'ipo-CompetitionBase ':
            self.flag = 1
        if tag == 'div' and len(attrs) == 1 and attrs[0][1] == 'ipo-Fixture ipo-Fixture_TimedFixture ':
            self.flag = 1
            self.item = {}

        if self.flag == 1 and len(attrs) == 1 and tag == 'div':
            if attrs[0][1] == 'ipo-Competition_Name ':
                self.key = 'competition'
            elif attrs[0][1] == 'ipo-Fixture_GameInfo ipo-Fixture_Time ':
                self.key = 'time'

        if self.flag == 1 and len(attrs) == 1 and tag == 'span':
            if attrs[0][1] == 'ipo-Fixture_Truncator ':
                self.key = 'team'
                self.item['competition'] = self.com_base
            elif attrs[0][1] == 'ipo-Fixture_PointField ':
                self.key = 'point'
            elif attrs[0][1] == 'ipo-Participant_OppOdds ':
                self.key = 'odd'

    def handle_data(self, data):
        if self.flag == 1 and self.key is not None:
            if self.key == 'competition':
                self.com_base = data
            elif self.key == 'time':
                self.item[self.key] = data
            else:
                if self.item.get(self.key) is None:
                    self.item[self.key] = []
                self.item[self.key].append(data)

    def handle_endtag(self, tag):
        if self.flag == 1 and self.key is not None:
            if self.key == 'odd' and len(self.item['odd']) == 3:
                self.flag = -1
                self.rs.append(self.item)
            self.key = None


@app.route('/sport/odd')
def hello():
    return json.dumps(get_sport_odd_on_time())


if __name__ == '__main__':
    init_web()
    app.run(port=5001, host='0.0.0.0')
