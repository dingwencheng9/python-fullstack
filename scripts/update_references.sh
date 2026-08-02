#!/bin/bash
# 更新所有 P → S 引用

cd /Users/nexo/python-fullstack

echo "=== 更新 Stage S 引用 ==="

# 1. 更新 stageS-web-scraping/README.md
sed -i '' 's/Stage P:/Stage S:/g' stageS-web-scraping/README.md
sed -i '' 's/P01-P09/S01-S09/g' stageS-web-scraping/README.md
sed -i '' 's/P01/P01-S01/g; s/P02/P02-S02/g; s/P03/P03-S03/g; s/P04/P04-S04/g; s/P05/P05-S05/g; s/P06/P06-S06/g; s/P07/P07-S07/g; s/P08/P08-S08/g; s/P09/P09-S09/g' stageS-web-scraping/README.md
sed -i '' 's/L01-L09/L01-L10/g' stageS-web-scraping/README.md

echo "✓ stageS-web-scraping/README.md"

# 2. 更新课程 README.md 文件
for dir in stageS-web-scraping/lessons/S*/; do
    # 更新课程编号
    sed -i '' 's/> \*\*课程编号\*\*: P/P/g' "$dir"*/README.md 2>/dev/null
    sed -i '' 's/> \*\*前置课程\*\*: P/> \*\*前置课程\*\*: S/g' "$dir"*/README.md 2>/dev/null

    # 更新内部链接
    sed -i '' 's/P01/S01/g; s/P02/S02/g; s/P03/S03/g; s/P04/S04/g; s/P05/S05/g; s/P06/S06/g; s/P07/S07/g; s/P08/S08/g; s/P09/S09/g' "$dir"*/README.md 2>/dev/null
    sed -i '' 's/P01/S01/g; s/P02/S02/g; s/P03/S03/g; s/P04/S04/g; s/P05/S05/g; s/P06/S06/g; s/P07/S07/g; s/P08/S08/g; s/P09/S09/g' "$dir"*/lesson.md 2>/dev/null
done

echo "✓ 课程 README/lesson.md 文件"

# 3. 更新 Stage 0 课程文件中的旧引用
cd stage0-python-basics/lessons

# L04-functions-modules
sed -i '' 's/L05-file-operations/L06-file-operations/g; s/L05-debugging/L05-debugging/g' L04-functions-modules/lesson.md
sed -i '' 's/L05-file-operations/L06-file-operations/g' L04-functions-modules/README.md

