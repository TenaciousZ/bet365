# -*- coding: utf-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import time
import datetime
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


# dao = MysqlDao(host='47.94.198.236', port=3306, database='bet365', user='root', password='root@1234560789')
dao = MysqlDao(host='112.74.54.187', port=3306, database='bet365', user='root', password='root@1234560789')


# 保存球赛数据
class SaveSoccerData:
    def __init__(self):
        self.mysql_server = ''
        self.key_to_id = {}
        self.items = []
        self.browser = BrowserUtil()
        pass

    def save_to_mysql(self):
        keys = []
        for item in self.items:
            key = item['key']
            value = item['value']
            keys.append(key)

            # 不存在 则添加
            if not self.key_to_id.__contains__(key):
                soccer = self.save_soccer(item)
                self.save_soccer_detail(soccer['id'], item)
                # 加入队列
                self.key_to_id[key] = {
                    "value": value,
                    "pid": soccer['id']
                }
            else:
                key_id_item = self.key_to_id[key]
                if value == key_id_item['value']:
                    continue
                else:
                    pid = key_id_item['pid']
                    self.save_soccer_detail(pid, item)
                    self.key_to_id[key] = {
                        "value": value,
                        "pid": pid
                    }

        # 结束的比赛入库
        not_in_keys = []
        for key in self.key_to_id:
            if key not in keys:
                key_id_item = self.key_to_id[key]
                self.end_soccer(str(key_id_item['pid']))
                not_in_keys.append(key)
        for key in not_in_keys:
            del self.key_to_id[key]

    def save_soccer(self, item):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        key = date + "-" + item['key']
        select_sql = "SELECT * FROM tb_soccer WHERE `key`='" + key + "'"
        rs = dao.queryone(select_sql)
        if rs is None:
            insert_sql = "INSERT INTO `tb_soccer` " \
                         "(`key`, `date`, `time`, `league_name`, `team_a_name`, `team_b_name`, `finished`, `remark`) " \
                         "VALUES " \
                         "(%(key)s, %(date)s, %(time)s, %(league_name)s, %(team_a_name)s, %(team_b_name)s, %(finished)s, %(remark)s);"
            bean = {
                "key": key,
                "date": date,
                "time": datetime.datetime.now().strftime('%H:%M:%S'),
                # "start_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "league_name": item['competition_name'],
                "team_a_name": item['team_a_name'],
                "team_b_name": item['team_b_name'],
                "finished": "0",
                "remark": 'insert'
            }
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'insert soccer', str(bean))
            dao.execute(insert_sql, bean)
            return self.save_soccer(item)
        elif rs['finished'] == 1:
            update_sql = "UPDATE `tb_soccer` SET  `finished`=0, `result`=NULL, `remark`='update' WHERE `id`='" + str(rs['id']) + "'"
            dao.execute(update_sql)
            return self.save_soccer(item)
        else:
            return rs

    @staticmethod
    def save_soccer_detail(p_id, item):
        insert_sql = "INSERT INTO `tb_soccer_detail`" + \
                     "(`p_id`, `date`, `time`, `league_name`, `team_a_name`, `team_b_name`, `score_a`, `score_b`, `odd_a`, `odd_b`, `odd_x`, `remark`) " + \
                     " VALUES " + \
                     " (%(p_id)s, %(date)s, %(time)s,%(league_name)s, %(team_a_name)s, %(team_b_name)s,%(score_a)s, %(score_b)s,%(odd_a)s, %(odd_b)s,%(odd_x)s, %(remark)s)"
        bean = {
            "p_id": str(p_id),
            "date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "time": item['time'],
            "league_name": item['competition_name'],
            "team_a_name": item['team_a_name'],
            "team_b_name": item['team_b_name'],
            "score_a": item['score_a'],
            "score_b": item['score_b'],
            "odd_a": item['odd_a'],
            "odd_b": item['odd_b'],
            "odd_x": item['odd_x'],
            "remark": "update data"
        }
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'insert soccer_detail', str(bean))
        dao.execute(insert_sql, bean)

    @staticmethod
    def end_soccer(soccer_id):
        """
        结束比赛
        :param soccer_id:
        :return:
        """
        soccer = dao.queryone("SELECT * FROM tb_soccer WHERE `id`='" + soccer_id + "'")
        soccer_detail = dao.queryone(
            "SELECT * FROM tb_soccer_detail WHERE `p_id`='" + soccer_id + "' ORDER BY create_time DESC LIMIT 1")

        if soccer is None or soccer_detail is None:
            return 0
        else:
            team_a_score = soccer_detail['score_a']
            team_b_score = soccer_detail['score_b']
            result = 'x'
            if team_a_score > team_b_score:
                result = 'a'
            elif team_a_score < team_b_score:
                result = 'b'
            update_sql = "UPDATE `tb_soccer` SET  `finished`=1, `result`='" + result + "', `remark`='end' WHERE `id`='" + soccer_id + "'"
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'end soccer', update_sql)
            dao.execute(update_sql)

    def parse_soccer_data_from_html(self, html):
        """
        从HTML中解析比赛数据
        :param html: HTML页面字符串
        :return: 0/1
        0-错误/没有数据-需要刷新页面
        1-正确-数据已经存入类属性中 self.items
        """
        b = BeautifulSoup(html, 'html.parser')
        # 频道判断
        rs = b.findAll('div', {
            'class': 'ipo-ClassificationBarButtonBase ipo-ClassificationBarButtonBase_Selected ipo-ClassificationBarButtonBase_Selected-1 '})
        if rs is None or len(rs) == 0 or len(rs[0].findAll(text="足球")) == 0:
            # 转移至足球频道
            for item in self.browser.browser.find_elements_by_class_name('ipo-ClassificationBarButtonBase_Label '):
                if str(item.text).strip() == '足球':
                    item.click()
                    time.sleep(1)
            return 0

        # 获取所有联赛
        competitions = b.findAll('div', {'class': 'ipo-Competition ipo-Competition-open '})
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'number', len(competitions))
        if competitions is None or len(competitions) == 0:
            return 0

        # 遍历联赛获取所有球队比赛
        self.items = []
        for c in competitions:
            competition_name = c.find('div', {
                'class': 'ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading '}).string
            for teams in c.findAll('div', {'class': 'ipo-Fixture_TableRow '}):
                # 获取球队与赔率
                team_ab = teams.findAll('span', {'class': 'ipo-TeamStack_TeamWrapper'})
                odds = teams.findAll('span', {'class': 'gl-ParticipantCentered_Odds'})
                if len(team_ab) < 2:
                    continue
                team_a = team_ab[0].string
                team_b = team_ab[1].string
                # 获取得分
                score_a = teams.find('div',
                                     {'class': 'ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamone '}).string
                score_b = teams.find('div',
                                     {
                                         'class': 'ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamtwo '}).string.string
                if len(odds) < 3:
                    continue
                odd_a = odds[0].string
                odd_b = odds[1].string
                odd_x = odds[2].string
                # 未开启形态判断
                if odd_a == 'SP' or odd_b == 'SP' or odd_x == 'SP':
                    continue

                # 获取时间
                c_time = teams.find('div', {'class': 'ipo-InPlayTimer '}).string
                key = competition_name + "_" + team_a + "_" + team_b
                value = score_a + "-" + score_b + "," + odd_a + "-" + odd_b + "-" + odd_x
                item = {
                    "key": key,
                    "value": value,
                    "time": c_time,
                    "competition_name": competition_name,
                    "team_a_name": team_a,
                    "team_b_name": team_b,
                    "score_a": score_a,
                    "score_b": score_b,
                    "odd_a": odd_a,
                    "odd_b": odd_b,
                    "odd_x": odd_x
                }
                self.items.append(item)
        return 1

    def get_soccer_data(self):
        self.browser.init_firefox(False)

        self.browser.set_url('https://www.356884.com/zh-CHS/?&cb=10326512504#/IP/')
        time.sleep(2)
        self.browser.browser.find_element_by_id("dv1").click()
        time.sleep(2)
        self.browser.set_url('https://www.356884.com/#/IP/')
        time.sleep(2)
        while True:
            self.browser.refresh_html()
            try:
                flag = self.parse_soccer_data_from_html(self.browser.html)
                if flag == 0:
                    self.browser.browser.refresh()
                self.save_to_mysql()
            except Exception as e:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e)
            time.sleep(5)


if __name__ == '__main__':
    saveSoccerData = SaveSoccerData()
    saveSoccerData.get_soccer_data()
