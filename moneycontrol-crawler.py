import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, timedelta
import subprocess
from requests import session

import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--sc_id', default="TCS")
	parser.add_argument('--todate', default="2018-10-10")
	parser.add_argument('--fromdate', default="2008-01-01")
	parser.add_argument('--exchange', default="B")
	parser.add_argument('--format_', default="daily")
	parser.add_argument('--page', default="1")
	args = parser.parse_args()

	url = "http://www.moneycontrol.com/stocks/hist_stock_result.php?"
	url = url + "sc_id=" + args.sc_id + "&"
	url = url + "pno=" + args.page + "&"
	url = url + "hdn=" + args.format_ + "&"
	url = url + "fdt=" + args.fromdate + "&"
	url = url + "todt=" + args.todate + "&"
	url = url + "ex=" + args.exchange

	with open(args.sc_id + '_' + args.fromdate + '_' + args.todate + '.csv','wb') as file:
		file.write(bytes('Date, Open, High, Low, Close, Volume, High_sub_Low, Open_sub_Close\n', 'UTF-8'))
		try:
			req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
			html_source = urlopen(req).read()
			parsed_html = BeautifulSoup(html_source, 'html.parser')
			rows = parsed_html.find_all("tr", class_="")
			for row in rows:
				cols = row.find_all("td")#, class_="")
				if len(cols)==8:
					line_str = ', '.join([x.find(text=True, recursive=True) for x in cols])
					print(line_str)
					file.write(bytes(line_str + '\n', 'UTF-8'))
		except Exception:
			traceback.print_exc()

if __name__ == '__main__':
	main()