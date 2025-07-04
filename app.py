import streamlit as st
import ansible_runner
import json
import yaml
import os
from datetime import datetime
import pandas as pd
from pathlib import Path

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

# 服务器配置（注意：实际使用时应该从环境变量或加密配置文件读取）
SERVERS = {
    "Server A": {
        "host": "108.61.207.206",
        "user": "root",
        "password": "4C+uD3si,#5,rCW]"
    },
    "Server B": {
        "host": "149.28.92.23",
        "user": "root",
        "password": "z@8B}s)fT#?tQurb"
    },
    "Server C": {
        "host": "108.61.207.206",  # 注意：与Server A相同的IP
        "user": "root",
        "password": "4C+uD3si,#5,rCW]"
    }
}

# 生成Ansible inventory文件
def generate_inventory():
    inventory = {
        "all": {
            "hosts": {},
            "vars": {
                "ansible_connection": "ssh",
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
            }
        }
    }
    
    for name, config in SERVERS.items():
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
    st.info("⚠️ 安全提示：建议使用SSH密钥认证而非密码")

# 主要功能标签页
tab1, tab2, tab3, tab4 = st.tabs(["📊 服务器状态", "🔧 执行命令", "📋 系统信息", "📈 监控面板"])

# Tab 1: 服务器状态
with tab1:
    st.header("服务器连接状态")
    
    if st.button("检查所有服务器连接"):
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

# Tab 2: 执行命令
with tab2:
    st.header("执行远程命令")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_servers = st.multiselect(
            "选择服务器",
            options=list(SERVERS.keys()),
            default=list(SERVERS.keys())
        )
    
    with col2:
        command = st.text_input("输入要执行的命令", placeholder="例如: ls -la, df -h, free -m")
    
    if st.button("执行命令") and command and selected_servers:
        hosts = ",".join([s.replace(" ", "_") for s in selected_servers])
        
        with st.spinner(f"正在执行命令: {command}"):
            runner = run_ansible_adhoc(hosts, "shell", command)
            
            st.subheader("执行结果")
            
            for event in runner.events:
                if event['event'] == 'runner_on_ok':
                    host = event['event_data']['host']
                    result = event['event_data']['res']
                    
                    with st.expander(f"📍 {host}"):
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
    
    if st.button("收集系统信息"):
        create_system_info_playbook()
        
        with st.spinner("正在收集系统信息..."):
            runner = run_ansible_playbook('ansible_playbooks/system_info.yml')
            
            for event in runner.events:
                if event['event'] == 'runner_on_ok' and 'ansible_facts' in event['event_data']['res']:
                    host = event['event_data']['host']
                    facts = event['event_data']['res']['ansible_facts']
                    
                    with st.expander(f"🖥️ {host} 系统信息"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("操作系统", f"{facts.get('ansible_distribution', 'N/A')} {facts.get('ansible_distribution_version', '')}")
                            st.metric("内核版本", facts.get('ansible_kernel', 'N/A'))
                            st.metric("架构", facts.get('ansible_architecture', 'N/A'))
                        
                        with col2:
                            st.metric("CPU核心数", facts.get('ansible_processor_cores', 'N/A'))
                            total_mem = facts.get('ansible_memtotal_mb', 0)
                            free_mem = facts.get('ansible_memfree_mb', 0)
                            st.metric("总内存", f"{total_mem} MB")
                            st.metric("可用内存", f"{free_mem} MB")
                        
                        with col3:
                            st.metric("主机名", facts.get('ansible_hostname', 'N/A'))
                            st.metric("IP地址", facts.get('ansible_default_ipv4', {}).get('address', 'N/A'))
                            st.metric("运行时间", facts.get('ansible_uptime_seconds', 0) // 86400, "天")

# Tab 4: 监控面板
with tab4:
    st.header("实时监控")
    
    # 资源使用情况
    st.subheader("资源使用监控")
    
    monitoring_commands = {
        "CPU使用率": "top -bn1 | grep 'Cpu(s)' | head -1",
        "内存使用": "free -m | grep Mem",
        "磁盘使用": "df -h | grep '^/dev/'",
        "系统负载": "uptime"
    }
    
    selected_metric = st.selectbox("选择监控指标", list(monitoring_commands.keys()))
    
    if st.button("获取监控数据"):
        command = monitoring_commands[selected_metric]
        
        with st.spinner(f"正在获取{selected_metric}数据..."):
            for name in SERVERS.keys():
                host_pattern = name.replace(" ", "_")
                runner = run_ansible_adhoc(host_pattern, "shell", command)
                
                for event in runner.events:
                    if event['event'] == 'runner_on_ok':
                        result = event['event_data']['res']
                        
                        with st.expander(f"📊 {name}"):
                            if 'stdout' in result:
                                st.code(result['stdout'], language='bash')

# 页脚
st.markdown("---")
st.markdown("💡 **提示**: 这是一个基础的Ansible可视化管理工具。建议在生产环境中使用更安全的认证方式。")