"""
py2app setup script for Ansible Server Manager
"""
from setuptools import setup

APP = ['app_secure.py']
DATA_FILES = [
    ('', ['README.md', 'requirements.txt', '.env.example']),
    ('ansible_inventory', []),
    ('ansible_playbooks', []),
    ('ansible_logs', []),
]

OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': False,
        'CFBundleName': 'Ansible Server Manager',
        'CFBundleDisplayName': 'Ansible Server Manager',
        'CFBundleGetInfoString': "Ansible服务器管理工具",
        'CFBundleIdentifier': "com.ansible.servermanager",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': u"Copyright © 2024, Ansible Server Manager",
    },
    'packages': ['streamlit', 'ansible_runner', 'pandas', 'yaml', 'dotenv'],
    'includes': ['streamlit', 'ansible_runner', 'pandas', 'yaml', 'dotenv'],
    'excludes': ['tkinter', 'PyQt5', 'PyQt4'],
    'iconfile': None,  # 您可以添加.icns图标文件
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 