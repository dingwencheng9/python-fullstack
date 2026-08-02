# Git 进阶操作示例

## G.1 git rebase 示例

```bash
# === 基础 rebase ===
# 场景：将 feature 分支变基到 main
git checkout feature
git rebase main

# === 交互式 rebase（压缩历史）===
# 假设有 3 个连续的工作进度提交
# commit abc: WIP
# commit def: WIP
# commit ghi: 完成功能

git rebase -i HEAD~3
# 编辑器打开：
# pick abc123 WIP
# pick def456 WIP
# pick ghi789 完成功能
# 改为：
# pick abc123 WIP
# squash def456 WIP
# squash ghi789 完成功能
# 结果：合并为 1 个有意义的提交

# === rebase --onto ===
# 场景：将 feature 的 3 个提交变基到 main 上
git rebase --onto main feature~3 feature
```

## G.2 merge vs rebase 对比

```bash
# === merge（保留完整历史）===
git checkout main
git merge feature/login
# 产生 merge commit，历史保留完整分支结构

# === rebase（线性历史）===
git checkout feature
git rebase main
# 历史线性，但会重写提交（不要对已推送的提交 rebase）
```

## G.3 git cherry-pick 示例

```bash
# === 应用单个提交 ===
git cherry-pick abc123

# === 应用多个提交 ===
git cherry-pick abc123 def456

# === 处理冲突后继续 ===
git cherry-pick --continue
# 或放弃
git cherry-pick --abort

# === 场景：backport 修复到旧版本 ===
git checkout v1.0
git cherry-pick abc123  # 将修复提交 cherry-pick 到 v1.0 分支
```

## G.4 git reflog 示例

```bash
# === 查看 reflog ===
git reflog
# 输出：
# abc123 HEAD@{0}: commit: feat: add feature X
# def456 HEAD@{1}: rebase: 修复冲突
# ghi789 HEAD@{2}: checkout: 切换到 feature

# === 恢复误删的提交 ===
git checkout HEAD@{1}  # 恢复到冲突前状态

# === 基于 reflog 恢复分支 ===
git branch recovery-branch HEAD@{5}

# === 恢复硬重置丢失的提交 ===
git reset --hard abc123  # 误操作
git reflog  # 找到原来的 HEAD
git reset --hard HEAD@{1}  # 恢复到操作前
```

## G.5 git bisect 示例

```bash
# === 手动 bisect ===
git bisect start
git bisect good v1.0.0      # 标记好版本
git bisect bad HEAD         # 标记当前有 bug
# Git 自动 checkout 中间版本
# 测试后标记
git bisect good  # 或 git bisect bad
# 重复直到找到第一个坏提交

# === 自动 bisect ===
git bisect start
git bisect good v1.0.0
git bisect bad HEAD
git bisect run pytest tests/test_feature.py
# 自动运行测试，输出第一个坏提交

# === 结束 bisect ===
git bisect reset
```

## G.6 git stash 示例

```bash
# === 基本 stash ===
git stash
# 工作区干净，可以切换分支

# === stash 并添加描述 ===
git stash push -m "WIP: 新功能开发中"

# === 查看 stash 列表 ===
git stash list
# stash@{0}: WIP: 新功能开发中
# stash@{1}: On main: feat: add feature X

# === 恢复并删除 stash ===
git stash pop  # 推荐，弹栈

# === 恢复但不删除 ===
git stash apply stash@{1}

# === 查看 stash 内容 ===
git stash show -p stash@{0}

# === 删除 stash ===
git stash drop stash@{0}

# === 包含未跟踪文件 ===
git stash -u

# === 清空所有 stash ===
git stash clear
```

## G.7 实际工作流组合

```bash
# === 场景：功能开发中途需要修 bug ===
git stash                    # 1. 保存当前工作
git checkout main
git pull
git checkout -b fix/bug-123  # 2. 创建修复分支
# ... 修复 bug 并提交 ...
git checkout feature/my-feat # 3. 切回原分支
git rebase main              # 4. 变基到最新 main
git stash pop                # 5. 恢复工作进度

# === 场景：rebase 冲突处理 ===
git rebase main
# 冲突时：
# 1. 解决冲突文件
# 2. git add <file>
# 3. git rebase --continue
# 或放弃：git rebase --abort
```

## G.8 常用 Git 别名（提升效率）

```bash
# ~/.gitconfig 中配置
git config --global alias.st "status -sb"
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --decorate"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "reset HEAD --"
```
