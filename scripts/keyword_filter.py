#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词筛选模块 - 基于关键词的新闻筛选
"""

import json
import os

class KeywordFilter:
    """关键词筛选器"""
    
    def __init__(self, config_path=None):
        """
        初始化关键词筛选器
        
        Args:
            config_path: 关键词配置文件路径，默认为config/keywords_config.json
        """
        if config_path is None:
            # 默认配置文件路径
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(os.path.dirname(script_dir), 'config', 'keywords_config.json')
        
        # 从配置文件加载关键词
        self.load_keywords(config_path)
    
    def load_keywords(self, config_path):
        """从配置文件加载关键词"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.exclude_keywords = config.get('exclude_keywords', [])
        self.exclude_domains = config.get('exclude_domains', [])
        
        # 处理include_keywords，支持分类结构
        include_kw = config.get('include_keywords', [])
        if isinstance(include_kw, dict):
            # 如果是字典（分类结构），展平为列表
            self.include_keywords = []
            for category, keywords in include_kw.items():
                self.include_keywords.extend(keywords)
        else:
            # 如果是列表，直接使用
            self.include_keywords = include_kw
    
    def should_exclude(self, title):
        """判断是否应该排除"""
        title_lower = title.lower()
        
        # 检查排除关键词
        for keyword in self.exclude_keywords:
            if keyword in title_lower:
                return True, f"包含排除关键词: {keyword}"
        
        # 检查排除领域
        for domain in self.exclude_domains:
            if domain in title:
                return True, f"属于排除领域: {domain}"
        
        return False, None
    
    def should_include(self, title):
        """判断是否应该包含"""
        title_lower = title.lower()
        
        # 检查必须包含关键词
        for keyword in self.include_keywords:
            if keyword.lower() in title_lower:
                return True, f"匹配关键词: {keyword}"
        
        return False, None
    
    def filter_news(self, news_item):
        """
        筛选单条新闻
        
        Returns:
            (bool, str): (是否保留, 原因)
        """
        title = news_item.get('title', '')
        
        # 第一步：检查是否应该排除
        should_excl, excl_reason = self.should_exclude(title)
        if should_excl:
            return False, excl_reason
        
        # 第二步：检查是否应该包含
        should_incl, incl_reason = self.should_include(title)
        if should_incl:
            return True, incl_reason
        
        # 不匹配任何关键词，排除
        return False, "未匹配任何关键词"
    
    def filter_news_list(self, news_list):
        """批量筛选新闻"""
        filtered = []
        stats = {
            'total': len(news_list),
            'kept': 0,
            'excluded_keywords': 0,
            'excluded_domains': 0,
            'no_match': 0
        }
        
        for news in news_list:
            keep, reason = self.filter_news(news)
            if keep:
                filtered.append(news)
                stats['kept'] += 1
            else:
                if '排除关键词' in reason:
                    stats['excluded_keywords'] += 1
                elif '排除领域' in reason:
                    stats['excluded_domains'] += 1
                else:
                    stats['no_match'] += 1
        
        print(f"\n关键词筛选结果:")
        print(f"  原始数量: {stats['total']}")
        print(f"  保留: {stats['kept']}")
        print(f"  排除-股票类: {stats['excluded_keywords']}")
        print(f"  排除-领域: {stats['excluded_domains']}")
        print(f"  排除-无关: {stats['no_match']}")
        
        return filtered, stats
