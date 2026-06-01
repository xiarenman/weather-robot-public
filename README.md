# 🌤️ 天气机器人 (Weather Robot)

一个通过企业微信每天定时推送天气消息的智能助手。支持多城市推送、GitHub Actions 云端部署，**零基础用户也可在 5 分钟内完成部署**。

## 🌟 功能特性

- 🌡️ **精准数据**：实时获取温度、湿度、风力及天气状况。
- 👗 **穿着建议**：根据实时温度自动推荐今日穿搭。
- ☔ **带伞提醒**：分析降雨概率，提前预警。
- 🏙️ **全国通**：支持全国任何县级及以上城市推送（如：上海,宁波,义乌）。
- 💬 **趣味吐槽**：内置随机吐槽，让天气预报不再枯燥。
- ☁️ **零成本云运行**：使用 GitHub Actions，无需电脑开机，完全免费。

---

## 🚀 零代码部署教程 (推荐)

你不需要下载任何代码，直接在 GitHub 网页上即可完成部署。

### 第一步：准备 API 密钥
1. **和风天气**: 访问 [和风天气开发平台](https://dev.qweather.com/)，注册并创建一个项目，获取 `API Key`。
2. **企业微信机器人**: 
   - 在企业微信群中，点击「添加机器人」->「新创建一个机器人」。
   - 复制机器人的 `Webhook 地址`。

### 第二步：导入项目到你的私有仓库
1. 在本页面右上角点击 **Use this template** (如果有) 或直接 **Fork** 本仓库。
2. **强烈建议**：在 Fork 页面勾选 **Copy the master branch only**。
3. 为了保护隐私，你可以创建一个新的**私有仓库 (Private Repository)**，然后通过 GitHub 的 `Import repository` 功能将本仓库地址导入。

### 第三步：配置 GitHub Secrets
1. 在你的仓库页面，点击顶部菜单的 **Settings**。
2. 在左侧菜单找到 **Secrets and variables** -> **Actions**。
3. 点击 **New repository secret**，依次添加以下三个核心变量：

| Name (名称) | Value (值) |
| :--- | :--- |
| `HEFENG_API_KEY` | 填入你的和风天气 API Key |
| `WECOM_WEBHOOK_URL` | 填入你的企业微信机器人 Webhook 地址（支持多个，逗号隔开） |
| `CITY` | 填入城市名，多个用逗号隔开 (如：上海,宁波) |

### 第四步：启动机器人
1. 点击仓库顶部的 **Actions** 选项卡。
2. 在左侧选择 **Daily Weather Robot**。
3. 如果页面显示 `Workflows aren't run...`，点击绿色按钮 **Enable Actions**。
4. 点击右侧的 **Run workflow** -> **Run workflow** 绿色按钮手动测试一次。
5. **大功告成！** 机器人现在会每天北京时间早上 06:00 准时给你发消息。

---

## 🛠️ 进阶：本地运行

如果你想在本地运行或二次开发：

1. **克隆代码**：
   ```bash
   git clone https://github.com/your-username/weather-robot.git
   cd weather-robot
   ```
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
3. **配置文件**：
   复制 `.env.example` 为 `.env` 并填写相关 API 密钥。
4. **启动**：
   ```bash
   python main.py
   ```

---

## 💰 成本与安全 FAQ

- **收费吗？**
  完全免费。GitHub Actions 每月提供 2,000 分钟额度，本项目每月仅消耗约 30 分钟。
- **隐私安全吗？**
  只要你的仓库设为 **Private (私有)**，且密钥填在 **Secrets** 中，其他人就无法看到你的 API Key 和推送内容。
- **如何停止推送？**
  在 Actions 页面点击 `Disable workflow` 即可。

## 📄 License
[MIT](LICENSE)
