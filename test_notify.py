#!/usr/bin/env python3
# 测试邮件通知功能

import json
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from notify_mail import format_email_content, send_email

def test_email_config():
    """测试邮件配置是否正确"""
    print("=== 测试邮件配置 ===\n")
    
    from notify_mail import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, TO_EMAIL
    
    print(f"SMTP服务器: {SMTP_SERVER}")
    print(f"SMTP端口: {SMTP_PORT}")
    print(f"发件人: {EMAIL_USER}")
    print(f"收件人: {TO_EMAIL}")
    print(f"密码已配置: {'是' if EMAIL_PASSWORD else '否'}\n")
    
    if not all([EMAIL_USER, EMAIL_PASSWORD, TO_EMAIL]):
        print("[错误] 环境变量配置不完整！")
        print("请检查 .env 文件，确保以下变量都已配置：")
        print("  - EMAIL_USER")
        print("  - EMAIL_PASSWORD")
        print("  - TO_EMAIL")
        return False
    
    print("[成功] 环境变量配置完整\n")
    return True

def test_email_send():
    """测试发送邮件"""
    print("=== 测试发送邮件 ===\n")
    
    # 模拟 Codex 的 payload
    test_payload = {
        "type": "agent-turn-complete",
        "input-messages": [
            "## My request for Codex:\n测试邮件通知功能"
        ],
        "last-assistant-message": "已完成测试邮件通知功能的配置和验证\n"
    }
    
    # 格式化邮件内容
    subject, body = format_email_content(test_payload)
    
    print("邮件主题:")
    print(f"  {subject}\n")
    print("邮件内容:")
    print("─" * 50)
    print(body)
    print("─" * 50)
    print()
    
    # 询问是否发送测试邮件
    response = input("是否发送测试邮件？(y/n): ").strip().lower()
    
    if response == 'y':
        print("\n正在发送测试邮件...")
        if send_email(subject, body):
            print("[成功] 测试邮件发送成功！请检查收件箱。")
            return True
        else:
            print("[失败] 测试邮件发送失败，请检查配置和网络连接。")
            return False
    else:
        print("已取消发送测试邮件。")
        return None

def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("Codex 邮件通知测试工具")
    print("=" * 60 + "\n")
    
    # 检查 .env 文件是否存在
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("[错误] .env 文件不存在！\n")
        print("请先创建 .env 文件：")
        print("  1. 复制 env.example 为 .env")
        print("  2. 编辑 .env 文件，填入实际的邮箱配置\n")
        print("Windows 命令:")
        print("  copy env.example .env\n")
        print("Linux 命令:")
        print("  cp env.example .env\n")
        return 1
    
    print("[成功] 找到 .env 配置文件\n")
    
    # 测试配置
    if not test_email_config():
        return 1
    
    # 测试发送
    result = test_email_send()
    
    print("\n" + "=" * 60)
    if result is True:
        print("[成功] 所有测试通过！邮件通知功能正常。")
    elif result is False:
        print("[失败] 测试失败，请检查配置和错误信息。")
    else:
        print("测试已取消。")
    print("=" * 60 + "\n")
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())

