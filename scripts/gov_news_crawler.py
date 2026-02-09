#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政府官网新闻爬虫
爬取国家卫健委、医保局、教育部等官方网站
"""

import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

class GovNewsCrawler:
    """政府官网新闻爬虫"""
    
    def __init__(self, sector):
        self.sector = sector
        self.results = []
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
