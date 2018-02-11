# -*- coding: utf-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import time
from threading import Thread
import pymysql


class BrowserUtil:
    def __init__(self):
        self.html = ''
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


class MysqlDao:
    def __init__(self, host, port, database, user, password, charset='utf8mb4', dictionary=pymysql.cursors.DictCursor):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.dictionary = dictionary
        self.db = pymysql.connect(host=self.host, port=self.port, database=self.database, user=self.user,
                                  password=self.password,
                                  charset=self.charset, cursorclass=self.dictionary)

    # 执行SQL语句
    def execute(self, sql, args=None):
        try:
            # 执行sql语句
            cursor = self.db.cursor()
            cursor.execute(sql, args)
            # 提交到数据库执行
            self.db.commit()
        except Exception as exception:
            # 如果发生错误则回滚
            print(exception)
            self.db.rollback()

    # 查询返回数据
    def query(self, sql, args=None):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, args)
            return cursor.fetchall()
        except Exception as ex:
            print(ex)
            return None

    # 查询一条数据
    def queryone(self, sql, args=None):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, args)
            return cursor.fetchone()
        except Exception as ex:
            print(ex)
            return None

    def close(self):
        self.db.close()


class SaveSoccerData:
    def __init__(self):
        self.mysql_server = ''
        self.key_to_id = {}
        self.items = []
        pass

    def save_to_mysql(self):
        keys = []
        for item in self.items:
            key = item['key']
            keys.append(key)
            key_id_item = self.key_to_id[key]
            if key_id_item is None:
                pass
            else:
                value = item['value']
                if value == key_id_item['value']:
                    pass
                else:
                    pid = key_id_item['pid']
                    # update
                    pass
        not_in_keys = []
        for key in self.key_to_id:
            if key not in keys:
                # delete
                not_in_keys.append(key)
        for key in not_in_keys:
            del self.key_to_id[key]

    def parse_soccer_data_from_html(self, html):
        b = BeautifulSoup(html, 'html.parser')
        competitions = b.findAll('div', {'class': 'ipo-Competition ipo-Competition-open '})
        print(len(competitions))
        if competitions is None or len(competitions) == 0:
            return 0

        self.items = []
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
                key = competition_name + "_" + team_a + "_" + team_b
                value = score_a + "-" + score_b + "," + odd_a + "-" + odd_b + "-" + odd_x
                item = {
                    "key": key,
                    "value": value,
                    "time": c_time,
                    "competition_name": competition_name,
                    "team_name_a": team_a,
                    "team_name_b": team_b,
                    "score_a": score_a,
                    "score_b": score_b,
                    "odd_a": odd_a,
                    "odd_b": odd_b,
                    "odd_x": odd_x
                }
                self.items.append(item)

    def get_soccer_data(self):
        browser = BrowserUtil()
        browser.init_firefox(True)

        browser.set_url('https://www.356884.com/zh-CHS/?&cb=10326512504#/IP/')
        time.sleep(2)
        browser.browser.find_element_by_id("dv1").click()
        time.sleep(2)
        browser.set_url('https://www.356884.com/#/IP/')
        time.sleep(2)
        while True:
            browser.refresh_html()
            self.parse_soccer_data_from_html(browser.html)
            time.sleep(10)


if __name__ == '__main__':
    saveSoccerData = SaveSoccerData()
    saveSoccerData.get_soccer_data()
