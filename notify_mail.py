#!/usr/bin/env python3
# 文件名：~/.codex/notify_mail.py (Linux) 或 C:\Users\<user>\.codex\notify_mail.py (Windows)

import json
import re
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 从环境变量读取邮件配置
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def trunc(text, limit):
    """截断文本，在单词边界处截断"""
    if len(text) <= limit:
        return text
    cut = max(0, limit - 3)
    head = text[:cut]
    # 回退到最后一个空格，避免截断单词
    last_space = head.rfind(' ')
    if last_space > 0:
        head = head[:last_space]
    return head + "..."

def get_machine_info():
    """获取机器信息"""
    import platform
    import socket
    
    system = platform.system()
    hostname = socket.gethostname()
    if system == "Linux":
        return f"Ubuntu ({hostname})"
    elif system == "Windows":
        return f"Windows ({hostname})"
    else:
        return f"{system} ({hostname})"

def format_email_content(payload):
    """格式化邮件内容"""
    machine = get_machine_info()
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 提取请求内容
    input_messages = payload.get("input-messages", [])
    last_request = ""
    
    for msg in input_messages:
        if "## My request for Codex:" in msg:
            # 提取用户请求部分
            lines = msg.split("\n")
            capture = False
            request_lines = []
            
            for line in lines:
                if capture:
                    # 继续捕获，直到遇到新的 ## 标记或空白部分
                    stripped = line.strip()
                    if stripped:
                        if not stripped.startswith("## "):
                            request_lines.append(stripped)
                        else:
                            break  # 遇到新的标记，停止捕获
                elif "## My request for Codex:" in line:
                    capture = True
                    # 如果同一行有内容，也提取
                    after_marker = line.split("## My request for Codex:", 1)[1].strip()
                    if after_marker:
                        request_lines.append(after_marker)
            
            if request_lines:
                last_request = " ".join(request_lines)
                break
    
    # 提取助手回复
    assistant_msg = payload.get("last-assistant-message", "") or payload.get("last_assistant_message", "")
    
    # 如果有项目符号，只取前几个
    bullets = []
    for line in assistant_msg.split("\n"):
        if re.match(r'^\s*[-*]\s+', line):
            bullets.append(line.strip())
            if len(bullets) >= 3:  # 最多显示3个要点
                break
    
    # 构建邮件内容
    subject = f"Codex任务完成 - {machine}"
    
    body = f"""
任务请求: {trunc(last_request or "无具体请求信息", 200)}
机器: {machine}
时间: {request_time}

===== 执行结果 =====
"""
    
    if bullets:
        body += "\n".join(bullets) + "\n"
    else:
        body += trunc(assistant_msg, 300) + "\n"
    
    
    return subject, body

def send_email(subject, body):
    """发送邮件"""
    # 验证必要的环境变量
    if not all([EMAIL_USER, EMAIL_PASSWORD, TO_EMAIL]):
        print("错误: 缺少必要的环境变量 (EMAIL_USER, EMAIL_PASSWORD, TO_EMAIL)")
        print("请在 .env 文件中配置邮件信息")
        return False
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # 发送邮件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"邮件已发送: {subject}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        return 0
    
    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 0
    
    # 只处理agent-turn-complete类型
    if payload.get("type") != "agent-turn-complete":
        return 0
    
    # 格式化邮件内容
    subject, body = format_email_content(payload)
    
    # 发送邮件
    if send_email(subject, body):
        return 0
    else:
        # 发送失败，可以尝试备用方案或记录日志
        return 1

if __name__ == "__main__":
    sys.exit(main())