# L05-debugging-tools (原 L04.5)
sed -i '' 's/L04.5/L05/g; s/L05-debugging/L05-debugging/g; s/L05-file-operations/L06-file-operations/g' L05-debugging-tools/lesson.md
sed -i '' 's/L04.5/L05/g; s/L05-file-operations/L06-file-operations/g' L05-debugging-tools/README.md
sed -i '' 's/L04.5/L05/g' L05-debugging-tools/examples/*.py
sed -i '' 's/L04.5/L05/g' L05-debugging-tools/exercises/*.py
sed -i '' 's/L04.5/L05/g' L05-debugging-tools/solutions/*.py
sed -i '' 's/L04.5/L05/g' L05-debugging-tools/tests/*.py

# L06-file-operations (原 L05)
sed -i '' 's/L05-file-operations/L06-file-operations/g; s/L05-debugging-tools/L05-debugging-tools/g' L06-file-operations/lesson.md
sed -i '' 's/L05-file-operations/L06-file-operations/g; s/L05-debugging/L05-debugging/g' L06-file-operations/README.md
sed -i '' 's/L05-file-operations/L06-file-operations/g' L06-file-operations/tests/README.md

# L07-oop-basics (原 L06)
sed -i '' 's/L06-oop-basics/L07-oop-basics/g; s/L05-file-operations/L06-file-operations/g' L07-oop-basics/lesson.md
sed -i '' 's/L06-oop-basics/L07-oop-basics/g; s/L05/L06/g' L07-oop-basics/README.md

# L08-magic-methods (原 L07)
sed -i '' 's/L07-magic-methods/L08-magic-methods/g; s/L06-oop-basics/L07-oop-basics/g' L08-magic-methods/lesson.md
sed -i '' 's/L07-magic-methods/L08-magic-methods/g; s/L06/L07/g' L08-magic-methods/README.md

# L09-exceptions (原 L08)
sed -i '' 's/L08-exceptions/L09-exceptions/g; s/L07-magic-methods/L08-magic-methods/g' L09-exceptions/lesson.md
sed -i '' 's/L08-exceptions/L09-exceptions/g; s/L07/L08/g' L09-exceptions/README.md
sed -i '' 's/L09-basics-project/L10-basics-project/g' L09-exceptions/README.md

# L10-basics-project (原 L09)
sed -i '' 's/L09-basics-project/L10-basics-project/g; s/L08-exceptions/L09-exceptions/g' L10-basics-project/lesson.md
sed -i '' 's/L09-basics-project/L10-basics-project/g; s/L08/L09/g' L10-basics-project/README.md
sed -i '' 's/L09-basics-project/L10-basics-project/g' L10-basics-project/tests/README.md
sed -i '' 's/L09-basics-project/L10-basics-project/g' L10-basics-project/exercises/README.md
sed -i '' 's/L09-basics-project/L10-basics-project/g' L10-basics-project/examples/README.md

echo "✓ Stage 0 课程文件"

# 4. 更新根目录文档
cd /Users/nexo/python-fullstack
sed -i '' 's/L04.5-dev-tools-debugging/L05-debugging-tools/g' COURSE_MAPPING.md
sed -i '' 's/L05-file-operations/L06-file-operations/g' COURSE_MAPPING.md
sed -i '' 's/L06-oop-basics/L07-oop-basics/g' COURSE_MAPPING.md
sed -i '' 's/L07-magic-methods/L08-magic-methods/g' COURSE_MAPPING.md
sed -i '' 's/L08-exceptions/L09-exceptions/g' COURSE_MAPPING.md
sed -i '' 's/L09-basics-project/L10-basics-project/g' COURSE_MAPPING.md
sed -i '' 's/L04.5/L05/g; s/stageP/stageS/g; s/P01/S01/g; s/P02/S02/g; s/P03/S03/g; s/P04/S04/g; s/P05/S05/g; s/P06/S06/g; s/P07/S07/g; s/P08/S08/g; s/P09/S09/g' COURSE_MAPPING.md

echo "✓ COURSE_MAPPING.md"

# 5. 更新 docs/knowledge/ 文件
cd /Users/nexo/python-fullstack/docs/knowledge

# 更新 COURSE_KNOWLEDGE_MAP.md
sed -i '' 's/Stage P/Stage S/g; s/P01/S01/g; s/P02/S02/g; s/P03/S03/g; s/P04/S04/g; s/P05/S05/g; s/P06/S06/g; s/P07/S07/g; s/P08/S08/g; s/P09/S09/g; s/L04.5/L05/g; s/L05-file/L06-file/g; s/L06-oop/L07-oop/g; s/L07-magic/L08-magic/g; s/L08-exception/L09-exception/g; s/L09-basics/L10-basics/g' COURSE_KNOWLEDGE_MAP.md

echo "✓ docs/knowledge/COURSE_KNOWLEDGE_MAP.md"

# 更新 KNOWLEDGE_INVENTORY.md
sed -i '' 's/L04.5/L05/g; s/L05-file/L06-file/g; s/L06-oop/L07-oop/g; s/L07-magic/L08-magic/g; s/L08-exception/L09-exception/g; s/L09-basics/L10-basics/g' KNOWLEDGE_INVENTORY.md

echo "✓ docs/knowledge/KNOWLEDGE_INVENTORY.md"

# 更新 KNOWLEDGE_DAG.md
sed -i '' 's/L04_5/L05/g; s/L04.5/L05/g; s/L05/L05/g' KNOWLEDGE_DAG.md

echo "✓ docs/knowledge/KNOWLEDGE_DAG.md"

echo ""
echo "=== 更新完成 ==="
