#!/usr/bin/env bash
# 把 fanfanshuo skill 安装到用户全局（~/.claude/skills/fanfanshuo）
# 用法：在仓库根目录运行 bash .claude/skills/fanfanshuo/install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/SKILL.md"
DEST_DIR="$HOME/.claude/skills/fanfanshuo"
DEST="$DEST_DIR/SKILL.md"

if [[ ! -f "$SRC" ]]; then
  echo "❌ 找不到源文件: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

if [[ -f "$DEST" ]]; then
  if cmp -s "$SRC" "$DEST"; then
    echo "✅ 已是最新版本: $DEST"
    exit 0
  fi
  BACKUP="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  cp "$DEST" "$BACKUP"
  echo "📦 已备份旧版本: $BACKUP"
fi

cp "$SRC" "$DEST"
echo "✅ 已安装到: $DEST"
echo "💡 任何项目里启动 Claude Code 后输入 /fanfanshuo 即可调用"
