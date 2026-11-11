"""Look up weapon records and follow their references."""
import argparse
from collections import deque
import json
from pathlib import Path
import re


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("get", "flat", "search", "chain"))
    parser.add_argument("term")
    parser.add_argument("--values", action="store_true")
    parser.add_argument("--type", default="")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.depth < 0 or args.limit < 1:
        parser.error("depth must be nonnegative and limit positive")
    path = Path(__file__).resolve().parents[1] / "data" / "weapons.jsonl"
    with path.open(encoding="utf-8") as stream:
        records = {record["name"]: record for record in map(json.loads, stream)}
    if args.command == "get":
        result = records[args.term]
    elif args.command == "flat":
        owner, _, field = args.term.rpartition(".")
        result = records[owner]["fields"][field]
    elif args.command == "search":
        pattern = re.compile(args.term, re.IGNORECASE)
        hits = [r for r in records.values() if (not args.type or args.type.lower() in r["type"].lower())
                and pattern.search(json.dumps(r) if args.values else r["name"])]
        result = {"matches": [{"name": r["name"], "type": r["type"]} for r in hits[:args.limit]], "total": len(hits)}
    else:
        queue = deque([(args.term, 0)])
        seen = set()
        found = []
        while queue and len(found) < args.limit:
            name, depth = queue.popleft()
            if name in seen:
                continue
            seen.add(name)
            record = records[name]
            found.append(record)
            if depth < args.depth:
                queue.extend((ref, depth + 1) for ref in strings(record["fields"]) if ref in records and ref not in seen)
        result = {"records": found, "truncated": any(name not in seen for name, depth in queue)}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
