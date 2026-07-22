#!/usr/bin/env python3
"""Backward-compatible entry point for the renamed bulk SAP runner."""

from sap_validate import main


if __name__ == "__main__":
    raise SystemExit(main())
