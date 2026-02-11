#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送新闻CSV邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

def send_email_with_attachment(to_email, csv_file, summary):
    """发送带附件的邮件"""
    
    # 邮件配置（需要配置SMTP服务器）
    from_email = "clawdbot@example.com"  # 需要配置
    smtp_server = "smtp.example.com"      # 需要配置
    smtp_port = 587
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f'战略新兴产业新闻采集报告 - {datetime.now().strftime("%Y-%m-%d")}'
    
    # 邮件正文
    body = f"""
您好，

今日战略新兴产业新闻采集已完成，详情如下：

{summary}

新闻详情请查看附件CSV文件。

---
Clawdbot 自动发送
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    if os.path.exists(csv_file):
        with open(csv_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
                          f'attachment; filename={os.path.basename(csv_file)}')
            msg.attach(part)
    
    print(f"📧 准备发送邮件到: {to_email}")
    print(f"📎 附件: {csv_file}")
    
    # 注意：需要配置SMTP服务器才能发送
    print("⚠️  需要配置SMTP服务器")
    
    return msg

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("用法: python3 send_email.py <to_email> <csv_file> <summary>")
        sys.exit(1)
    
    send_email_with_attachment(sys.argv[1], sys.argv[2], sys.argv[3])
