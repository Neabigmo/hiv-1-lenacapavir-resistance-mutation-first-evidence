#!/usr/bin/env python3
"""日志 wrapper - 记录重要操作到审计系统"""
import json
import sys
from datetime import datetime
from pathlib import Path

def log_event(event_type: str, message: str, metadata: dict = None):
    """记录事件到 events.jsonl"""
    log_file = Path("logs/commands/events.jsonl")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "message": message,
        "agent": "claude"
    }
    if metadata:
        entry["metadata"] = metadata

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def log_decision(title: str, reason: str, impact: str):
    """记录决策到 DECISIONS.md"""
    log_file = Path("logs/decisions/DECISIONS.md")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n### {title}\n- **决策**: {title}\n- **原因**: {reason}\n- **影响**: {impact}\n"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: log_wrapper.py <event|decision> <args...>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "event":
        log_event(sys.argv[2], sys.argv[3])
    elif cmd == "decision":
        log_decision(sys.argv[2], sys.argv[3], sys.argv[4])
