#!/bin/bash

echo "🚀 开始打包Ansible服务器管理工具..."
echo "=================================="

# 激活虚拟环境
source venv/bin/activate

# 安装打包工具
echo "📦 安装打包工具..."
pip install py2app

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

# Ansible配置
ANSIBLE_HOST_KEY_CHECKING=False
ANSIBLE_TIMEOUT=30
EOL
fi

# 清理之前的构建
echo "🧹 清理之前的构建..."
rm -rf build dist

# 开始打包
echo "🔨 开始打包应用..."
python setup_app.py py2app

if [ $? -eq 0 ]; then
    echo "✅ 打包成功！"
    echo ""
    echo "📱 应用位置: dist/Ansible Server Manager.app"
    echo "💡 使用方法:"
    echo "   1. 双击 'Ansible Server Manager.app' 启动应用"
    echo "   2. 首次运行时，请在应用目录创建 .env 文件"
    echo "   3. 在浏览器中访问 http://localhost:8501"
    echo ""
    echo "📦 您可以将 dist/ 文件夹中的应用拷贝到任何地方使用"
else
    echo "❌ 打包失败，请检查错误信息"
fi 