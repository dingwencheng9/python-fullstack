#!/bin/bash
# Stage 0 重编号脚本
# L04.5 → L05, L05 → L06, ..., L09 → L10

set -e

LESSONS_DIR="/Users/nexo/python-fullstack/stage0-python-basics/lessons"

echo "=== Stage 0 课程重编号 ==="

# 定义重命名映射 (旧名称 → 新名称)
declare -A RENAME_MAP=(
    ["L04.5-dev-tools-debugging"]="L05-debugging-tools"
    ["L05-file-operations"]="L06-file-operations"
    ["L06-oop-basics"]="L07-oop-basics"
    ["L07-magic-methods"]="L08-magic-methods"
    ["L08-exceptions"]="L09-exceptions"
    ["L09-basics-project"]="L10-basics-project"
)

# 执行重命名
for old_name in "${!RENAME_MAP[@]}"; do
    new_name="${RENAME_MAP[$old_name]}"
    old_path="$LESSONS_DIR/$old_name"
    new_path="$LESSONS_DIR/$new_name"

    if [ -d "$old_path" ]; then
        echo "Renaming: $old_name → $new_name"
        mv "$old_path" "$new_path"
    else
        echo "WARNING: $old_path not found, skipping"
    fi
done

echo ""
echo "=== 重命名完成 ==="
ls -la "$LESSONS_DIR"
