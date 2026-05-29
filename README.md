# 🌤️ 天气机器人 (Weather Robot)

一个通过企业微信每天早上6点自动推送天气消息的聊天机器人。

## 功能特性

- 🌡️ 实时获取天气数据（温度、湿度、风力等）
- 👔 根据温度给出穿着建议
- ☂️ 降雨概率提醒带伞
- 💬 每日随机人性化吐槽
- ⏰ 每天早上6点自动推送
- 📱 企业微信消息推送

## 技术栈

- Python 3.8+
- requests - HTTP请求
- APScheduler - 定时任务
- 和风天气API - 天气数据
- 企业微信应用消息API - 消息推送

## 云端部署 (GitHub Actions)

项目支持通过 GitHub Actions 实现 24/7 自动运行，无需保持电脑开启。

### 配置步骤

1. 将项目上传至你的 GitHub 私有仓库（**强烈建议使用私有仓库**以保护配置）。
2. 在 GitHub 仓库页面，点击 `Settings` -> `Secrets and variables` -> `Actions`。
3. 点击 `New repository secret`，依次添加以下 Secrets（名称必须完全一致）：
   - `HEFENG_API_KEY`
   - `HEFENG_API_HOST`
   - `WECOM_CORP_ID`
   - `WECOM_AGENT_ID`
   - `WECOM_APP_SECRET`
   - `WECOM_TO_USER`
   - `WECOM_TOKEN`
   - `WECOM_ENCODING_AES_KEY`
   - `WECOM_WEBHOOK_URL` (推荐，解决 IP 限制问题)
   - `CITY` (可选，默认为上海)
4. 工作流会自动在每天北京时间 06:00 运行。你也可以在 `Actions` 页面手动点击 `Run workflow` 进行测试。

---

## 快速开始

### 1. 创建conda环境

```bash
conda create -n weatherrobot python=3.8
conda activate weatherrobot
pip install -r requirements.txt
```

### 2. 配置 API 密钥

项目使用 `.env` 文件管理敏感配置。

1. 复制模板文件：
   ```bash
   cp .env.example .env
   ```
2. 在 `.env` 中填入你的配置信息：

```ini
# 和风天气API
HEFENG_API_KEY=你的API_KEY
HEFENG_API_HOST=你的API_HOST

# 企业微信应用消息API
WECOM_CORP_ID=企业ID
WECOM_AGENT_ID=应用AgentID
WECOM_APP_SECRET=应用Secret
WECOM_TO_USER=接收消息的用户ID
WECOM_TOKEN=回调验证Token
WECOM_ENCODING_AES_KEY=回调验证AESKey
```

> ⚠️ **安全警告**: 请勿将 `.env` 文件提交到公共 Git 仓库。项目已配置 `.gitignore` 自动忽略该文件。

### 3. 启动定时任务

```bash
conda activate weatherrobot
python main.py
```

程序会在每天早上6:00自动发送天气消息到你的企业微信。

## 消息示例

```
☀️ 上海今日天气（2026年05月29日 周五）

早起的鸟儿有虫吃，早起的你有天气看！

🌡️ 气温：26°C（今日高温29°C，低温19°C，体感温度26°C）
💧 湿度：40%
🌬️ 风力：东风2级
🌤️ 天气状况：阴

👔 穿着建议：温度刚刚好！穿件短袖或者薄外套就很舒服啦～

🌧️ 降雨概率：0%，放心出门，应该不会下雨，不用带伞啦～

💬 太阳公公今天是吃了火药吗？出门五分钟，流汗两小时！
```

## 项目结构

```
weather-robot/
├── config.py              # 配置文件
├── weather_service.py     # 天气服务（和风天气API）
├── message_generator.py   # 消息生成器
├── wechat_client.py       # 企业微信推送
├── scheduler.py           # 定时调度器
├── main.py                # 主入口
├── callback_server.py     # 企业微信回调验证服务器
├── requirements.txt       # 依赖包
└── cloudflared.exe        # Cloudflare Tunnel工具
```

## 企业微信配置

1. 登录 https://work.weixin.qq.com/
2. 进入「管理后台」→「应用管理」→ 创建自建应用
3. 获取以下信息：
   - 企业ID (CorpID)
   - 应用AgentID
   - 应用Secret
4. 配置「接收消息服务器URL」（用于验证）
5. 添加「企业可信IP」（用于发送消息）

### 配置回调服务器（首次配置时需要）

```bash
# 启动回调服务器
python callback_server.py

# 启动Cloudflare Tunnel（另一个终端）
.\cloudflared.exe tunnel --url http://localhost:8066
```

将生成的URL填入企业微信的「接收消息服务器URL」。

## 获取API密钥

### 和风天气
1. 访问 https://dev.qweather.com/
2. 注册账号并创建应用
3. 获取API Key和API Host

### 企业微信
1. 访问 https://work.weixin.qq.com/
2. 注册企业并创建自建应用
3. 获取CorpID、AgentID和Secret

## 注意事项

- 公网IP可能会变化，IP变化后需要重新设置企业可信IP
- 回调服务器需要保持运行以维持企业微信配置
- 建议使用云服务器进行长期稳定运行

## 开发

```bash
# 手动发送一次天气消息（测试用）
python -c "
from weather_service import weather_service
from message_generator import message_generator
from wechat_client import wechat_client

weather_data = weather_service.get_weather()
forecast_data = weather_service.get_daily_forecast()
message = message_generator.generate(weather_data, forecast_data)
wechat_client.send_message(message)
print('发送成功！')
"
```

## License

MIT
