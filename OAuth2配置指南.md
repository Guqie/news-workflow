# OAuth 2.0邮件发送配置指南

**配置时间：** 2026-02-10 11:05
**目标：** 配置Outlook OAuth 2.0邮件发送

---

## 第一步：注册Azure应用

### 1. 访问Azure门户
- 打开浏览器
- 访问：https://portal.azure.com
- 使用你的Microsoft账户登录（Guqie1@outlook.com）

### 2. 进入应用注册
- 在搜索框输入"应用注册"或"App registrations"
- 点击进入"应用注册"页面

### 3. 创建新应用
- 点击"+ 新注册"或"+ New registration"
- 填写信息：
  - 名称：`Clawdbot邮件发送`
  - 支持的账户类型：选择"仅此组织目录中的账户"
  - 重定向URI：选择"Web"，输入 `http://localhost:8080`
- 点击"注册"

### 4. 记录应用信息
注册成功后，会看到：
- **应用程序(客户端) ID** - 复制保存
- **目录(租户) ID** - 复制保存

---

**完成第一步后，告诉我你的Client ID**
