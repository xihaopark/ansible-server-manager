#!/bin/bash

echo "🚀 Ansible服务器管理工具 - 安装脚本"
echo "====================================="

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

# 创建虚拟环境
echo -e "\n创建虚拟环境..."
python3 -m venv venv
if [[ $? -eq 0 ]]; then
    echo "✅ 虚拟环境创建成功"
else
    echo "❌ 虚拟环境创建失败"
    exit 1
fi

# 激活虚拟环境
echo -e "\n激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo -e "\n升级pip..."
pip install --upgrade pip

# 安装依赖
echo -e "\n安装项目依赖..."
pip install -r requirements.txt
if [[ $? -eq 0 ]]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建.env文件（如果不存在）
if [ ! -f .env ]; then
    echo -e "\n创建.env配置文件..."
    cat > .env << EOL
# 应用配置
APP_NAME=Ansible Server Manager

# Server A
SERVER_A_HOST=108.61.207.206
SERVER_A_USER=root
SERVER_A_PASSWORD=4C+uD3si,#5,rCW]

# Server B
SERVER_B_HOST=149.28.92.23
SERVER_B_USER=root
SERVER_B_PASSWORD=z@8B}s)fT#?tQurb

# Server C
SERVER_C_HOST=108.61.207.206
SERVER_C_USER=root
SERVER_C_PASSWORD=4C+uD3si,#5,rCW]

# Ansible配置
ANSIBLE_HOST_KEY_CHECKING=False
ANSIBLE_TIMEOUT=30
EOL
    echo "✅ .env文件创建成功"
    echo "⚠️  请编辑.env文件，更新服务器密码信息"
else
    echo "✅ .env文件已存在"
fi

# 创建必要的目录
echo -e "\n创建项目目录..."
mkdir -p ansible_inventory
mkdir -p ansible_playbooks
mkdir -p ansible_logs
echo "✅ 目录创建成功"

# 生成启动脚本
echo -e "\n创建启动脚本..."
cat > run.sh << 'EOL'
#!/bin/bash
source venv/bin/activate
streamlit run app_secure.py --server.port 8501 --server.address 0.0.0.0
EOL
chmod +x run.sh
echo "✅ 启动脚本创建成功"

echo -e "\n========================================="
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，确保服务器信息正确"
echo "2. 运行 ./run.sh 启动应用"
echo "3. 在浏览器中访问 http://localhost:8501"
echo ""
echo "安全建议："
echo "- 考虑使用SSH密钥代替密码认证"
echo "- 在生产环境中使用HTTPS"
echo "- 定期更新服务器密码"
echo "========================================="