# -*- coding: utf-8 -*-
import json
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import time
from threading import Thread


class ChromeUtil:
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options=self.option)
        self.html = ''
        self.thread = Thread(target=None)

    def init_browser_on_linux(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.browser = webdriver.Chrome(chrome_options=self.option)

    def set_url(self, url):
        self.browser.get(url=url)
        self.html = str(self.browser.find_element_by_tag_name('html').get_attribute('innerHTML'))

    def refresh_html(self):
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