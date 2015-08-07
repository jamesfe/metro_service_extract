# -*- coding: utf-8 -*-

import json

from service_message import ServiceMessage

PROCESSED_MESSAGE_FILE = '../test_data/json_export_cao_02AUG2015.json'


def test_line_color_extract(message_text):
    proc_message = ServiceMessage(message_text)
    return proc_message.extract_color_reference(), proc_message.pre_processed_text

if __name__ == '__main__':
    """
    Load the JSON file, check the preprocessed text for colors,
     then print everything out for visual inspection.
    """
    messages = None
    with open(PROCESSED_MESSAGE_FILE, 'r') as json_fp:
        messages = json.load(json_fp)
    for message in messages:
        print(test_line_color_extract(message['proc_text']))
