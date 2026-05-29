# 🌤️ 天气机器人 (Weather Robot)

一个通过企业微信每天定时推送天气消息的智能助手。支持多城市推送、GitHub Actions 云端部署。

## 功能特性

- 🌡️ **精准数据**：实时获取温度、湿度、风力及天气状况。
- 👗 **穿着建议**：根据实时温度自动推荐今日穿搭。
- ☔ **带伞提醒**：分析降雨概率，提前预警。
- 🏙️ **多城推送**：支持同时配置多个城市（如上海、宁波）。
- 💬 **趣味吐槽**：内置随机吐槽，让天气预报不再枯燥。
- ☁️ **云端运行**：支持 GitHub Actions，零成本 24/7 自动运行。

## 技术栈

- Python 3.11+
- [和风天气 API](https://dev.qweather.com/) - 专业天气数据源
- 企业微信群机器人/自建应用 - 消息推送通道
- GitHub Actions - 自动化调度

---

## 云端部署 (GitHub Actions) - 推荐方案

使用 GitHub Actions 可以在不保持电脑开启的情况下，每天免费、稳定地接收推送。

### 配置步骤

1. 将本项目上传至你的 GitHub **私有仓库**。
2. 在仓库页面点击 `Settings` -> `Secrets and variables` -> `Actions`。
3. 点击 `New repository secret`，依次添加以下环境变量：

| Secret Name | 说明 | 示例值 |
| :--- | :--- | :--- |
| `HEFENG_API_KEY` | 和风天气 API Key | `2a27458f...` |
| `WECOM_WEBHOOK_URL` | **推荐**：企业微信群机器人 Webhook 地址 | `https://qyapi.weixin.qq.com/...` |
| `CITY` | 推送城市，多个用逗号隔开 | `上海,宁波` |
| `HEFENG_API_HOST` | 和风天气 API Host | `n94nmv63jv.re.qweatherapi.com` |
| `WECOM_CORP_ID` | 企业微信 CorpID (可选) | `wwf3c...` |
| `WECOM_APP_SECRET` | 企业微信应用 Secret (可选) | `KVj_6...` |

4. **激活工作流**：在 `Actions` 选项卡选择 `Daily Weather Robot`，手动点击 `Run workflow` 测试。

> 💡 **为什么推荐 Webhook？** GitHub 服务器 IP 经常变化。使用群机器人 Webhook 可以绕过企业微信自建应用的“可信 IP”限制，实现零维护运行。

---

## 本地快速开始

### 1. 环境准备
```bash
conda create -n weatherrobot python=3.11
conda activate weatherrobot
pip install -r requirements.txt
```

### 2. 密钥配置
复制 `.env.example` 为 `.env` 并填写相关信息：
```ini
HEFENG_API_KEY=你的和风天气KEY
WECOM_WEBHOOK_URL=你的群机器人链接
CITY=上海,宁波
```

### 3. 运行
```bash
python main.py  # 启动长期调度任务
# 或
python run_once.py  # 立即发送一次进行测试
```

---

## 运行成本说明 (FAQ)

- **GitHub Actions 收费吗？**
  对于私有仓库，GitHub 每个月提供 2,000 分钟免费额度。本项目每天运行 1 分钟，每月仅需 30 分钟，**完全免费**。
- **API 收费吗？**
  和风天气免费版每日提供 1,000 次请求，企业微信推送目前也是免费的，足以满足个人使用。
- **如何增加城市？**
  在配置中的 `CITY` 字段添加城市名即可，例如 `CITY=上海,宁波,杭州`。代码已内置相关城市代码映射。

---

## 项目结构
- [weather_service.py](file:///e:/agent%20project/weather-robot/weather_service.py): 对接和风天气 API。
- [message_generator.py](file:///e:/agent%20project/weather-robot/message_generator.py): 构建人性化的天气文案。
- [wechat_client.py](file:///e:/agent%20project/weather-robot/wechat_client.py): 封装企业微信发送逻辑。
- [scheduler.py](file:///e:/agent%20project/weather-robot/scheduler.py): 处理多城市循环推送及定时逻辑。

## License
MIT
