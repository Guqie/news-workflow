#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过邮件发送CSV附件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_csv(to_email, csv_file):
    """发送带CSV附件的邮件"""
    
    # 邮件内容
    subject = "战略新兴产业新闻采集报告 - 2026-02-10"
    
    body = """战略新兴产业新闻采集报告

采集日期：2026-02-10
采集时间：09:30-09:35

一、采集结果统计
- 原始新闻数：228条
- 去重后：223条
- 去重率：2.2%

二、关键词使用情况
• 战略新兴产业 - 41条
• 新能源 - 100条
• 新材料 - 45条
• 数字经济 - 42条

三、新闻来源
政府网站、主流媒体、专业媒体

四、热点话题 Top 5
1. 山东战新产业集群全国第一
2. 深圳新兴产业占GDP达43%
3. 央企转型投资
4. 产业基金布局
5. 四川国资国企发展

详细数据请查看附件CSV文件。

---
Clawdbot 自动发送
2026-02-10 09:40
"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = to_email
    
    # 添加正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加CSV附件
    if os.path.exists(csv_file):
        with open(csv_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(csv_file)
            part.add_header('Content-Disposition', 
                          f'attachment; filename="{filename}"')
            msg.attach(part)
        print(f"✅ 附件已添加: {filename}")
    else:
        print(f"❌ 文件不存在: {csv_file}")
        return False
    
    # 使用本地sendmail发送
    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
        print(f"✅ 邮件已发送到: {to_email}")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == '__main__':
    csv_file = '/root/clawd/news-workflow/data/raw/strategic_emerging_20260210.csv'
    to_email = 'Guqie1@outlook.com'
    send_email_with_csv(to_email, csv_file)
