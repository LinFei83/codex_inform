# Codex 邮件通知配置

这是一个用于 Codex 完成任务后发送邮件通知的脚本。

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制示例配置文件并编辑：

```bash
# 将 env.example 复制为 .env
copy env.example .env
```

编辑 `.env` 文件，填入实际的邮件配置信息：

```
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
EMAIL_USER=你的QQ号@qq.com
EMAIL_PASSWORD=你的QQ邮箱授权码
TO_EMAIL=接收通知的邮箱@example.com
```

### 3. QQ邮箱授权码获取方法

QQ邮箱需要使用授权码，而不是QQ密码：

1. 登录 QQ 邮箱网页版 (mail.qq.com)
2. 点击顶部「设置」->「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」部分
4. 开启「IMAP/SMTP服务」（推荐）或「POP3/SMTP服务」
5. 按照提示发送短信验证
6. 生成授权码后，复制并填入 `.env` 文件的 `EMAIL_PASSWORD` 字段

注意：授权码只显示一次，请妥善保存。

### 4. 其他邮箱服务器配置

常见邮箱的 SMTP 配置：

- **Gmail**: `smtp.gmail.com` (端口 587) - 需要应用专用密码
- **163邮箱**: `smtp.163.com` (端口 465 或 25) - 需要授权码
- **Outlook**: `smtp-mail.outlook.com` (端口 587) - 使用账户密码

## 使用方法

脚本会在 Codex 完成任务时自动调用，发送邮件通知。

## 安全提示

- `.env` 文件包含敏感信息，已被添加到 `.gitignore` 中
- 请勿将 `.env` 文件提交到版本控制系统
- 如需分享配置，请使用 `env.example` 文件

