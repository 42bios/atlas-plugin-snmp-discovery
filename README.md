# Atlas SNMP Discovery plugin

Independent, read-only inventory connector for Atlas. Equipment, interfaces, link speeds, VLAN facts and observed network neighbors.

## Status

Repository connector for the Atlas isolated-worker runtime. The package is installed independently from the main application; configuration and import are separate steps. The README shown in Marketplace belongs to the catalog-pinned commit, so older package versions keep their original documentation.

## Install

1. Open **Marketplace**, search for this connector and open its repository README.
2. Choose **Download & review**. Atlas resolves the catalog's pinned commit and verifies the declared package files before installation.
3. Review the package and its access requirements, type `42bios/atlas-plugin-snmp-discovery` to confirm trust, then install it.
4. Choose **Configure connector**. An existing system opens for editing; multiple systems produce a chooser. Create a new instance only for a different upstream system.
5. Start with **Manual imports**, enter the controller URL / discovery targets and private credential, then save.
6. Open **Sources & settings → Connected systems** and select **Test & import**. Review the imported objects before enabling a schedule.

For a private or unlisted connector, use **Sources & settings → Developer tools → Add GitHub repository**. Installing a package does not authenticate to an upstream service or start an import. Each configured system has its own stable source ID and credential. Updates retain those IDs and credentials; do not create a second collector for the same system.


## Configuration

Set **Discovery targets** to explicit IPv4 addresses or CIDR networks, separated by spaces or commas, up to 1024 addresses. Choose SNMP 2c or 3 and enter the matching community or credential JSON privately. Physical patch-panel paths require manual documentation when not discoverable. SNMP command-line tools must be present on the Atlas host.

Credentials: **SNMP community or SNMPv3 credential JSON**. Credentials belong in Atlas's private credential field, never in this repository, issues or screenshots.

## Runtime and limits

Atlas add-in manifest schema 1, connector API 1, Python runtime. Atlas provides per-instance configuration paths and scoped snapshot credentials. This documents inventory; it does not monitor availability or modify the upstream system. Existing manual overrides are retained by stable connector-local IDs.

Atlas executes each import in a separate worker container. It receives this instance’s configuration and credential and a source-scoped import token. The worker has outbound network access, but no Atlas database, other instances’ credentials or Docker socket mount. Use reviewed code and read-only upstream credentials. File checksums identify the downloaded content; they do not certify its author.

## Development

Run `python -m unittest discover -s tests` before publishing. After modifying declared package files, run `python tools/update_manifest.py` and bump `version` in `atlas-addin.json`. Commit all checksum changes together. CI checks file integrity, Python syntax and collector fixtures without contacting a live system.

## Compatibility regression checks

Run `python3 -m unittest discover -s tests` before release. Fixtures cover upstream variations, unavailable queries and data minimization; they are not proof of a successful connection to every upstream release. The Kubernetes and Proxmox adapters remain fixture-validated until tested against a real installation.

### Discovery gaps and LLDP identities

A run with zero responding devices or missing required interface tables fails and preserves the previous snapshot. Unsupported MIB objects are different from tables that return no entries. Empty tables do not prove the absence of neighbors.

LLDP local identifiers are matched to unique interface identities/descriptions. An explicit `Slot: S Port: P` description can match an interface named `S/P`, as verified on the tested UniFi switches. The local LLDP number is never assumed to be ifIndex. Ambiguous or unmatched observations remain in `discovery.unmatchedNeighbors`; no physical cables or patch-panel paths are inferred. Saturated 32-bit speed values remain unknown unless a valid high-speed value is available.

## Validation and upgrade notes

Real SNMP observations have been imported into Atlas. This release retains the existing collector implementation; package tests cover discovery and parsing. Credentials and explicit target ranges are required, and LLDP observations do not prove passive patch paths.

This documentation release changes setup instructions and runtime descriptions. Collector behavior is unchanged. Review Marketplace updates explicitly; applying an update does not require re-entering saved credentials. Keep credentials out of repositories, issues and screenshots.

## License

Copyright © 2026 42bios. Licensed under **GPL-3.0-only**. See [LICENSE.txt](LICENSE.txt). This applies to this connector’s code and documentation; upstream products and trademarks retain their own rights.
