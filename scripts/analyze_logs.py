#!/usr/bin/env python3
"""Print the five client IPs with the most HTTP 5xx responses."""

import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/analyze_logs.py <nginx-access-log>")
        return 1

    log_path = Path(sys.argv[1])
    if not log_path.is_file():
        print(f"Error: log file not found: {log_path}")
        return 1

    counts = Counter()
    try:
        with log_path.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                fields = line.split()
                if len(fields) < 9:
                    continue
                ip, status_text = fields[0], fields[8]
                if status_text.isdigit() and 500 <= int(status_text) <= 599:
                    counts[ip] += 1
    except OSError as exc:
        print(f"Error reading {log_path}: {exc}")
        return 1

    print("Top 5 client IPs with HTTP 5xx errors:")
    for ip, count in counts.most_common(5):
        print(f"{ip}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
