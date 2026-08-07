#!/bin/bash

# ============================================================
# AI Agent Chat API V2 - 端到端测试脚本
# ============================================================
# 用途: 验证完整流程（创建 Thread → 发送消息 → 流式响应）
# 创建日期: 2026-06-07
# ============================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置
API_URL="${API_URL:-http://localhost:8000}"
JWT_TOKEN="${JWT_TOKEN:-demo-token}"

# 输出函数
print_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ============================================================
# 测试 1: 健康检查
# ============================================================

test_health_check() {
    print_header "测试 1: 健康检查"

    print_info "请求: GET ${API_URL}/health"

    response=$(curl -s -w "\n%{http_code}" "${API_URL}/health")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "健康检查通过"
        echo "$body" | jq '.'
    else
        print_error "健康检查失败 (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
}

# ============================================================
# 测试 2: 创建新会话并发送消息（非流式）
# ============================================================

test_create_conversation() {
    print_header "测试 2: 创建新会话（非流式）"

    print_info "请求: POST ${API_URL}/api/v2/agent/chat"
    print_info "参数: stream=false (非流式，便于测试)"

    response=$(curl -s -w "\n%{http_code}" \
        -X POST "${API_URL}/api/v2/agent/chat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${JWT_TOKEN}" \
        -d '{
            "message": "你好，这是测试消息",
            "stream": false,
            "include_history": true
        }')

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "会话创建成功"

        # 提取 thread_id
        THREAD_ID=$(echo "$body" | jq -r '.thread_id')

        if [ -n "$THREAD_ID" ] && [ "$THREAD_ID" != "null" ]; then
            print_success "Thread ID: $THREAD_ID"
            echo "$body" | jq '.'

            # 保存 thread_id 供后续测试使用
            echo "$THREAD_ID" > /tmp/agent_test_thread_id.txt
        else
            print_error "未返回 thread_id"
            exit 1
        fi
    else
        print_error "会话创建失败 (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
}

# ============================================================
# 测试 3: 查看会话列表
# ============================================================

test_list_conversations() {
    print_header "测试 3: 查看会话列表"

    print_info "请求: GET ${API_URL}/api/v2/agent/conversations"

    response=$(curl -s -w "\n%{http_code}" \
        -X GET "${API_URL}/api/v2/agent/conversations?limit=10" \
        -H "Authorization: Bearer ${JWT_TOKEN}")

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "会话列表获取成功"

        # 统计会话数
        count=$(echo "$body" | jq '.conversations | length')
        print_info "找到 $count 个会话"

        echo "$body" | jq '.'
    else
        print_error "会话列表获取失败 (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
}

# ============================================================
# 测试 4: 查看会话详情
# ============================================================

test_get_conversation_detail() {
    print_header "测试 4: 查看会话详情"

    # 读取之前保存的 thread_id
    if [ ! -f /tmp/agent_test_thread_id.txt ]; then
        print_error "未找到 thread_id，请先运行测试 2"
        exit 1
    fi

    THREAD_ID=$(cat /tmp/agent_test_thread_id.txt)

    print_info "请求: GET ${API_URL}/api/v2/agent/conversations/${THREAD_ID}"

    response=$(curl -s -w "\n%{http_code}" \
        -X GET "${API_URL}/api/v2/agent/conversations/${THREAD_ID}" \
        -H "Authorization: Bearer ${JWT_TOKEN}")

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "会话详情获取成功"

        # 统计消息数
        message_count=$(echo "$body" | jq '.messages | length')
        print_info "会话包含 $message_count 条消息"

        echo "$body" | jq '.'
    else
        print_error "会话详情获取失败 (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
}

# ============================================================
# 测试 5: 继续对话（加载历史）
# ============================================================

test_continue_conversation() {
    print_header "测试 5: 继续对话（加载历史）"

    # 读取 thread_id
    if [ ! -f /tmp/agent_test_thread_id.txt ]; then
        print_error "未找到 thread_id，请先运行测试 2"
        exit 1
    fi

    THREAD_ID=$(cat /tmp/agent_test_thread_id.txt)

    print_info "请求: POST ${API_URL}/api/v2/agent/chat"
    print_info "Thread ID: $THREAD_ID"
    print_info "参数: include_history=true (加载历史)"

    response=$(curl -s -w "\n%{http_code}" \
        -X POST "${API_URL}/api/v2/agent/chat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${JWT_TOKEN}" \
        -d "{
            \"message\": \"继续对话，询问 Python 异步编程\",
            \"thread_id\": \"${THREAD_ID}\",
            \"stream\": false,
            \"include_history\": true
        }")

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "对话继续成功（历史已加载）"

        # 检查 Token 统计
        total_tokens=$(echo "$body" | jq '.token_statistics.total_tokens')
        print_info "当前 Token 总数: $total_tokens"

        echo "$body" | jq '.'
    else
        print_error "对话继续失败 (HTTP $http_code)"
        echo "$body"
        exit 1
    fi
}

