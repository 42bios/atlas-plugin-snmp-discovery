# Atlas SNMP Discovery plugin

Independent, read-only inventory connector for Atlas. Equipment, interfaces, link speeds, VLAN facts and observed network neighbors.

## Status

Initial extracted package, version 1.0.0. This repository is public and can be downloaded anonymously through Atlas’s repository installer. The collector implementation already exists in Atlas. Repository installation is separate from migrating an existing bundled connector; do not create a duplicate scheduled collector for the same system.

## Install

1. Open **Sources & settings → Add-ins → Add GitHub repository** in Atlas.
2. Enter `https://github.com/42bios/atlas-plugin-snmp-discovery`; optionally pin a release tag or commit.
3. Review the downloaded files and commit. Confirm trust with the exact repository name.
4. Add a connector instance, configure it, then select **Import now**.
5. After checking imported inventory, choose an import schedule if desired.

## Configuration

Set **Discovery targets** to explicit IPv4 addresses or CIDR networks, separated by spaces or commas, up to 1024 addresses. Choose SNMP 2c or 3 and enter the matching community or credential JSON privately. Physical patch-panel paths require manual documentation when not discoverable. SNMP command-line tools must be present on the Atlas host.

Credentials: **SNMP community or SNMPv3 credential JSON**. Credentials belong in Atlas's private credential field, never in this repository, issues or screenshots.

## Runtime and limits

Atlas add-in manifest schema 1, connector API 1, Python runtime. Atlas provides per-instance configuration paths and scoped snapshot credentials. This documents inventory; it does not monitor availability or modify the upstream system. Existing manual overrides are retained by stable connector-local IDs.

Repository code runs with Atlas application permissions. Checksums verify the downloaded files, not the author's trustworthiness. Install only code you have reviewed and trust.

## Development

Run `python -m unittest discover -s tests` before publishing. After modifying declared package files, run `python tools/update_manifest.py` and bump `version` in `atlas-addin.json`. Commit all checksum changes together. CI checks file integrity, Python syntax and collector fixtures without contacting a live system.
