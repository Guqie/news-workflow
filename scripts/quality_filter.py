#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量筛选模块 - 基于规则的新闻质量筛选
"""

import json
import os

class QualityFilter:
    """质量筛选器"""
    
    def __init__(self, config_path=None):
        """初始化质量筛选器"""
        if config_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(os.path.dirname(script_dir), 'config', 'quality_rules.json')
        
        self.load_rules(config_path)
    
    def load_rules(self, config_path):
        """从配置文件加载规则"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.soft_ad_keywords = config.get('软文特征词', [])
        self.clickbait_keywords = config.get('标题党特征词', [])
        self.quality_thresholds = config.get('低质量特征', {})
        self.exclude_sources = config.get('排除来源', [])
    
    def check_soft_ad(self, title):
        """检测软文特征"""
        for keyword in self.soft_ad_keywords:
            if keyword in title:
                return True, f"包含软文特征词: {keyword}"
        return False, None
    
    def check_clickbait(self, title):
        """检测标题党特征"""
        for keyword in self.clickbait_keywords:
            if keyword in title:
                return True, f"包含标题党特征词: {keyword}"
        return False, None
    
    def check_quality(self, news_item):
        """检测内容质量"""
        title = news_item.get('title', '')
        content = news_item.get('content', '')
        
        # 检查标题长度
        if len(title) > self.quality_thresholds.get('标题过长', 80):
            return False, f"标题过长({len(title)}字)"
        
        if len(title) < self.quality_thresholds.get('标题过短', 10):
            return False, f"标题过短({len(title)}字)"
        
        # 检查内容长度
        if content and len(content) < self.quality_thresholds.get('内容过短', 100):
            return False, f"内容过短({len(content)}字)"
        
        # 检查感叹号数量
        exclamation_count = title.count('!') + title.count('！')
        if exclamation_count > self.quality_thresholds.get('感叹号过多', 3):
            return False, f"感叹号过多({exclamation_count}个)"
        
        return True, None
    
    def filter_news(self, news_item):
        """
        筛选单条新闻
        
        Returns:
            (bool, str): (是否保留, 原因)
        """
        title = news_item.get('title', '')
        
        # 检查软文
        is_soft_ad, reason = self.check_soft_ad(title)
        if is_soft_ad:
            return False, reason
        
        # 检查标题党
        is_clickbait, reason = self.check_clickbait(title)
        if is_clickbait:
            return False, reason
        
        # 检查质量
        is_quality, reason = self.check_quality(news_item)
        if not is_quality:
            return False, reason
        
        return True, "通过质量检查"
    
    def filter_news_list(self, news_list):
        """批量筛选新闻"""
        filtered = []
        stats = {
            'total': len(news_list),
            'kept': 0,
            'soft_ad': 0,
            'clickbait': 0,
            'low_quality': 0
        }
        
        for news in news_list:
            keep, reason = self.filter_news(news)
            if keep:
                filtered.append(news)
                stats['kept'] += 1
            else:
                if '软文' in reason:
                    stats['soft_ad'] += 1
                elif '标题党' in reason:
                    stats['clickbait'] += 1
                else:
                    stats['low_quality'] += 1
        
        print(f"\n质量筛选结果:")
        print(f"  原始数量: {stats['total']}")
        print(f"  保留: {stats['kept']}")
        print(f"  排除-软文: {stats['soft_ad']}")
        print(f"  排除-标题党: {stats['clickbait']}")
        print(f"  排除-低质量: {stats['low_quality']}")
        
        return filtered, stats
