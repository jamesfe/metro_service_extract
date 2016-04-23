# -*- coding: utf-8 -*-
# from __future__ import absolute_import

from datetime import datetime, timedelta
import json
import re

from bs4 import BeautifulSoup
import requests

from service_message import ServiceMessage
from dated_link import DatedLink

METRO_ARCHIVES = 'http://www.wmata.com/rail/service_reports/viewReportArchive.cfm'
REPORT_LINK_SIGNATURE = 'viewPage_update.cfm?ReportID='
REPORT_BASE = 'http://www.wmata.com/rail/service_reports/'


def gather_dated_links():
    response = requests.get(METRO_ARCHIVES)
    if response.status_code == 200:
        in_soup = BeautifulSoup(response.text, "html.parser")
    else:
        raise Exception(METRO_ARCHIVES, response.status_code, response.text)

    ret_vals = []

    links = in_soup.findAll('a')

    for html_link in links:
        if 'href' in html_link.attrs and html_link.attrs['href'].find(REPORT_LINK_SIGNATURE) > -1:
            ret_vals.append(DatedLink(pagelink=html_link.attrs['href'],
                                      datetext=html_link.text,
                                      report_base=REPORT_BASE))
    return ret_vals


if __name__ == "__main__":
    out_data = []
    report_page_links = gather_dated_links()

    for link in report_page_links:
        print(link)
        for item in link.parse_page():
            cline = ServiceMessage(item, parent=link.make_parent())
            full_data = cline.extract_full_data()
            full_data['event_dtg'] = full_data['event_dtg'].isoformat()
            out_data.append(full_data)
    out_file = open('out.json', 'w')
    out_file.write(json.dumps(out_data))
    out_file.close()
