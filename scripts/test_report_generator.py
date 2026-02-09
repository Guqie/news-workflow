#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告生成器 - 验证新闻聚合系统
"""

import json
import os
from datetime import datetime

class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.script_dir, '../data/raw')
    
    def test_source(self, sector, source_name):
        """测试单个新闻源"""
        date_str = datetime.now().strftime('%Y%m%d')
        file_path = os.path.join(self.data_dir, f'{sector}_{source_name}_{date_str}.json')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                news_list = json.load(f)
                return len(news_list), True
        return 0, False
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("新闻聚合系统测试报告")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        sectors = ['healthcare', 'education']
        sector_names = {'healthcare': '医疗健康', 'education': '教育人才'}
        sources = ['google', 'rss', 'rolling', 'aggregated']
        
        for sector in sectors:
            print(f"\n【{sector_names[sector]}板块】")
            
            total = 0
            for source in sources:
                count, ok = self.test_source(sector, source)
                status = '✅' if ok else '❌'
                print(f"  {source.capitalize()}: {status} {count}条")
                if source != 'aggregated':
                    total += count
            
            agg_count, _ = self.test_source(sector, 'aggregated')
            if agg_count > 0:
                print(f"  去重率: {((total - agg_count) / total * 100):.1f}%")

if __name__ == '__main__':
    generator = TestReportGenerator()
    generator.generate_report()
