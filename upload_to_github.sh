#!/bin/bash

echo "🚀 准备上传到GitHub..."
echo "========================="

# 设置Git用户信息
echo "📝 配置Git用户信息..."
git config user.name "xihao park"
git config user.email "xihaopark@gamil.com"

# 初始化Git仓库（如果还没有）
if [ ! -d .git ]; then
    echo "🔧 初始化Git仓库..."
    git init
    git branch -M main
fi

# 创建MIT许可证文件
echo "📄 创建MIT许可证..."
cat > LICENSE << 'EOL'
MIT License

Copyright (c) 2024 xihao park

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOL

# 创建.env.example文件
if [ ! -f .env.example ]; then
    echo "📝 创建.env.example文件..."
    cat > .env.example << 'EOL'
# 应用配置
APP_NAME=Ansible Server Manager

# Server A
SERVER_A_HOST=your_server_ip
SERVER_A_USER=root
SERVER_A_PASSWORD=your_password

# Server B
SERVER_B_HOST=your_server_ip
SERVER_B_USER=root
SERVER_B_PASSWORD=your_password

# Server C
SERVER_C_HOST=your_server_ip
SERVER_C_USER=root
SERVER_C_PASSWORD=your_password

# Ansible配置
ANSIBLE_HOST_KEY_CHECKING=False
ANSIBLE_TIMEOUT=30
EOL
fi

# 添加所有文件到Git
echo "📦 添加文件到Git..."
git add .

# 检查是否有变更
if git diff --staged --quiet; then
    echo "⚠️  没有检测到变更，跳过提交"
else
    # 提交变更
    echo "💾 提交变更..."
    git commit -m "Initial commit: Ansible Server Manager

🖥️ 功能特点:
- 服务器状态监控
- 远程命令执行
- 系统信息收集
- 资源监控
- 软件包管理
- 服务管理
- 日志查看

🚀 支持:
- Web界面 (Streamlit)
- macOS应用打包
- 环境变量配置
- 安全认证"
fi

echo ""
echo "✅ Git仓库准备完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在GitHub上创建新仓库 'ansible-server-manager'"
echo "   地址: https://github.com/new"
echo "   仓库名: ansible-server-manager"
echo "   类型: Public"
echo "   ❌ 不要勾选 'Add a README file'"
echo "   ❌ 不要勾选 'Add .gitignore'"
echo "   ✅ 选择 'MIT License'"
echo ""
echo "2. 创建完成后，运行以下命令上传代码："
echo ""
echo "   git remote add origin https://github.com/xihaopark/ansible-server-manager.git"
echo "   git push -u origin main"
echo ""
echo "🔐 注意：首次推送可能需要GitHub Personal Access Token"
echo "   如需帮助，请访问: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token" 