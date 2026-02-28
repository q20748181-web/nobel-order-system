#!/bin/bash
# -*- coding: utf-8 -*-
# Streamlit Cloud 部署自动化脚本

set -e

echo "=========================================="
echo "🚀 Nobel订单管理系统 - Streamlit Cloud 部署"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}欢迎使用 Streamlit Cloud 自动部署向导${NC}"
echo ""
echo "本脚本将帮助您完成以下步骤："
echo "  1. 检查代码准备情况"
echo "  2. 验证必要文件"
echo "  3. 生成部署配置"
echo "  4. 提供推送到 GitHub 的详细说明"
echo "  5. 提供在 Streamlit Cloud 部署的步骤"
echo ""

# 检查必要文件
echo "=========================================="
echo "📋 步骤 1/5: 检查必要文件"
echo "=========================================="
echo ""

REQUIRED_FILES=(
    "src/app_server.py"
    "config/supabase_config.json"
    "requirements.streamlit.txt"
)

ALL_EXIST=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    echo -e "${RED}错误：缺少必要文件${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 所有必要文件都存在${NC}"
echo ""

# 检查 Git 状态
echo "=========================================="
echo "📋 步骤 2/5: 检查 Git 状态"
echo "=========================================="
echo ""

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}错误：不是 Git 仓库${NC}"
    echo "请先初始化 Git 仓库："
    echo "  git init"
    exit 1
fi

echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
echo ""

# 添加并提交所有更改
echo "=========================================="
echo "📋 步骤 3/5: 提交代码"
echo "=========================================="
echo ""

echo "添加所有文件到 Git..."
git add -A

echo ""
echo "检查是否有未提交的更改..."
if git diff --cached --quiet; then
    echo -e "${YELLOW}没有新的更改需要提交${NC}"
else
    echo "提交更改..."
    git commit -m "chore: 准备 Streamlit Cloud 部署"
    echo -e "${GREEN}✓ 代码已提交${NC}"
fi

echo ""

# 检查远程仓库
echo "=========================================="
echo "📋 步骤 4/5: 检查远程仓库"
echo "=========================================="
echo ""

if git remote get-url origin > /dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    echo -e "${GREEN}✓ 已配置远程仓库${NC}"
    echo "  URL: $REMOTE_URL"
    echo ""
    echo "推送代码到 GitHub..."
    git push -u origin main || git push -u origin master || {
        echo -e "${RED}推送失败，请检查网络和凭据${NC}"
        echo "或者手动执行："
        echo "  git push -u origin main"
    }
else
    echo -e "${YELLOW}未配置远程仓库${NC}"
    echo ""
    echo "请按以下步骤创建 GitHub 仓库并配置远程："
    echo ""
    echo "1. 访问 GitHub 创建新仓库："
    echo "   https://github.com/new"
    echo ""
    echo "2. 仓库名建议：nobel-order-system"
    echo "   选择 Public 或 Private（推荐 Private）"
    echo ""
    echo "3. 创建仓库后，配置远程仓库："
    echo "   git remote add origin https://github.com/你的用户名/nobel-order-system.git"
    echo ""
    echo "4. 推送代码："
    echo "   git push -u origin main"
    echo ""
    read -p "配置完成后，按回车继续..."
fi

echo ""

# 部署说明
echo "=========================================="
echo "📋 步骤 5/5: Streamlit Cloud 部署说明"
echo "=========================================="
echo ""

echo -e "${BLUE}🎯 下一步：在 Streamlit Cloud 部署${NC}"
echo ""
echo "1. 访问 Streamlit Cloud："
echo "   ${GREEN}https://share.streamlit.io/${NC}"
echo ""
echo "2. 使用 GitHub 账号登录并授权"
echo ""
echo "3. 点击 'New app' 创建新应用"
echo ""
echo "4. 配置应用："
echo "   - 仓库：nobel-order-system（或你的仓库名）"
echo "   - 分支：main（或 master）"
echo "   - 主文件路径：${YELLOW}src/app_server.py${NC}"
echo ""
echo "5. 点击 'Deploy' 开始部署"
echo ""
echo "6. 配置环境变量（重要！）"
echo ""
echo "   在部署页面的 'Secrets' 部分添加以下内容："
echo ""
echo -e "${YELLOW}[supabase]${NC}"
echo -e "${YELLOW}project_url = \"你的 Supabase Project URL\"${NC}"
echo -e "${YELLOW}anon_key = \"你的 Supabase anon key\"${NC}"
echo -e "${YELLOW}service_role_key = \"你的 Supabase service role key\"${NC}"
echo ""
echo "7. 等待部署完成（1-3分钟）"
echo ""
echo "   部署成功后，你会看到类似这样的地址："
echo "   ${GREEN}https://nobel-order-system.streamlit.app${NC}"
echo ""
echo "=========================================="
echo ""

# 提供获取 Supabase 凭证的说明
echo -e "${BLUE}📝 如何获取 Supabase 凭证${NC}"
echo ""
echo "1. 访问 Supabase 控制台："
echo "   https://app.supabase.com/"
echo ""
echo "2. 选择你的项目"
echo ""
echo "3. 进入 'Settings' → 'API'"
echo ""
echo "4. 复制以下信息："
echo "   - Project URL"
echo "   - anon key"
echo "   - service_role key（仅用于服务端）"
echo ""
echo "=========================================="
echo ""

# 检查 Supabase 配置文件
if [ -f "config/supabase_config.json" ]; then
    echo -e "${BLUE}📄 检测到 Supabase 配置文件${NC}"
    echo ""
    echo "配置文件内容："
    echo ""
    cat config/supabase_config.json | head -20
    echo ""
    echo "=========================================="
    echo ""
fi

echo -e "${GREEN}✅ 部署准备完成！${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "  - Streamlit Cloud 会自动检测 requirements.txt 或 requirements.streamlit.txt"
echo "  - 首次部署可能需要 3-5 分钟"
echo "  - 后续推送代码会自动重新部署"
echo "  - 可以在 Streamlit Cloud 控制台查看部署日志"
echo ""
echo -e "${BLUE}📚 相关文档：${NC}"
echo "  - Streamlit Cloud 部署：docs/DEPLOY_STREAMLIT_CLOUD.md"
echo "  - 部署指南总结：docs/DEPLOYMENT_GUIDE.md"
echo "  - 快速使用教程：docs/QUICK_START_TUTORIAL.md"
echo ""
echo "=========================================="
echo ""
echo "祝您部署顺利！🚀"
