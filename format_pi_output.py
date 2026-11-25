#!/usr/bin/env python3
"""Print pi's `--mode json` event stream in a human readable form.

Usage:
    pi --mode json "some prompt" | python3 format_pi_output.py

Reads one JSON event per line from standard input and prints reasoning,
tool calls, tool results and answers as they arrive.
"""

import json
import sys


def print_block(title, content):
    content = (content or "").strip()
    if not content:
        return
    print("\n=== " + title + " ===", flush=True)
    print(content, flush=True)


def text_of(result):
    parts = []
    for part in (result or {}).get("content", []) or []:
        if isinstance(part, dict) and part.get("type") == "text":
            parts.append(part.get("text", ""))
    return "\n".join(parts)


def main():
    for line in sys.stdin:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        kind = event.get("type")

        if kind == "message_update":
            inner = event.get("assistantMessageEvent") or {}
            inner_kind = inner.get("type")

            if inner_kind == "thinking_end":
                print_block("reasoning", inner.get("content"))
            elif inner_kind == "toolcall_end":
                call = inner.get("toolCall") or {}
                arguments = json.dumps(call.get("arguments"), ensure_ascii=False, indent=2)
                print_block("tool call: " + str(call.get("name")), arguments)
            elif inner_kind == "text_end":
                print_block("answer", inner.get("content"))

        elif kind == "tool_execution_end":
            output = text_of(event.get("result"))
            if len(output) > 2000:
                output = output[:2000] + "\n... (truncated)"
            print_block("tool result: " + str(event.get("toolName")), output)


if __name__ == "__main__":
    main()
