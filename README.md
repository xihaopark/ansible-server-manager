# 🖥️ Ansible 服务器可视化管理工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![Ansible](https://img.shields.io/badge/Ansible-8.5.0-green.svg)](https://www.ansible.com/)

这是一个基于 Streamlit 和 Ansible 的服务器管理可视化工具，提供直观的Web界面来管理和监控多台服务器。

## ✨ 功能特点

- 🖥️ **服务器状态监控**：实时检查服务器连接状态
- 🔧 **远程命令执行**：在选定的服务器上执行Shell命令
- 📋 **系统信息收集**：获取服务器的详细系统信息
- 📈 **资源监控**：监控CPU、内存、磁盘等资源使用情况
- 📦 **软件包管理**：安装、更新、删除软件包
- 🔧 **服务管理**：启动、停止、重启系统服务
- 📄 **日志查看**：查看系统和应用日志
- 🔐 **安全认证**：密码保护的Web界面

## 🚀 快速开始

### 方法一：一键安装（推荐）

```bash
# 克隆项目
git clone https://github.com/xihaopark/ansible-server-manager.git
cd ansible-server-manager

# 运行安装脚本
chmod +x setup.sh
./setup.sh

# 启动应用
./run.sh
```

### 方法二：手动安装

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的服务器信息

# 4. 启动应用
streamlit run app_secure.py --server.port 8501
```

## ⚙️ 配置说明

1. **复制配置文件**：
   ```bash
   cp .env.example .env
   ```

2. **编辑 `.env` 文件**：
   ```bash
   # 应用密码
   APP_PASSWORD=your_password
   
   # 服务器配置
   SERVER_A_HOST=your_server_ip
   SERVER_A_USER=root
   SERVER_A_PASSWORD=your_password
   ```

## 📱 使用方法

1. 启动应用后，访问：http://localhost:8501
2. 输入在 `.env` 中设置的密码
3. 选择功能标签页开始管理服务器

## 安全建议

⚠️ **重要安全提示**：

1. **不要在代码中硬编码密码**
   - 使用环境变量存储敏感信息
   - 或使用加密的配置文件

2. **使用SSH密钥认证**
   - 生成SSH密钥对：`ssh-keygen -t rsa -b 4096`
   - 将公钥添加到服务器：`ssh-copy-id user@server`

3. **限制访问**
   - 在生产环境中添加身份验证
   - 使用HTTPS加密传输

## 改进建议

### 1. 使用环境变量存储密码

```python
import os
from dotenv import load_dotenv

load_dotenv()

SERVERS = {
    "Server A": {
        "host": os.getenv("SERVER_A_HOST"),
        "user": os.getenv("SERVER_A_USER"),
        "password": os.getenv("SERVER_A_PASSWORD")
    }
}
```

### 2. 添加SSH密钥支持

```python
# 在inventory中使用SSH密钥
inventory["all"]["hosts"][name] = {
    "ansible_host": config["host"],
    "ansible_user": config["user"],
    "ansible_ssh_private_key_file": "/path/to/private/key"
}
```

### 3. 添加更多功能

- 📦 软件包管理（安装/更新/删除）
- 🔄 服务管理（启动/停止/重启服务）
- 📁 文件管理（上传/下载/编辑文件）
- 🔐 用户管理（创建/删除用户）
- 📊 日志查看和分析
- ⏰ 定时任务管理

## 故障排除

### 连接问题
- 确保服务器SSH服务正在运行
- 检查防火墙设置
- 验证用户名和密码是否正确

### Ansible相关问题
- 确保已安装所有依赖：`pip install -r requirements.txt`
- 检查Python版本（建议使用Python 3.8+）

## 注意事项

- 服务器A和C的IP地址相同（108.61.207.206），请确认是否正确
- 建议定期更新密码并使用强密码策略
- 在执行危险命令前请谨慎确认

## 📦 打包成macOS应用

如果您想将工具打包成可以双击运行的macOS应用：

```bash
# 运行打包脚本
chmod +x build_app.sh
./build_app.sh

# 打包完成后，应用位于 dist/ 目录
# 您可以将 "Ansible Server Manager.app" 拷贝到任何地方使用
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📸 截图

![主界面](screenshots/main.png)
![服务器监控](screenshots/monitoring.png)

## 🔗 相关链接

- [Streamlit 文档](https://docs.streamlit.io/)
- [Ansible 文档](https://docs.ansible.com/)
- [项目Wiki](https://github.com/xihaopark/ansible-server-manager/wiki)
- [在线文档](https://xihaopark.github.io/ansible-server-manager/)