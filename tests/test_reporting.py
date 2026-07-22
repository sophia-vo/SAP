from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runner.reporting import aggregate_run


class ReportingTests(unittest.TestCase):
    def test_aggregates_completed_and_missing_servers(self):
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp)
            completed = run_dir / "server-01"
            completed.mkdir()
            (completed / "results.json").write_text(
                json.dumps(
                    [
                        {"check": "Login", "status": "PASS", "details": "ok"},
                        {"check": "Disk", "status": "WARN", "details": "high"},
                    ]
                )
            )
            (run_dir / "_controller.log").write_text(
                "server-01 : ok=10 changed=0 unreachable=0 failed=0 skipped=1 rescued=0 ignored=0\n"
                "server-02 : ok=0 changed=0 unreachable=1 failed=0 skipped=0 rescued=0 ignored=0\n"
            )
            normalized = {
                "servers": {
                    "server-01": {"address": "10.0.0.1", "components": ["hana"]},
                    "server-02": {"address": "10.0.0.2", "components": ["abap"]},
                }
            }
            summary = aggregate_run(
                run_dir=run_dir,
                normalized=normalized,
                selected_hosts=["server-01", "server-02"],
                ansible_return_code=4,
                command="ansible-playbook ...",
                run_timestamp="20260721_150000",
            )
            by_host = {row["server_id"]: row for row in summary["servers"]}
            self.assertEqual(by_host["server-01"]["overall_status"], "WARN")
            self.assertEqual(by_host["server-02"]["overall_status"], "UNREACHABLE")
            self.assertTrue((run_dir / "_summary.csv").exists())
            self.assertTrue((run_dir / "server-02" / "status.json").exists())


if __name__ == "__main__":
    unittest.main()
