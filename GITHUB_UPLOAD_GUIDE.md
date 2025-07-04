# 📚 GitHub 上传完整指南

## 🎯 第一步：在GitHub上创建仓库

1. **访问GitHub创建页面**：
   - 打开浏览器，访问：https://github.com/new
   - 确保已登录您的GitHub账户 (xihaopark)

2. **填写仓库信息**：
   ```
   Repository name: ansible-server-manager
   Description: 基于Streamlit和Ansible的服务器管理可视化工具
   ```

3. **仓库设置**：
   - ✅ **Public** (公开仓库)
   - ❌ **不要勾选** "Add a README file"
   - ❌ **不要勾选** "Add .gitignore"
   - ✅ **选择** "MIT License"

4. **点击 "Create repository"**

## 🚀 第二步：上传代码

创建仓库后，GitHub会显示一个页面。**忽略页面上的指令**，直接在终端运行：

```bash
# 1. 添加远程仓库
git remote add origin https://github.com/xihaopark/ansible-server-manager.git

# 2. 推送代码到GitHub
git push -u origin main
```

## 🔐 第三步：处理认证（如果需要）

如果推送时要求输入用户名和密码：

### 方法一：使用Personal Access Token (推荐)

1. **创建Token**：
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 设置过期时间和权限：
     - Expiration: 90 days (或更长)
     - 勾选：`repo` (完整仓库权限)
   - 点击 "Generate token"
   - **立即复制Token**（只显示一次）

2. **使用Token推送**：
   ```bash
   # 用户名输入：xihaopark
   # 密码输入：刚才复制的Token
   git push -u origin main
   ```

### 方法二：配置SSH密钥

1. **生成SSH密钥**：
   ```bash
   ssh-keygen -t ed25519 -C "xihaopark@gamil.com"
   ```

2. **添加到GitHub**：
   ```bash
   # 复制公钥
   cat ~/.ssh/id_ed25519.pub
   ```
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥内容

3. **更改远程URL**：
   ```bash
   git remote set-url origin git@github.com:xihaopark/ansible-server-manager.git
   git push -u origin main
   ```

## ✅ 第四步：验证上传成功

1. **访问仓库页面**：
   https://github.com/xihaopark/ansible-server-manager

2. **检查内容**：
   - ✅ README.md 显示正常
   - ✅ 代码文件都已上传
   - ✅ MIT License 已添加

## 🌐 第五步：设置GitHub Pages

1. **进入仓库设置**：
   - 在仓库页面点击 "Settings"
   - 在左侧菜单找到 "Pages"

2. **配置Pages**：
   - Source: "Deploy from a branch"
   - Branch: "gh-pages" (如果没有，先选择None)
   - 点击 "Save"

3. **等待Actions运行**：
   - 点击仓库的 "Actions" 标签
   - 等待CI/CD流程完成
   - 成功后会自动创建 gh-pages 分支

4. **访问文档站点**：
   https://xihaopark.github.io/ansible-server-manager/

## 🏷️ 第六步：添加Topics标签

1. **在仓库主页**：
   - 点击右侧的齿轮图标 ⚙️ (在About部分)

2. **添加Topics**：
   ```
   ansible, server-management, streamlit, python, devops, automation, monitoring, web-app
   ```

3. **点击 "Save changes"**

## 🎉 完成！

您的项目现在已经成功上传到GitHub，并具备：

- ✅ **完整的代码仓库**
- ✅ **自动化CI/CD流程**
- ✅ **在线文档站点**
- ✅ **MIT开源许可证**
- ✅ **专业的项目展示**

## 📞 如需帮助

如果遇到任何问题，请：

1. 检查网络连接
2. 确认GitHub用户名和密码/Token正确
3. 查看终端错误信息
4. 参考GitHub官方文档：https://docs.github.com/

---

**项目地址**: https://github.com/xihaopark/ansible-server-manager  
**文档地址**: https://xihaopark.github.io/ansible-server-manager/ 