# Codex 邮件通知配置

这是一个用于 Codex 完成任务后发送邮件通知的脚本。当 Codex 完成一个回合的任务时，自动发送邮件通知到指定邮箱。

## 功能特点

- 自动提取 Codex 任务请求和执行结果
- 支持 Windows 和 Linux 系统
- 邮件内容包含机器信息、时间戳和执行摘要
- 使用环境变量安全管理邮箱凭据

## 系统要求

- Python 3.10+
- 有效的 SMTP 邮箱账户（QQ 邮箱、Gmail、163 等）

## 安装配置

### 步骤 1: 克隆或下载此项目

将项目文件放置在合适的位置，例如：
- Windows: `C:\Users\<用户名>\.codex\`
- Linux: `~/.codex/`

### 步骤 2: 安装 Python 依赖

本项目支持两种依赖管理方式：

#### 方式 1: 使用 uv（推荐）

[uv](https://github.com/astral-sh/uv) 是一个快速的 Python 包管理器，推荐使用。

**安装 uv：**

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**安装项目依赖：**

```bash
uv sync
```

这会自动创建虚拟环境并安装所有依赖。

#### 方式 2: 使用传统 pip

```bash
pip install -r requirements.txt
```

### 步骤 3: 配置邮件环境变量

复制示例配置文件并编辑：

**Windows (PowerShell):**
```powershell
copy env.example .env
```

**Linux (Bash):**
```bash
cp env.example .env
```

编辑 `.env` 文件，填入实际的邮件配置信息：

```
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
EMAIL_USER=你的QQ号@qq.com
EMAIL_PASSWORD=你的QQ邮箱授权码
TO_EMAIL=接收通知的邮箱@example.com
```

### 步骤 4: 获取邮箱授权码

#### QQ邮箱授权码获取方法

QQ邮箱需要使用授权码，而不是QQ密码：

1. 登录 QQ 邮箱网页版 (mail.qq.com)
2. 点击顶部「设置」->「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」部分
4. 开启「IMAP/SMTP服务」（推荐）或「POP3/SMTP服务」
5. 按照提示发送短信验证
6. 生成授权码后，复制并填入 `.env` 文件的 `EMAIL_PASSWORD` 字段

注意：授权码只显示一次，请妥善保存。

#### 其他邮箱服务器配置

常见邮箱的 SMTP 配置：

- **Gmail**: `smtp.gmail.com` (端口 587) - 需要应用专用密码
- **163邮箱**: `smtp.163.com` (端口 465 或 25) - 需要授权码
- **Outlook**: `smtp-mail.outlook.com` (端口 587) - 使用账户密码

### 步骤 5: 配置 Codex

编辑 Codex 的配置文件 `config.toml`：

**Windows 系统：**
配置文件位置：`C:\Users\<用户名>\.codex\config.toml`

```toml
model = "gpt-5.1-codex-max"

# 配置邮件通知（注意：notify 必须在最顶层，不能在任何 [section] 下面）

# 方式 1: 使用 uv run（推荐，需要指定项目目录）
notify = ["uv", "run", "--directory", "C:\\Users\\<用户名>\\.codex", "notify_mail.py"]

# 方式 2: 使用 uv 创建的虚拟环境中的 Python（最可靠）
# 先运行 uv sync，然后使用虚拟环境的 Python
# notify = ["C:\\Users\\<用户名>\\.codex\\.venv\\Scripts\\python.exe", "C:\\Users\\<用户名>\\.codex\\notify_mail.py"]

# 方式 3: 使用传统 Python 命令
# notify = ["python", "C:\\Users\\<用户名>\\.codex\\notify_mail.py"]

[history]
persistence = "save-all"

[tui]
notifications = ["agent-turn-complete"]
```

**Linux 系统：**
配置文件位置：`~/.codex/config.toml`

```toml
model = "gpt-5.1-codex-max"

# 配置邮件通知（注意：notify 必须在最顶层，不能在任何 [section] 下面）

