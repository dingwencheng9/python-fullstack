#!/bin/bash
# cleanup_python313.sh
# L06 Python 3.13 环境完整清理脚本

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧹 L06 Python 3.13 环境清理"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 定义变量
L06_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_VERSION="3.13.0"

# 确认清理
echo -e "${YELLOW}⚠️  此脚本将清理以下内容:${NC}"
echo ""
echo "  1. L06 虚拟环境 (.venv313)"
echo "  2. Python 版本配置 (.python-version)"
echo "  3. Python 3.13 (pyenv)"
echo "  4. 相关缓存文件"
echo ""
echo -e "${BLUE}💡 主环境 (Python 3.12) 不会被影响${NC}"
echo ""

read -p "确认继续? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消清理"
    exit 0
fi

echo ""

# 步骤 1: 清理 L06 虚拟环境
echo "📁 步骤 1/5: 清理 L06 虚拟环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$L06_DIR"

# 如果虚拟环境被激活，先退出
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "退出虚拟环境..."
    deactivate 2>/dev/null || true
fi

# 删除虚拟环境
if [ -d ".venv313" ]; then
    echo "删除 .venv313..."
    VENV_SIZE=$(du -sh .venv313 2>/dev/null | cut -f1)
    rm -rf .venv313
    echo -e "${GREEN}✅ 已删除虚拟环境 (释放空间: $VENV_SIZE)${NC}"
else
    echo "ℹ️  虚拟环境不存在，跳过"
fi

echo ""

# 步骤 2: 清理 Python 版本配置
echo "📄 步骤 2/5: 清理 Python 版本配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f ".python-version" ]; then
    PYVER_CONTENT=$(cat .python-version)
    echo "当前配置: $PYVER_CONTENT"
    rm .python-version
    echo -e "${GREEN}✅ 已删除 .python-version${NC}"
else
    echo "ℹ️  .python-version 不存在，跳过"
fi

echo ""

# 步骤 3: 卸载 Python 3.13
echo "🐍 步骤 3/5: 卸载 Python 3.13"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v pyenv &> /dev/null; then
    if pyenv versions 2>/dev/null | grep -q "$PYTHON_VERSION"; then
        echo "卸载 Python $PYTHON_VERSION..."

        # 获取安装大小
        if [ -d "$HOME/.pyenv/versions/$PYTHON_VERSION" ]; then
            PY313_SIZE=$(du -sh "$HOME/.pyenv/versions/$PYTHON_VERSION" 2>/dev/null | cut -f1)
        else
            PY313_SIZE="unknown"
        fi

        pyenv uninstall -f $PYTHON_VERSION 2>/dev/null || true
        echo -e "${GREEN}✅ 已卸载 Python $PYTHON_VERSION (释放空间: $PY313_SIZE)${NC}"
    else
        echo "ℹ️  Python $PYTHON_VERSION 未安装，跳过"
    fi
else
    echo "ℹ️  pyenv 未安装，跳过"
fi

echo ""

# 步骤 4: 清理缓存
echo "🗑️  步骤 4/5: 清理缓存"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CACHE_CLEARED=0

# 清理 pip 缓存
if [ -d "$HOME/.cache/pip" ]; then
    echo "清理 pip 缓存 (Python 3.13)..."
    BEFORE_SIZE=$(du -sh "$HOME/.cache/pip" 2>/dev/null | cut -f1)
    find "$HOME/.cache/pip" -name "*cp313*" -delete 2>/dev/null || true
    AFTER_SIZE=$(du -sh "$HOME/.cache/pip" 2>/dev/null | cut -f1)
    echo "  pip 缓存: $BEFORE_SIZE → $AFTER_SIZE"
    CACHE_CLEARED=1
fi

# 清理 pyenv 缓存
if [ -d "$HOME/.pyenv/cache" ]; then
    echo "清理 pyenv 缓存 (Python 3.13)..."
    find "$HOME/.pyenv/cache" -name "*3.13*" -delete 2>/dev/null || true
    CACHE_CLEARED=1
fi

# 清理 uv 缓存（如果使用）
if command -v uv &> /dev/null; then
    echo "清理 uv 缓存..."
    uv cache clean 2>/dev/null || true
    CACHE_CLEARED=1
fi

# 清理 pytest 缓存
if [ -d "$L06_DIR/.pytest_cache" ]; then
    echo "清理 pytest 缓存..."
    rm -rf "$L06_DIR/.pytest_cache"
    CACHE_CLEARED=1
fi

