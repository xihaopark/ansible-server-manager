#!/bin/bash

echo "🚀 准备GitHub发布..."
echo "===================="

# 创建截图目录
mkdir -p screenshots

# 创建.env.example文件
if [ ! -f .env.example ]; then
    echo "📝 创建.env.example文件..."
    cat > .env.example << 'EOL'
# 应用密码（用于访问Web界面）
APP_PASSWORD=admin

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

# 初始化Git仓库（如果还没有）
if [ ! -d .git ]; then
    echo "🔧 初始化Git仓库..."
    git init
    git add .
    git commit -m "Initial commit: Ansible Server Manager"
fi

echo "✅ GitHub发布准备完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在GitHub上创建新仓库 'ansible-server-manager'"
echo "2. 运行以下命令上传代码："
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/ansible-server-manager.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🔐 注意：请确保 .env 文件已被 .gitignore 忽略，不会上传敏感信息！"
echo ""
echo "📁 项目文件结构："
ls -la | grep -E '\.(py|sh|txt|md)$|^d' 