# 使用 uv run
notify = ["uv", "run", "--directory", "/home/<用户名>/.codex", "notify_mail.py"]


[history]
persistence = "save-all"

[tui]
notifications = ["agent-turn-complete"]
```



## 测试配置

### 手动测试

在配置完成后，可以手动测试脚本是否能正常发送邮件：

**使用 uv（推荐）：**
```bash
uv run test_notify.py
```


如果配置正确，你应该能收到一封测试邮件。

### 测试 Codex 集成

启动 Codex 并给它一个简单的任务：

```
请帮我创建一个简单的 Python 函数，实现两数相加
```

当 Codex 完成任务后，你应该会收到邮件通知。

## 邮件内容说明

收到的邮件会包含以下信息：

- **邮件主题**: `Codex任务完成 - <系统名称>`
- **任务请求**: 你发送给 Codex 的原始请求
- **机器信息**: 运行 Codex 的机器名称和操作系统
- **时间戳**: 任务完成的时间
- **执行结果**: Codex 的回复摘要（最多显示前 3 个要点）


## 高级配置

### 自定义邮件格式

你可以编辑 `notify_mail.py` 中的 `format_email_content` 函数来自定义邮件内容：

- 修改邮件主题格式
- 调整显示的要点数量（默认 3 个）
- 添加更多机器信息
- 修改文本截断长度

### 支持多个收件人

在 `.env` 文件中，`TO_EMAIL` 可以使用逗号分隔多个邮箱：

```
TO_EMAIL=email1@example.com,email2@example.com
```

然后修改 `notify_mail.py` 第 114 行：

```python
msg['To'] = TO_EMAIL  # 保持不变，SMTP 会自动处理
```

### 使用其他通知方式

参考官方教程了解更多通知方式：
- Linux 桌面通知：使用 `notify-send`
- Windows Toast 通知：使用 `win10toast` 模块
- 企业微信、钉钉等 Webhook 通知

参考链接：https://kanman.de/en/posts/codex-desktop-notifications/

## 安全提示

- `.env` 文件包含敏感信息，已被添加到 `.gitignore` 中
- 请勿将 `.env` 文件提交到版本控制系统
- 如需分享配置，请使用 `env.example` 文件
- 定期更换邮箱授权码以保障安全

## 文件说明

- `notify_mail.py` - 主脚本，处理 Codex 通知并发送邮件
- `test_notify.py` - 测试脚本，验证邮件配置
- `.env` - 环境变量配置文件（需手动创建）
- `env.example` - 环境变量配置示例
- `pyproject.toml` - 项目配置文件（uv 使用）

## 快速开始（使用 uv）

如果你使用 uv 包管理器，只需以下几步：

```bash
# 1. 进入项目目录
cd ~/.codex  # Linux
# 或 cd C:\Users\<用户名>\.codex  # Windows

# 2. 安装依赖（会创建 .venv 虚拟环境）
uv sync

# 3. 复制并配置环境变量
cp env.example .env  # Linux
# 或 copy env.example .env  # Windows

# 4. 编辑 .env 文件，填入邮箱配置

# 5. 测试配置
uv run test_notify.py

# 6. 从其他目录测试（验证跨目录调用）
cd /tmp
uv run --directory ~/.codex test_notify.py
# 或使用虚拟环境 Python
~/.codex/.venv/bin/python ~/.codex/test_notify.py

# 7. 在 config.toml 中配置 notify
# 推荐使用方式 1（--directory）或方式 2（.venv Python）
```

**uv sync 创建的虚拟环境位置：**
- Linux: `~/.codex/.venv/bin/python`
- Windows: `C:\Users\<用户名>\.codex\.venv\Scripts\python.exe`

## 许可证

本项目代码可自由使用和修改。

## 参考资料

- [Codex 桌面通知官方教程](https://kanman.de/en/posts/codex-desktop-notifications/)
- [Codex 官方文档](https://docs.codex.ai/)

