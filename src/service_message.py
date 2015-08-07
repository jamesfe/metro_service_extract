# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import timedelta
import re


class ServiceMessage(object):
    def __init__(self, text='', parent={}):
        self.raw_input_message = text
        self.parent = parent
        self.pre_processed_text = self.preprocess_message()

    @staticmethod
    def is_valid_message(in_text):
        if len(ServiceMessage(in_text).pre_processed_text) <= 10:
            return False
        return True

    def preprocess_message(self):
        stat = self.raw_input_message.lower()
        stat = stat.replace('report archives', '').strip()
        stat = stat.replace('end content', '').strip()

        return stat

    def extract_full_data(self):
        ret_dict = dict()
        event_time = self.extract_event_time()
        if event_time is None:
            event_delta = timedelta(minutes=0)
        else:
            event_delta = timedelta(hours=event_time['hour'], minutes=event_time['min'])
        event_date = self.parent['date'] + event_delta
        ret_dict['delay'] = self.extract_delay_value()
        ret_dict['gap'] = self.extract_gap_value()
        ret_dict['expressed'] = self.extract_expressed_value()
        ret_dict['id'] = self.parent['page_id'] + "_" + self.scrunchtime()
        ret_dict['event_dtg'] = event_date
        ret_dict['proc_text'] = self.pre_processed_text
        ret_dict['colors'] = self.extract_color_reference()
        return ret_dict

    def scrunchtime(self):
        event_time = self.extract_event_time()
        if event_time is None:
            return "UNK"
        return str(event_time['hour']) + "_" + str(event_time['min'])

    def extract_event_time(self):
        time_text = re.search('^\s?([0-9]{1,2})\s?:?([0-9]{1,2})\s?(a|p)',
                              self.pre_processed_text,
                              re.I | re.M)
        if time_text is not None and len(time_text.groups()) == 3:
            ret_vals = dict()
            try:
                if time_text.groups()[2] == 'p':
                    ret_vals['hour'] = int(time_text.groups()[0]) + 12
                else:
                    ret_vals['hour'] = int(time_text.groups()[0])
                ret_vals['min'] = int(time_text.groups()[1])
                return ret_vals
            except Exception as e:
                print("Exception: ", e)
                return None
        return time_text

    def extract_delay_value(self):
        if self.pre_processed_text.find('delay') == -1:
            return None
        search_area = self.pre_processed_text[10:]
        num_minutes = re.search('^\D*([0-9]{1,3})\D*', search_area)
        if num_minutes is None:
            return None
        if search_area.find('minute') > -1:
            return {'minutes': int(num_minutes.groups()[0])}
        else:
            return None

    def extract_gap_value(self):
        if self.pre_processed_text.find('gap') == -1:
            return None
        search_area = self.pre_processed_text[10:]
        num_minutes = re.search('^\D*([0-9]{1,3})\D*', search_area)
        if num_minutes is None:
            return None
        if search_area.find('minute') > -1:
            return {'minutes': int(num_minutes.groups()[0])}
        else:
            return None

    def extract_color_reference(self):
        line_colors = ['red', 'orange', 'blue', 'green', 'yellow', 'silver']
        ret_colors = []
        bad_stations = ['greenbelt', 'green belt', 'silver spring', 'greensboro']
        colorless_text = self.pre_processed_text
        for station in bad_stations:
            colorless_text = colorless_text.replace(station, '')
        for color in line_colors:
            if colorless_text.find(color) > -1:
                ret_colors.append(color)
        return ret_colors

    def extract_expressed_value(self):
        if self.pre_processed_text.find('expressed') > -1:
            return True
        return False
