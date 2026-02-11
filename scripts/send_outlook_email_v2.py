#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Outlook SMTP发送邮件 - SSL版本
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_outlook_email_ssl(to_email, csv_file, app_password):
    """通过Outlook SMTP发送邮件（使用SSL）"""
    
    # Outlook SMTP配置 - 使用SSL
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    from_email = to_email
    
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
2026-02-10 10:00
"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
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
    
    # 尝试多种配置
    configs = [
        ("smtp-mail.outlook.com", 587, "TLS"),
        ("smtp.office365.com", 587, "TLS"),
        ("smtp-mail.outlook.com", 25, "TLS"),
    ]
    
    for server, port, method in configs:
        try:
            print(f"\n📧 尝试: {server}:{port} ({method})")
            smtp = smtplib.SMTP(server, port, timeout=10)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            print(f"🔐 登录: {from_email}")
            smtp.login(from_email, app_password)
            print(f"📤 发送邮件...")
            smtp.send_message(msg)
            smtp.quit()
            print(f"✅ 邮件发送成功！")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            continue
    
    print(f"\n❌ 所有配置都失败")
    return False

if __name__ == '__main__':
    csv_file = '/root/clawd/news-workflow/data/raw/strategic_emerging_20260210.csv'
    to_email = 'Guqie1@outlook.com'
    app_password = 'qfupedqtbwsxckwi'
    
    send_outlook_email_ssl(to_email, csv_file, app_password)
