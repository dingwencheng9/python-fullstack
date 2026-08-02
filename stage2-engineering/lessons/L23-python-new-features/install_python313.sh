#!/bin/bash
# install_python313.sh
# L06 Python 3.13 环境安装脚本

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐍 L06 Python 3.13 体验环境安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 定义变量
L06_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_VERSION="3.13.0"

# 检查函数
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 已安装${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 未安装${NC}"
        return 1
    fi
}

# 步骤 1: 检查前置条件
echo "📋 步骤 1/5: 检查前置条件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查当前 Python 版本
CURRENT_PYTHON=$(python --version 2>&1)
echo "当前 Python 版本: $CURRENT_PYTHON"

if [[ ! $CURRENT_PYTHON == *"3.12"* ]]; then
    echo -e "${YELLOW}⚠️  警告: 主环境不是 Python 3.12${NC}"
    echo "建议在 Python 3.12 环境下运行此脚本"
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查磁盘空间
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "可用磁盘空间: $AVAILABLE_SPACE"

# 检查 L06 目录
if [ ! -d "$L06_DIR" ]; then
    echo -e "${RED}❌ 错误: L06 目录不存在${NC}"
    echo "路径: $L06_DIR"
    exit 1
fi

echo -e "${GREEN}✅ 前置条件检查通过${NC}"
echo ""

# 步骤 2: 安装 pyenv（如果需要）
echo "📦 步骤 2/5: 安装 pyenv"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v pyenv &> /dev/null; then
    echo -e "${GREEN}✅ pyenv 已安装${NC}"
    pyenv --version
else
    echo "正在安装 pyenv..."

    # 安装 pyenv
    curl https://pyenv.run | bash

    # 配置环境变量
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"

    # 添加到 shell 配置
    SHELL_CONFIG="$HOME/.zshrc"
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    fi

    if ! grep -q "PYENV_ROOT" "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo "# pyenv configuration" >> "$SHELL_CONFIG"
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$SHELL_CONFIG"
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> "$SHELL_CONFIG"
        echo 'eval "$(pyenv init --path)"' >> "$SHELL_CONFIG"
        echo 'eval "$(pyenv init -)"' >> "$SHELL_CONFIG"

        echo -e "${GREEN}✅ pyenv 配置已添加到 $SHELL_CONFIG${NC}"
    fi

    echo -e "${GREEN}✅ pyenv 安装完成${NC}"
fi

echo ""

# 步骤 3: 安装 Python 3.13
echo "🐍 步骤 3/5: 安装 Python 3.13"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if pyenv versions 2>/dev/null | grep -q "$PYTHON_VERSION"; then
    echo -e "${GREEN}✅ Python $PYTHON_VERSION 已安装${NC}"
else
    echo "正在安装 Python $PYTHON_VERSION..."
    echo "⏱️  预计时间: 5-10 分钟（首次编译）"
    echo "💾 磁盘空间: ~200MB"
    echo ""

    # 安装编译依赖（macOS）
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "检查编译依赖..."
        if command -v brew &> /dev/null; then
            brew install openssl readline sqlite3 xz zlib 2>/dev/null || true
        fi
    fi

    # 安装 Python 3.13
    pyenv install $PYTHON_VERSION

    echo -e "${GREEN}✅ Python $PYTHON_VERSION 安装完成${NC}"
fi

echo ""

# 步骤 4: 创建 L06 虚拟环境
echo "📁 步骤 4/5: 创建 L06 虚拟环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$L06_DIR"

# 设置 Python 版本
echo "设置 L06 目录使用 Python $PYTHON_VERSION..."
pyenv local $PYTHON_VERSION

# 创建虚拟环境
if [ -d ".venv313" ]; then
    echo -e "${YELLOW}⚠️  虚拟环境已存在，删除旧环境...${NC}"
    rm -rf .venv313
fi

echo "创建虚拟环境..."
python -m venv .venv313

# 激活虚拟环境
source .venv313/bin/activate

# 验证版本
VENV_PYTHON=$(python --version 2>&1)
echo "虚拟环境 Python 版本: $VENV_PYTHON"

if [[ ! $VENV_PYTHON == *"3.13"* ]]; then
    echo -e "${RED}❌ 错误: 虚拟环境 Python 版本不是 3.13${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 虚拟环境创建成功${NC}"
echo ""

# 步骤 5: 安装依赖
echo "📦 步骤 5/5: 安装依赖"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip -q

# 安装依赖
if [ -f "requirements.txt" ]; then
    echo "从 requirements.txt 安装依赖..."
    pip install -r requirements.txt -q
elif [ -f "pyproject.toml" ]; then
    echo "从 pyproject.toml 安装依赖..."
    pip install -e . -q
fi

# 安装测试依赖
echo "安装测试依赖..."
pip install pytest pytest-cov -q

echo -e "${GREEN}✅ 依赖安装完成${NC}"
echo ""

# 运行测试验证
echo "🧪 运行测试验证环境..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pytest tests/ -v --tb=short || true

echo ""

# 完成报告
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 L06 Python 3.13 环境安装完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 安装信息:"
echo "  ✅ Python 版本: $(python --version)"
echo "  ✅ 虚拟环境: $L06_DIR/.venv313"
echo "  ✅ pyenv 位置: $(which pyenv)"
echo ""
echo "🚀 开始体验 L06:"
echo ""
echo "  # 1. 进入 L06 目录"
echo "  cd $L06_DIR"
echo ""
echo "  # 2. 激活虚拟环境"
echo "  source .venv313/bin/activate"
echo ""
echo "  # 3. 验证 Python 版本"
echo "  python --version  # 应显示 Python 3.13.x"
echo ""
echo "  # 4. 运行测试（所有测试应通过）"
echo "  pytest tests/ -v"
echo ""
echo "  # 5. 体验彩色错误提示"
echo "  python demos/01-colored-traceback.py"
echo ""
echo "  # 6. 体验改进的 REPL"
echo "  python  # 进入 Python 3.13 REPL"
echo ""
echo "  # 7. 运行性能对比"
echo "  python demos/03-performance-test.py"
echo ""
echo "  # 8. 完成练习"
echo "  python exercises/01-error-handling.py"
echo "  python exercises/02-interactive-debug.py"
echo "  python exercises/03-benchmark.py"
echo ""
echo "🧹 体验完成后清理:"
echo ""
echo "  # 退出虚拟环境"
echo "  deactivate"
echo ""
echo "  # 运行清理脚本"
echo "  ./cleanup_python313.sh"
echo ""
echo "📚 更多信息:"
echo "  查看 L06_PYTHON313_ENV_GUIDE.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
