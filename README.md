# Bulk SAP Validation

This repository runs the existing read-only SAP HANA and S/4HANA validation
checks across one server or thousands of servers.

The scalable workflow is:

1. Maintain server connection records in `inputs/servers.csv`.
2. Maintain SAP component/instance records in `inputs/instances.csv`.
3. Run `./sap_validate.py`.
4. The runner compiles `generated/inventory.yml`, executes Ansible in controlled
   batches, and writes one directory per server below a shared timestamp.

The validation task implementations under `tasks/` remain unchanged. The
inventory compiler generates their existing `hana_sid`, `app_sid`, `hana_db`,
and `nw_app` interfaces for compatibility.

See [usage_guide.md](usage_guide.md) for setup and operating instructions.
