#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国搜索关键词搜索 - 修正版
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def search_chinaso_fixed(keyword, max_results=10):
    """使用正确的选择器搜索中国搜索"""
    
    print(f"\n{'='*70}")
    print(f"搜索关键词: {keyword}")
    print('='*70)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    
    driver = None
    results = []
    
    try:
        print("📱 启动浏览器...")
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        print("🌐 访问中国搜索...")
        driver.get("https://www.chinaso.com/")
        time.sleep(2)
        
        # 使用正确的ID "q"
        print("🔍 查找搜索框（ID=q）...")
        search_box = driver.find_element(By.ID, "q")
        
        print(f"⌨️  输入关键词: {keyword}")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        
        print("⏳ 等待搜索结果...")
        time.sleep(5)
        
        print(f"✅ 当前URL: {driver.current_url}")
        
        # 提取搜索结果
        print("📋 提取搜索结果...")
        
        # 尝试多种选择器
        selectors = [
            "div.result",
            "div.news-box",
            "div[class*='result']",
            "h3 a",
            "a[href*='http']"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 3:
                    print(f"✅ 使用选择器: {selector}, 找到 {len(elements)} 个元素")
                    
                    for element in elements[:max_results]:
                        try:
                            title = element.text.strip()
                            url = element.get_attribute('href')
                            
                            if title and url and 'http' in url and len(title) > 10:
                                results.append({
                                    'title': title[:100],
                                    'url': url,
                                    'keyword': keyword
                                })
                        except:
                            continue
                    
                    if results:
                        break
            except:
                continue
        
        if results:
            print(f"\n📊 成功提取 {len(results)} 条结果")
            print(f"\n前3条结果:")
            for i, result in enumerate(results[:3], 1):
                print(f"\n{i}. {result['title']}")
                print(f"   {result['url']}")
        else:
            print("⚠️  未找到搜索结果，保存页面用于调试")
            with open(f'/root/clawd/news-workflow/search_{keyword}.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
        
        return results
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return []
        
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    test_keywords = ["战略新兴产业", "新能源"]
    
    print("=" * 70)
    print("中国搜索关键词检索测试（修正版）")
    print("=" * 70)
    
    all_results = []
    
    for keyword in test_keywords:
        results = search_chinaso_fixed(keyword, max_results=10)
        all_results.extend(results)
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print(f"测试完成 - 总计: {len(all_results)} 条结果")
    print("=" * 70)