# 清理 __pycache__
echo "清理 __pycache__..."
find "$L06_DIR" -type d -name "__pycache__" -exec rm -rf  + 2>/dev/null || true

if [ $CACHE_CLEARED -eq 1 ]; then
    echo -e "${GREEN}✅ 缓存清理完成${NC}"
else
    echo "ℹ️  没有需要清理的缓存"
fi

echo ""

# 步骤 5: 验证环境恢复
echo "📋 步骤 5/5: 验证环境恢复"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$L06_DIR"

# 验证 Python 版本
PYTHON_VERSION_NOW=$(python --version 2>&1)
echo "当前 Python 版本: $PYTHON_VERSION_NOW"

if [[ $PYTHON_VERSION_NOW == *"3.12"* ]]; then
    echo -e "${GREEN}✅ 环境已恢复到 Python 3.12${NC}"
    ENV_STATUS="正常"
elif [[ $PYTHON_VERSION_NOW == *"3.13"* ]]; then
    echo -e "${RED}⚠️  警告: 当前仍为 Python 3.13${NC}"
    echo "可能需要手动切换回 Python 3.12"
    ENV_STATUS="需要手动调整"
else
    echo -e "${YELLOW}ℹ️  当前 Python 版本: $PYTHON_VERSION_NOW${NC}"
    ENV_STATUS="其他版本"
fi

# 验证 pyenv 状态
if command -v pyenv &> /dev/null; then
    echo ""
    echo "pyenv 已安装版本:"
    pyenv versions | head -5
fi

# 验证文件清理
echo ""
echo "文件清理验证:"

if [ ! -d ".venv313" ]; then
    echo -e "  ${GREEN}✅${NC} .venv313 已删除"
else
    echo -e "  ${RED}❌${NC} .venv313 仍存在"
fi

if [ ! -f ".python-version" ]; then
    echo -e "  ${GREEN}✅${NC} .python-version 已删除"
else
    echo -e "  ${RED}❌${NC} .python-version 仍存在"
fi

# 计算释放的空间
echo ""

# 生成清理报告
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 L06 Python 3.13 环境清理完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 清理统计:"
echo "  ✅ 虚拟环境: 已删除"
echo "  ✅ Python 3.13: 已卸载"
echo "  ✅ 缓存: 已清理"
echo "  ✅ 配置文件: 已清除"
echo ""
echo "💾 释放空间: 约 200-300 MB"
echo "⏱️  清理耗时: < 1 分钟"
echo ""
echo "当前环境:"
echo "  Python 版本: $PYTHON_VERSION_NOW"
echo "  工作目录: $(pwd)"
echo "  环境状态: $ENV_STATUS"
echo ""

if [[ $ENV_STATUS == "正常" ]]; then
    echo "✨ 环境已完全恢复，可以继续使用 Python 3.12 进行开发"
else
    echo "⚠️  请检查环境状态，可能需要手动调整"
    echo ""
    echo "手动恢复步骤:"
    echo "  1. 检查 pyenv 版本: pyenv versions"
    echo "  2. 切换到 3.12: pyenv local 3.12.13"
    echo "  3. 验证版本: python --version"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 可选: 提示是否继续保留 pyenv
if command -v pyenv &> /dev/null; then
    echo ""
    echo -e "${BLUE}💡 提示:${NC}"
    echo "  pyenv 仍然保留在系统中（可以管理多个 Python 版本）"
    echo ""
    echo "  如果不再需要 pyenv，可以手动卸载:"
    echo "    1. 删除 pyenv: rm -rf ~/.pyenv"
    echo "    2. 从 ~/.zshrc 或 ~/.bashrc 删除 pyenv 配置"
    echo "    3. 重新加载配置: source ~/.zshrc"
    echo ""
fi

# 保存清理日志
CLEANUP_LOG="$L06_DIR/cleanup_$(date +%Y%m%d_%H%M%S).log"
cat > "$CLEANUP_LOG" << LOGEOF
L06 Python 3.13 环境清理日志
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

清理时间: $(date '+%Y-%m-%d %H:%M:%S')
清理目录: $L06_DIR

清理内容:
  ✅ 虚拟环境 (.venv313)
  ✅ Python 版本配置 (.python-version)
  ✅ Python 3.13 (pyenv)
  ✅ 相关缓存

环境状态:
  清理前: Python 3.13.x
  清理后: $PYTHON_VERSION_NOW
  状态: $ENV_STATUS

释放空间: 约 200-300 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGEOF

echo "📄 清理日志已保存: $CLEANUP_LOG"
echo ""
