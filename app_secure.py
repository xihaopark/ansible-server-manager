import streamlit as st
import ansible_runner
import json
import yaml
import os
from datetime import datetime
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建必要的目录
os.makedirs('ansible_inventory', exist_ok=True)
os.makedirs('ansible_playbooks', exist_ok=True)
os.makedirs('ansible_logs', exist_ok=True)

# 页面配置
st.set_page_config(
    page_title="Ansible服务器管理面板",
    page_icon="🖥️",
    layout="wide"
)

# 从环境变量读取服务器配置
def load_servers_from_env():
    servers = {}
    
    # 查找所有SERVER_*_HOST环境变量
    for key in os.environ:
        if key.endswith('_HOST') and key.startswith('SERVER_'):
            server_name = key.replace('_HOST', '').replace('SERVER_', 'Server ')
            server_prefix = key.replace('_HOST', '')
            
            servers[server_name] = {
                "host": os.getenv(f"{server_prefix}_HOST"),
                "user": os.getenv(f"{server_prefix}_USER", "root"),
                "password": os.getenv(f"{server_prefix}_PASSWORD")
            }
    
    return servers

# 加载服务器配置
SERVERS = load_servers_from_env()

# 如果没有配置服务器，显示警告
if not SERVERS:
    st.error("❌ 未找到服务器配置！请创建 .env 文件并配置服务器信息。")
    st.code("""
# .env 文件示例
SERVER_A_HOST=192.168.1.100
SERVER_A_USER=root
SERVER_A_PASSWORD=your_password

SERVER_B_HOST=192.168.1.101
SERVER_B_USER=root
SERVER_B_PASSWORD=your_password
    """)
    st.stop()

# 生成Ansible inventory文件
def generate_inventory():
    inventory = {
        "all": {
            "hosts": {},
            "vars": {
                "ansible_connection": "ssh",
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no",
                "ansible_python_interpreter": "/usr/bin/python3"
            }
        }
    }
    
    for name, config in SERVERS.items():
        if config["host"] and config["password"]:  # 确保必要信息存在
            inventory["all"]["hosts"][name.replace(" ", "_")] = {
                "ansible_host": config["host"],
                "ansible_user": config["user"],
                "ansible_password": config["password"]
            }
    
    with open('ansible_inventory/hosts.yml', 'w') as f:
        yaml.dump(inventory, f)

# 执行Ansible命令
def run_ansible_adhoc(hosts, module, args=""):
    generate_inventory()
    
    runner = ansible_runner.run(
        private_data_dir='.',
        inventory='ansible_inventory/hosts.yml',
        host_pattern=hosts,
        module=module,
        module_args=args,
        quiet=True
    )
    
    return runner

# 执行Ansible Playbook
def run_ansible_playbook(playbook_path, hosts="all"):
    generate_inventory()
    
    runner = ansible_runner.run(
        private_data_dir='.',
        inventory='ansible_inventory/hosts.yml',
        playbook=playbook_path,
        limit=hosts,
        quiet=True
    )
    
    return runner

# 创建系统信息收集playbook
def create_system_info_playbook():
    playbook = [{
        "name": "收集系统信息",
        "hosts": "all",
        "gather_facts": True,
        "tasks": [
            {
                "name": "获取系统信息",
                "setup": None
            }
        ]
    }]
    
    with open('ansible_playbooks/system_info.yml', 'w') as f:
        yaml.dump(playbook, f)

# 主程序开始

# 主界面
st.title("🖥️ Ansible服务器管理面板")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("服务器列表")
    
    # 显示服务器状态
    st.subheader("服务器概览")
    for name, config in SERVERS.items():
        with st.expander(f"{name} ({config['host']})"):
            st.text(f"IP: {config['host']}")
            st.text(f"用户: {config['user']}")
            st.text("密码: ********")
    
    st.markdown("---")
    
    # 安全提示
    with st.expander("🔐 安全建议"):
        st.markdown("""
        1. **使用SSH密钥认证**
        2. **定期更换密码**
        3. **限制root访问**
        4. **启用防火墙**
        5. **定期更新系统**
        """)
    
    # 应用信息
    st.info("💡 Ansible服务器管理工具 v1.0")

