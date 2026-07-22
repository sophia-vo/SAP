#!/usr/bin/env python3
"""Command-line interface for compiling SAP inventory input files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import CompileError, compile_inventory, write_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile CSV SAP inventory into Ansible YAML.")
    parser.add_argument("--servers", type=Path, default=Path("inputs/servers.csv"))
    parser.add_argument("--instances", type=Path, default=Path("inputs/instances.csv"))
    parser.add_argument("--defaults", type=Path, default=Path("config/defaults.json"))
    parser.add_argument("--credentials", type=Path, default=Path("config/credentials.json"))
    parser.add_argument("--overrides", type=Path, default=Path("inputs/overrides.json"))
    parser.add_argument("--output", type=Path, default=Path("generated/inventory.yml"))
    parser.add_argument(
        "--normalized-output",
        type=Path,
        default=Path("generated/normalized_inventory.json"),
    )
    args = parser.parse_args()
    try:
        inventory, normalized = compile_inventory(
            servers_path=args.servers,
            instances_path=args.instances,
            defaults_path=args.defaults,
            credentials_path=args.credentials,
            overrides_path=args.overrides,
        )
        write_inventory(
            inventory,
            normalized,
            inventory_path=args.output,
            normalized_path=args.normalized_output,
        )
    except CompileError as exc:
        print(f"Inventory compilation failed: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {args.output} for {len(normalized['servers'])} enabled server(s).")
    print(f"Wrote {args.normalized_output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
