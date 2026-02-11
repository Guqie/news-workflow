#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取中国搜索页面结构
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = '/usr/bin/chromium-browser'

try:
    print("启动浏览器...")
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("访问中国搜索...")
    driver.get("https://www.chinaso.com/")
    time.sleep(3)
    
    print(f"页面标题: {driver.title}")
    
    # 保存页面源码
    with open('/root/clawd/news-workflow/chinaso_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    print("✅ 页面源码已保存到: /root/clawd/news-workflow/chinaso_page.html")
    
    # 查找所有input元素
    inputs = driver.find_elements('tag name', 'input')
    print(f"\n找到 {len(inputs)} 个input元素:")
    for i, inp in enumerate(inputs[:10], 1):
        inp_id = inp.get_attribute('id')
        inp_name = inp.get_attribute('name')
        inp_type = inp.get_attribute('type')
        inp_class = inp.get_attribute('class')
        print(f"{i}. ID={inp_id}, Name={inp_name}, Type={inp_type}, Class={inp_class}")
    
    driver.quit()
    print("\n✅ 完成")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
