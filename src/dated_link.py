# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import datetime

from bs4 import BeautifulSoup
import requests

from service_message import ServiceMessage

class DatedLink(object):
    def __init__(self, pagelink="", datetext="", report_base=""):
        self.report_base = report_base
        self.pagelink = pagelink
        self.datetext = datetext

    def __str__(self):
        return self.pagelink + " " + self.datetext

    def make_parent(self):
        parsed_page_date = datetime.strptime(self.datetext, '%B %d, %Y')
        parent = dict({'page_id': self.pagelink[self.pagelink.find('=') + 1:],
                       'date': parsed_page_date})
        return parent

    def parse_page(self):
        ret_text = []
        tgt_url = self.report_base + self.pagelink
        page_response = requests.get(tgt_url)
        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.text, 'html.parser')
        else:
            raise Exception(tgt_url, page_response.status_code, page_response.text)
        main_content = soup.findAll('div', {'class': 'internal-box2-inner'})[0]
        parent = self.make_parent()
        for paragraph in main_content.findAll('p')[0].findAll(text=True):
            if ServiceMessage.is_valid_message(paragraph):
                ret_text.append(ServiceMessage(text=paragraph,
                                               parent=parent).pre_processed_text)
        return sorted(ret_text)

    @staticmethod
    def process_message(raw_status_report):
        message = ServiceMessage(raw_status_report)
        return message.extract_full_data()
