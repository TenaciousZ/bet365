# -*- coding: utf-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import time
from threading import Thread
from flask import Flask
import json

app = Flask(__name__)
browser = ''


class BrowserUtil:
    def __init__(self):
        self.html = ''
        self.thread = Thread(target=None)
        if False:
            self.browser = webdriver.Firefox()

    def init_google(self, linux=False):
        if linux:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Chrome()

    def init_firefox(self, linux=False):
        if linux:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox()

    def init_phantom(self, path):
        self.browser = webdriver.PhantomJS(executable_path=path)

    def set_url(self, url):
        self.browser.get(url=url)
        self.html = str(self.browser.find_element_by_tag_name('html').get_attribute('innerHTML'))

    def refresh_html(self):
        # self.browser.refresh()
        self.html = str(self.browser.find_element_by_tag_name('html').get_attribute('innerHTML'))
        return self.html

    def get_html_interval(self, url, interval):
        self.set_url(url)
        while True:
            self.refresh_html()
            time.sleep(interval)

    def create_thread(self, url, interval):
        if self.thread.is_alive():
            self.thread.join(1000)
        self.thread = Thread(target=self.get_html_interval, args=(url, interval))
        self.thread.start()


class SaveSoccerData:
    def __init__(self):
        self.mysql_server = ''
        # self.keys1 = []
        # self.keys2 = []
        # self.items1 = {}
        # self.items2 = {}
        self.result = []
        self.chrome = BrowserUtil()
        self.chrome.init_phantom("H:\\迅雷下载\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        pass

    def parse_soccer_data_from_html(self, html):
        b = BeautifulSoup(html, 'html.parser')
        competitions = b.findAll('div', {'class': 'ipo-Competition ipo-Competition-open '})
        print(len(competitions))
        if competitions is None or len(competitions) == 0:
            return 0

        # self.items2 = {}
        # self.keys2 = []
        self.result = []
        for c in competitions:
            competition_name = c.find('div', {
                'class': 'ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading '}).string
            print(competition_name)
            for teams in c.findAll('div', {'class': 'ipo-Fixture_TableRow '}):
                team_ab = teams.findAll('span', {'class': 'ipo-TeamStack_TeamWrapper'})
                odds = teams.findAll('span', {'class': 'gl-ParticipantCentered_Odds'})
                team_a = team_ab[0].string
                team_b = team_ab[1].string
                score_a = teams.find('div',
                                     {'class': 'ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamone '}).string
                score_b = teams.find('div',
                                     {
                                         'class': 'ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamtwo '}).string.string
                odd_a = odds[0].string
                odd_b = odds[1].string
                odd_x = odds[2].string
                c_time = teams.find('div', {'class': 'ipo-InPlayTimer '}).string
                item = {
                    "competition": competition_name,
                    "team": [team_a, team_b],
                    "time": c_time,
                    "point": [score_a, score_b],
                    "odd": [odd_a, odd_x, odd_b]
                }
                self.result.append(item)
                # key = competition_name + "_" + team_a + "_" + team_b
                # value = score_a + "-" + score_b + "," + odd_a + "-" + odd_b + "-" + odd_x
                # item = {
                #     "key": key,
                #     "value": value,
                #     "time": c_time,
                #     "competition_name": competition_name,
                #     "team_name_a": team_a,
                #     "team_name_b": team_b,
                #     "score_a": score_a,
                #     "score_b": score_b,
                #     "odd_a": odd_a,
                #     "odd_b": odd_b,
                #     "odd_x": odd_x
                # }
                # self.items2['key'] = item
                # self.keys2.append(key)

    def get_soccer_data(self):
        # chrome = ChromeUtil()
        # chromeUtil.init_browser()
        self.chrome.set_url('https://www.356884.com/zh-CHS/?&cb=10326512504#/IP/')
        time.sleep(2)
        self.chrome.browser.find_element_by_id("dv1").click()
        time.sleep(2)
        self.chrome.set_url('https://www.356884.com/#/IP/')
        time.sleep(2)
        self.chrome.refresh_html()
        # while True:
        #     chrome.refresh_html()
        #     self.parse_soccer_data_from_html(chrome.html)
        #     time.sleep(10)

    def get_last_data(self):
        self.chrome.refresh_html()
        print(self.chrome.html)
        self.parse_soccer_data_from_html(self.chrome.html)
        return self.result


@app.route('/sport/odd')
def hello():
    return json.dumps(saveSoccerData.get_last_data())


if __name__ == '__main__':
    global saveSoccerData
    saveSoccerData = SaveSoccerData()
    saveSoccerData.get_soccer_data()
    saveSoccerData.get_last_data()
    print("init done!")
    app.run(port=5001, host='0.0.0.0')
