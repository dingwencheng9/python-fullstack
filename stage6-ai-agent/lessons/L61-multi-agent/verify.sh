#!/bin/bash

################################################################################
# L20: 多 Agent 协同编排 - 验证脚本
# 用途: 验证环境和依赖是否正确安装
################################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 主函数
main() {
    print_header "L20: 多 Agent 协同编排 - 环境验证"

    # 1. 检查 Python 版本
    print_header "步骤 1: 检查 Python 版本"

    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_info "Python 版本: $python_version"

    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"; then
        print_success "Python 版本满足要求 (>= 3.12)"
    else
        print_warning "推荐使用 Python 3.12+"
    fi

    # 2. 检查依赖包
    print_header "步骤 2: 检查依赖包"

    packages=(
        "langgraph"
        "langchain_core"
        "pandas"
        "opentelemetry"
        "pydantic"
        "pytest"
    )

    for package in "${packages[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            version=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null)
            print_success "$package ($version)"
        else
            print_error "$package 未安装"
            echo "  运行: pip install -r requirements.txt"
        fi
    done

    # 3. 检查核心文件
    print_header "步骤 3: 检查核心文件"

    files=(
        "agents.py"
        "workers.py"
        "orchestrator.py"
        "example.py"
        "test_agents.py"
        "__init__.py"
        "requirements.txt"
        "GUIDE.md"
    )

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            print_success "$file"
        else
            print_error "$file 缺失"
        fi
    done

    # 4. 检查基础设施
    print_header "步骤 4: 检查基础设施"

    # 检查 Docker
    if command -v docker &> /dev/null; then
        print_success "Docker 已安装"

        # 检查 Jaeger
        if docker ps | grep -q jaeger; then
            print_success "Jaeger 正在运行"
            print_info "  访问: http://localhost:16686"
        else
            print_warning "Jaeger 未运行"
            print_info "  启动: docker-compose -f ../../../docker-compose.infra.yml up -d jaeger"
        fi
    else
        print_warning "Docker 未安装"
    fi

    # 5. 语法检查
    print_header "步骤 5: 语法检查"

    for py_file in *.py; do
        if python3 -m py_compile "$py_file" 2>/dev/null; then
            print_success "$py_file 语法正确"
        else
            print_error "$py_file 语法错误"
        fi
    done

    # 6. 导入测试
    print_header "步骤 6: 导入测试"

    python3 << 'EOF'
import sys

try:
    from solutions.multi_agent.agents import SupervisorAgent, AgentRole, AgentMessage
    print("✅ agents 模块导入成功")
except Exception as e:
    print(f"❌ agents 模块导入失败: {e}")
    sys.exit(1)

try:
    from solutions.multi_agent.workers import DataAnalystAgent, KnowledgeAgent
    print("✅ workers 模块导入成功")
except Exception as e:
    print(f"❌ workers 模块导入失败: {e}")
    sys.exit(1)

try:
    from solutions.multi_agent.orchestrator import MultiAgentOrchestrator, run_multi_agent_query
    print("✅ orchestrator 模块导入成功")
except Exception as e:
    print(f"❌ orchestrator 模块导入失败: {e}")
    sys.exit(1)
EOF

    # 7. 快速功能测试
    print_header "步骤 7: 快速功能测试"

    python3 << 'EOF'
import asyncio
from solutions.multi_agent.agents import SupervisorAgent, AgentState, TaskStatus

async def test():
    supervisor = SupervisorAgent()

    state = {
        "user_query": "测试查询",
        "task_id": "test",
        "task_plan": [],
        "current_task_index": 0,
        "messages": [],
        "current_message": None,
        "tool_results": {},
        "final_answer": None,
        "status": TaskStatus.PENDING,
        "error": None,
        "trace_id": "test_trace",
        "iteration_count": 0
    }

    tasks = await supervisor.plan_tasks("分析数据并检索知识", state)

    if len(tasks) >= 2:
        print("✅ Supervisor 任务规划正常")
    else:
        print("❌ Supervisor 任务规划失败")

asyncio.run(test())
EOF

    # 完成
    print_header "验证完成"

    print_success "所有验证完成"
    print_info ""
    print_info "下一步:"
    print_info "  1. 查看使用指南: cat GUIDE.md"
    print_info "  2. 运行示例: python example.py"
    print_info "  3. 运行测试: pytest test_agents.py -v"
    print_info "  4. 查看 Jaeger UI: http://localhost:16686"
    print_info ""
}

# 执行
main

exit 0