# 主要功能标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 服务器状态", 
    "🔧 执行命令", 
    "📋 系统信息", 
    "📈 监控面板",
    "⚙️ 高级操作"
])

# Tab 1: 服务器状态
with tab1:
    st.header("服务器连接状态")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        auto_refresh = st.checkbox("自动刷新 (30秒)")
    
    if st.button("🔄 检查所有服务器连接") or auto_refresh:
        with st.spinner("正在检查服务器连接..."):
            results = []
            
            for name in SERVERS.keys():
                host_pattern = name.replace(" ", "_")
                runner = run_ansible_adhoc(host_pattern, "ping")
                
                status = "✅ 在线" if runner.status == "successful" else "❌ 离线"
                results.append({
                    "服务器": name,
                    "IP地址": SERVERS[name]["host"],
                    "状态": status,
                    "检查时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            # 显示统计信息
            online_count = len([r for r in results if "✅" in r["状态"]])
            total_count = len(results)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("总服务器数", total_count)
            col2.metric("在线服务器", online_count)
            col3.metric("离线服务器", total_count - online_count)

# Tab 2: 执行命令
with tab2:
    st.header("执行远程命令")
    
    # 预定义命令
    st.subheader("快速命令")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_commands = {
        "查看进程": "ps aux | head -20",
        "磁盘使用": "df -h",
        "内存使用": "free -m",
        "网络连接": "netstat -tuln | head -20"
    }
    
    selected_quick_cmd = None
    for i, (label, cmd) in enumerate(quick_commands.items()):
        if i % 4 == 0:
            if col1.button(label):
                selected_quick_cmd = cmd
        elif i % 4 == 1:
            if col2.button(label):
                selected_quick_cmd = cmd
        elif i % 4 == 2:
            if col3.button(label):
                selected_quick_cmd = cmd
        else:
            if col4.button(label):
                selected_quick_cmd = cmd
    
    st.markdown("---")
    
    # 自定义命令
    st.subheader("自定义命令")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_servers = st.multiselect(
            "选择服务器",
            options=list(SERVERS.keys()),
            default=list(SERVERS.keys())
        )
    
    with col2:
        if selected_quick_cmd:
            command = st.text_input("输入要执行的命令", value=selected_quick_cmd)
        else:
            command = st.text_input("输入要执行的命令", placeholder="例如: ls -la, df -h, free -m")
    
    # 危险命令警告
    dangerous_commands = ['rm -rf', 'shutdown', 'reboot', 'mkfs', 'dd if=']
    if any(dc in command.lower() for dc in dangerous_commands):
        st.warning("⚠️ 警告：您正在执行可能有危险的命令！")
    
    if st.button("执行命令", type="primary") and command and selected_servers:
        hosts = ",".join([s.replace(" ", "_") for s in selected_servers])
        
        with st.spinner(f"正在执行命令: {command}"):
            runner = run_ansible_adhoc(hosts, "shell", command)
            
            st.subheader("执行结果")
            
            for event in runner.events:
                if event['event'] == 'runner_on_ok':
                    host = event['event_data']['host']
                    result = event['event_data']['res']
                    
                    with st.expander(f"📍 {host}", expanded=True):
                        if 'stdout' in result:
                            st.code(result['stdout'], language='bash')
                        if 'stderr' in result and result['stderr']:
                            st.error(result['stderr'])
                
                elif event['event'] == 'runner_on_failed':
                    host = event['event_data']['host']
                    st.error(f"❌ {host}: 命令执行失败")

# Tab 3: 系统信息
with tab3:
    st.header("系统详细信息")
    
    if st.button("🔍 收集系统信息"):
        create_system_info_playbook()
        
        with st.spinner("正在收集系统信息..."):
            runner = run_ansible_playbook('ansible_playbooks/system_info.yml')
            
            for event in runner.events:
                if event['event'] == 'runner_on_ok' and 'ansible_facts' in event['event_data']['res']:
                    host = event['event_data']['host']
                    facts = event['event_data']['res']['ansible_facts']
                    
                    with st.expander(f"🖥️ {host} 系统信息", expanded=True):
                        # 基本信息
                        st.subheader("基本信息")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("操作系统", f"{facts.get('ansible_distribution', 'N/A')} {facts.get('ansible_distribution_version', '')}")
                            st.metric("内核版本", facts.get('ansible_kernel', 'N/A'))
                            st.metric("架构", facts.get('ansible_architecture', 'N/A'))
                        
                        with col2:
                            st.metric("CPU核心数", facts.get('ansible_processor_cores', 'N/A'))
                            st.metric("CPU型号", facts.get('ansible_processor', ['N/A'])[-1] if facts.get('ansible_processor') else 'N/A')
                            total_mem = facts.get('ansible_memtotal_mb', 0)
                            st.metric("总内存", f"{total_mem:,} MB")
                        
                        with col3:
                            st.metric("主机名", facts.get('ansible_hostname', 'N/A'))
                            st.metric("IP地址", facts.get('ansible_default_ipv4', {}).get('address', 'N/A'))
                            uptime_days = facts.get('ansible_uptime_seconds', 0) // 86400
                            st.metric("运行时间", f"{uptime_days} 天")
                        
                        # 网络接口
                        st.subheader("网络接口")
                        interfaces = facts.get('ansible_interfaces', [])
                        if interfaces:
                            for iface in interfaces[:5]:  # 限制显示前5个
                                iface_data = facts.get(f'ansible_{iface}', {})
                                if iface_data.get('ipv4'):
                                    st.text(f"{iface}: {iface_data['ipv4'].get('address', 'N/A')}")

# Tab 4: 监控面板
with tab4:
    st.header("实时监控")
    
    # 选择监控类型
    monitor_type = st.selectbox(
        "选择监控类型",
        ["资源使用率", "服务状态", "日志查看"]
    )
    
    if monitor_type == "资源使用率":
        st.subheader("资源使用监控")
        
        monitoring_commands = {
            "CPU使用率": "top -bn1 | head -20",
            "内存详情": "free -m",
            "磁盘使用": "df -h",
            "系统负载": "uptime",
            "网络流量": "ifconfig | grep -A 1 'inet'",
            "进程统计": "ps aux --sort=-%cpu | head -10"
        }
        
        selected_metric = st.selectbox("选择监控指标", list(monitoring_commands.keys()))
        
        if st.button("📊 获取监控数据"):
            command = monitoring_commands[selected_metric]
            
            with st.spinner(f"正在获取{selected_metric}数据..."):
                for name in SERVERS.keys():
                    host_pattern = name.replace(" ", "_")
                    runner = run_ansible_adhoc(host_pattern, "shell", command)
                    
                    for event in runner.events:
                        if event['event'] == 'runner_on_ok':
                            result = event['event_data']['res']
                            
                            with st.expander(f"📊 {name}", expanded=True):
                                if 'stdout' in result:
                                    st.code(result['stdout'], language='bash')
    
    elif monitor_type == "服务状态":
        st.subheader("服务状态检查")
        
        common_services = ["nginx", "apache2", "mysql", "postgresql", "redis", "docker", "ssh"]
        selected_service = st.selectbox("选择服务", common_services)
        
        if st.button("🔍 检查服务状态"):
            command = f"systemctl status {selected_service} --no-pager"
            
            with st.spinner(f"正在检查 {selected_service} 服务状态..."):
                for name in SERVERS.keys():
                    host_pattern = name.replace(" ", "_")
                    runner = run_ansible_adhoc(host_pattern, "shell", command)
                    
                    for event in runner.events:
                        if event['event'] == 'runner_on_ok':
                            result = event['event_data']['res']
                            
                            with st.expander(f"🔧 {name}"):
                                if 'stdout' in result:
                                    output = result['stdout']
                                    if "active (running)" in output:
                                        st.success(f"✅ {selected_service} 正在运行")
                                    else:
                                        st.error(f"❌ {selected_service} 未运行")
                                    st.code(output, language='bash')
    
    elif monitor_type == "日志查看":
        st.subheader("系统日志查看")
        
        log_files = {
            "系统日志": "/var/log/syslog",
            "认证日志": "/var/log/auth.log",
            "Nginx访问日志": "/var/log/nginx/access.log",
            "Nginx错误日志": "/var/log/nginx/error.log",
            "Apache访问日志": "/var/log/apache2/access.log",
            "Apache错误日志": "/var/log/apache2/error.log"
        }
        
        selected_log = st.selectbox("选择日志文件", list(log_files.keys()))
        lines = st.slider("显示行数", 10, 100, 20)
        
        if st.button("📄 查看日志"):
            log_path = log_files[selected_log]
            command = f"tail -n {lines} {log_path}"
            
            with st.spinner(f"正在读取日志文件..."):
                for name in SERVERS.keys():
                    host_pattern = name.replace(" ", "_")
                    runner = run_ansible_adhoc(host_pattern, "shell", command)
                    
                    for event in runner.events:
                        if event['event'] == 'runner_on_ok':
                            result = event['event_data']['res']
                            
                            with st.expander(f"📄 {name} - {selected_log}"):
                                if 'stdout' in result:
                                    st.code(result['stdout'], language='log')
                                if 'stderr' in result and "No such file" in result['stderr']:
                                    st.warning(f"日志文件不存在: {log_path}")

# Tab 5: 高级操作
with tab5:
    st.header("高级操作")
    
    operation = st.selectbox(
        "选择操作类型",
        ["软件包管理", "用户管理", "文件操作", "服务管理"]
    )
    
    if operation == "软件包管理":
        st.subheader("📦 软件包管理")
        
        action = st.radio("选择操作", ["安装", "更新", "删除", "搜索"])
        package_name = st.text_input("软件包名称")
        
        if st.button("执行操作") and package_name:
            if action == "安装":
                command = f"apt-get install -y {package_name}"
            elif action == "更新":
                command = f"apt-get update && apt-get upgrade -y {package_name}"
            elif action == "删除":
                command = f"apt-get remove -y {package_name}"
            else:
                command = f"apt-cache search {package_name}"
            
            st.warning(f"即将执行: {command}")
            
            if st.button("确认执行", key="confirm_package"):
                with st.spinner(f"正在{action}软件包 {package_name}..."):
                    for name in SERVERS.keys():
                        host_pattern = name.replace(" ", "_")
                        runner = run_ansible_adhoc(host_pattern, "shell", command)
                        
                        for event in runner.events:
                            if event['event'] == 'runner_on_ok':
                                st.success(f"✅ {name}: 操作完成")
                            elif event['event'] == 'runner_on_failed':
                                st.error(f"❌ {name}: 操作失败")
    
    elif operation == "服务管理":
        st.subheader("🔧 服务管理")
        
        service_name = st.text_input("服务名称", placeholder="例如: nginx, mysql, docker")
        action = st.radio("选择操作", ["启动", "停止", "重启", "重载"])
        
        if st.button("执行操作") and service_name:
            action_map = {
                "启动": "start",
                "停止": "stop",
                "重启": "restart",
                "重载": "reload"
            }
            
            command = f"systemctl {action_map[action]} {service_name}"
            
            with st.spinner(f"正在{action}服务 {service_name}..."):
                for name in SERVERS.keys():
                    host_pattern = name.replace(" ", "_")
                    runner = run_ansible_adhoc(host_pattern, "shell", command)
                    
                    for event in runner.events:
                        if event['event'] == 'runner_on_ok':
                            st.success(f"✅ {name}: 服务{action}成功")
                            # 检查服务状态
                            status_runner = run_ansible_adhoc(host_pattern, "shell", f"systemctl is-active {service_name}")
                            for status_event in status_runner.events:
                                if status_event['event'] == 'runner_on_ok':
                                    status = status_event['event_data']['res']['stdout'].strip()
                                    st.info(f"服务状态: {status}")

# 页脚
st.markdown("---")
st.markdown("💡 **提示**: 这是一个基于Ansible的服务器管理工具。请谨慎执行操作，特别是在生产环境中。")
st.markdown("🔒 **安全**: 所有密码信息都从环境变量读取，不会在代码中硬编码。")