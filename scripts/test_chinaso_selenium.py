#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国搜索关键词搜索测试 - Selenium版本
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def test_chinaso_search(keyword):
    """测试中国搜索关键词搜索"""
    
    print(f"\n{'='*70}")
    print(f"测试关键词: {keyword}")
    print('='*70)
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    
    try:
        print("📱 启动浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        # 访问中国搜索
        print("🌐 访问中国搜索...")
        driver.get("https://www.chinaso.com/")
        time.sleep(2)
        
        print(f"✅ 页面标题: {driver.title}")
        
        # 查找搜索框
        print("🔍 查找搜索框...")
        search_box = driver.find_element(By.ID, "search_keyword")
        
        # 输入关键词
        print(f"⌨️  输入关键词: {keyword}")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        
        # 等待搜索结果加载
        print("⏳ 等待搜索结果...")
        time.sleep(3)
        
        print(f"✅ 当前URL: {driver.current_url}")
        
        # 提取搜索结果
        print("📋 提取搜索结果...")
        
        # 尝试多种可能的选择器
        result_selectors = [
            "div.result",
            "div.news-item",
            "div.item",
            "a[href*='http']"
        ]
        
        results = []
        for selector in result_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ 使用选择器: {selector}, 找到 {len(elements)} 个元素")
                    results = elements
                    break
            except:
                continue
        
        if results:
            print(f"\n📊 搜索结果数量: {len(results)}")
            print(f"\n前5个结果:")
            
            for i, result in enumerate(results[:5], 1):
                try:
                    # 尝试提取标题和链接
                    text = result.text[:100] if result.text else "无文本"
                    href = result.get_attribute('href') if result.tag_name == 'a' else "无链接"
                    print(f"{i}. {text}")
                    if href != "无链接":
                        print(f"   链接: {href}")
                except:
                    continue
        else:
            print("⚠️  未找到搜索结果")
            # 保存页面源码用于调试
            print("\n📄 页面源码片段:")
            print(driver.page_source[:500])
        
        return len(results)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 0
        
    finally:
        if driver:
            driver.quit()
            print("\n✅ 浏览器已关闭")

if __name__ == '__main__':
    # 测试关键词
    test_keywords = [
        "战略新兴产业",
        "新能源",
        "人工智能"
    ]
    
    print("=" * 70)
    print("中国搜索关键词搜索测试")
    print("=" * 70)
    
    results_summary = []
    
    for keyword in test_keywords:
        count = test_chinaso_search(keyword)
        results_summary.append({
            'keyword': keyword,
            'count': count
        })
        time.sleep(2)  # 避免请求过快
    
    # 输出汇总
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    for result in results_summary:
        print(f"{result['keyword']}: {result['count']} 个结果")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