# ============================================================
# 测试 6: 流式响应（SSE）
# ============================================================

test_streaming_response() {
    print_header "测试 6: 流式响应（SSE）"

    print_info "请求: POST ${API_URL}/api/v2/agent/chat (流式)"
    print_info "提示: 观察 SSE 事件流（前 20 个事件）"

    # 使用 curl 的 --no-buffer 选项实时输出
    curl -s --no-buffer \
        -X POST "${API_URL}/api/v2/agent/chat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${JWT_TOKEN}" \
        -d '{
            "message": "测试流式响应",
            "stream": true,
            "include_history": false
        }' | head -n 20

    echo ""
    print_success "流式响应测试完成（仅显示前 20 行）"
}

# ============================================================
# 测试 7: Token 压缩测试（模拟大量消息）
# ============================================================

test_token_compression() {
    print_header "测试 7: Token 压缩（模拟大量消息）"

    print_info "创建新会话并发送多条消息..."

    # 创建新会话
    response=$(curl -s -w "\n%{http_code}" \
        -X POST "${API_URL}/api/v2/agent/chat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${JWT_TOKEN}" \
        -d '{
            "message": "第一条消息：初始化会话",
            "stream": false
        }')

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -ne 200 ]; then
        print_error "会话创建失败"
        exit 1
    fi

    THREAD_ID=$(echo "$body" | jq -r '.thread_id')
    print_success "新会话已创建: $THREAD_ID"

    # 发送 10 条消息（模拟对话历史积累）
    print_info "发送 10 条消息..."

    for i in {2..10}; do
        curl -s \
            -X POST "${API_URL}/api/v2/agent/chat" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${JWT_TOKEN}" \
            -d "{
                \"message\": \"第 ${i} 条消息：这是一条较长的消息，用于累积 Token 数。内容包含多个句子，以便更快触发压缩阈值。\",
                \"thread_id\": \"${THREAD_ID}\",
                \"stream\": false,
                \"include_history\": true
            }" > /dev/null

        echo -n "."
    done

    echo ""
    print_success "10 条消息已发送"

    # 查看会话详情（检查 Token 统计）
    print_info "查看 Token 统计..."

    response=$(curl -s \
        -X GET "${API_URL}/api/v2/agent/conversations/${THREAD_ID}" \
        -H "Authorization: Bearer ${JWT_TOKEN}")

    total_tokens=$(echo "$response" | jq '.conversation.total_tokens')
    total_messages=$(echo "$response" | jq '.conversation.total_messages')

    print_info "总消息数: $total_messages"
    print_info "总 Token 数: $total_tokens"

    if [ "$total_tokens" -gt 8000 ]; then
        print_success "Token 数超过阈值，应触发压缩"
    else
        print_info "Token 数未超过阈值（8000），未触发压缩"
    fi
}

# ============================================================
# 主测试流程
# ============================================================

main() {
    print_header "AI Agent Chat API V2 - 端到端测试"

    print_info "API 地址: $API_URL"
    print_info "JWT Token: $JWT_TOKEN"

    # 检查依赖
    if ! command -v curl &> /dev/null; then
        print_error "curl 未安装"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        print_error "jq 未安装（用于解析 JSON）"
        print_info "安装: brew install jq (macOS) 或 apt install jq (Linux)"
        exit 1
    fi

    # 运行测试
    test_health_check
    test_create_conversation
    test_list_conversations
    test_get_conversation_detail
    test_continue_conversation
    test_streaming_response
    test_token_compression

    # 总结
    print_header "测试完成"
    print_success "所有测试通过！🎉"

    echo ""
    echo -e "${CYAN}快速验证命令:${NC}"
    echo -e "${YELLOW}健康检查:${NC} curl ${API_URL}/health"
    echo -e "${YELLOW}API 文档:${NC} ${API_URL}/docs"
    echo -e "${YELLOW}Jaeger UI:${NC} http://localhost:16686"
    echo ""
}

# 运行主函数
main
