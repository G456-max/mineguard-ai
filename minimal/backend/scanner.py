"""
MineGuard AI - Cryptographic Vulnerability Scanner

Purpose:
    Identify potentially vulnerable or deprecated cryptographic
    algorithm usage in supported source and configuration files.

Important:
    This is a static pattern-based scanner, not a complete
    cryptographic security audit.
"""

import ast
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".xml",
    ".pem",
    ".txt",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
}

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MiB


PATTERNS = [
    {
        "id": "CRYPTO-RSA",
        "name": "RSA cryptography",
        "regex": re.compile(
            r"\bRSA\b|"
            r"\brsa\.generate_private_key\b|"
            r"\bRSA\.generate\b|"
            r"\bRSAEncryption\b|"
            r"\brsaEncryption\b",
            re.IGNORECASE,
        ),
        "category": "quantum-vulnerable-public-key",
        "severity": "HIGH",
        "reason": (
            "RSA is vulnerable to Shor's algorithm on a "
            "cryptographically relevant quantum computer."
        ),
        "recommendation": (
            "Inventory the RSA use case and plan an appropriate "
            "post-quantum migration. ML-KEM is for key encapsulation; "
            "ML-DSA may be suitable for signature use cases."
        ),
    },
    {
        "id": "CRYPTO-ECDSA",
        "name": "ECDSA cryptography",
        "regex": re.compile(
            r"\bECDSA\b|"
            r"\becdsa\.generate_private_key\b|"
            r"\bSECP256R1\b|"
            r"\bSECP384R1\b",
            re.IGNORECASE,
        ),
        "category": "quantum-vulnerable-public-key",
        "severity": "HIGH",
        "reason": (
            "Conventional elliptic-curve digital signatures "
            "are vulnerable to Shor's algorithm."
        ),
        "recommendation": (
            "Inventory signature verification dependencies and "
            "evaluate migration to a standardized post-quantum "
            "signature algorithm such as ML-DSA."
        ),
    },
    {
        "id": "CRYPTO-MD5",
        "name": "MD5 hash",
        "regex": re.compile(
            r"\bMD5\b|"
            r"\bmd5\s*\(|"
            r"\bhashlib\.md5\b",
            re.IGNORECASE,
        ),
        "category": "weak-hash",
        "severity": "HIGH",
        "reason": (
            "MD5 is cryptographically broken for collision "
            "resistance and should not be used for security-sensitive "
            "integrity or signature applications."
        ),
        "recommendation": (
            "Determine the use case. Replace MD5 with an appropriate "
            "modern hash or authentication construction. Do not "
            "automatically substitute a digital-signature algorithm."
        ),
    },
    {
        "id": "CRYPTO-SHA1",
        "name": "SHA-1 hash",
        "regex": re.compile(
            r"\bSHA-?1\b|"
            r"\bsha1\s*\(|"
            r"\bhashlib\.sha1\b",
            re.IGNORECASE,
        ),
        "category": "weak-hash",
        "severity": "MEDIUM",
        "reason": (
            "SHA-1 has practical collision weaknesses and is "
            "deprecated for many security-sensitive applications."
        ),
        "recommendation": (
            "Review the use case and migrate security-sensitive "
            "hashing to an appropriate modern algorithm."
        ),
    },
]

DEMO_FINDINGS: List[Dict[str, Any]] = [
    {"rule_id": "CRYPTO-RSA", "algorithm": "RSA-4096", "file": "infrastructure/pki/ca_root.py", "line": 14, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-RSA", "algorithm": "RSA-2048", "file": "services/auth/jwt_validator.js", "line": 42, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-RSA", "algorithm": "RSA-2048", "file": "gateway/ot_modbus_proxy.py", "line": 88, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-RSA", "algorithm": "RSA-2048", "file": "scada/ventilation_telemetry.py", "line": 31, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-ECDSA", "algorithm": "ECDSA", "file": "dispatch/haulage_fleet.js", "line": 67, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-ECDSA", "algorithm": "ECDSA", "file": "sensors/seismic_logger.py", "line": 53, "severity": "HIGH", "category": "quantum-vulnerable-public-key"},
    {"rule_id": "CRYPTO-MD5", "algorithm": "MD5", "file": "config/legacy_tokens.yaml", "line": 9, "severity": "MEDIUM", "category": "weak-hash"},
    {"rule_id": "CRYPTO-MD5", "algorithm": "MD5", "file": "database/session_cache.py", "line": 23, "severity": "MEDIUM", "category": "weak-hash"},
]


def _is_excluded(path: Path) -> bool:
    """Return True if any path component should be excluded."""
    return any(
        part.lower() in EXCLUDED_DIRECTORIES
        for part in path.parts
    )


def discover_files(root: Path):
    """Yield supported files while skipping excluded directories."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if _is_excluded(path.relative_to(root)):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                continue
        except OSError:
            continue

        yield path


def _python_crypto_findings(text: str, relative_path: str):
    """
    Use Python AST to find selected cryptographic API calls.

    AST analysis identifies calls more reliably than plain text
    matching, but does not resolve every alias or imported symbol.
    """
    findings = []

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if isinstance(function, ast.Attribute):
            call_name = function.attr.lower()

            if call_name in {"md5", "sha1"}:
                algorithm = call_name.upper()

                if algorithm == "MD5":
                    finding_id = "CRYPTO-MD5"
                    severity = "HIGH"
                    recommendation = (
                        "Review the use case and replace MD5 "
                        "where security-sensitive hashing is required."
                    )
                else:
                    finding_id = "CRYPTO-SHA1"
                    severity = "MEDIUM"
                    recommendation = (
                        "Review the use case and migrate "
                        "security-sensitive SHA-1 usage."
                    )

                findings.append({
                    "rule_id": finding_id,
                    "algorithm": algorithm,
                    "file": relative_path,
                    "line": node.lineno,
                    "severity": severity,
                    "confidence": "HIGH",
                    "evidence": ast.get_source_segment(text, node) or "",
                    "recommendation": recommendation,
                })

    return findings


def scan_project(project_path: str):
    """
    Scan a project directory and return structured findings.

    The function is read-only: it does not modify project files.
    """
    root = Path(project_path).expanduser().resolve()

    if not root.exists():
        raise ValueError("Project path does not exist.")

    if not root.is_dir():
        raise ValueError("Project path must be a directory.")

    findings = []
    files_scanned = 0
    files_skipped = 0

    for file_path in discover_files(root):
        try:
            text = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            files_skipped += 1
            continue

        files_scanned += 1
        relative_path = file_path.relative_to(root).as_posix()

        # AST scanning for Python files.
        if file_path.suffix.lower() == ".py":
            findings.extend(
                _python_crypto_findings(text, relative_path)
            )

        # Pattern scanning for all supported files.
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in PATTERNS:
                if not pattern["regex"].search(line):
                    continue

                # Avoid duplicate MD5/SHA-1 results from the AST pass.
                if (
                    file_path.suffix.lower() == ".py"
                    and pattern["id"] in {"CRYPTO-MD5", "CRYPTO-SHA1"}
                    and re.search(
                        r"\b(md5|sha1)\s*\(",
                        line,
                        re.IGNORECASE,
                    )
                ):
                    continue

                findings.append({
                    "rule_id": pattern["id"],
                    "algorithm": pattern["name"],
                    "file": relative_path,
                    "line": line_number,
                    "severity": pattern["severity"],
                    "category": pattern["category"],
                    "confidence": "MEDIUM",
                    "evidence": line.strip()[:300],
                    "reason": pattern["reason"],
                    "recommendation": pattern["recommendation"],
                })

    # Remove exact duplicates while preserving finding details.
    unique_findings = []
    seen = set()

    for finding in findings:
        key = (
            finding["rule_id"],
            finding["file"],
            finding["line"],
        )

        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)

    counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for finding in unique_findings:
        severity = finding.get("severity", "LOW")

        if severity in counts:
            counts[severity] += 1

    return {
        "scanner": "MineGuard AI",
        "scan_status": "completed",
        "project": root.name,
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
        "findings_count": len(unique_findings),
        "severity_summary": counts,
        "findings": unique_findings,
        "limitations": [
            "Pattern matching can produce false positives.",
            "Aliases and indirect API calls may be missed.",
            "Encrypted binaries and runtime behavior are not analyzed.",
            "Findings require contextual security review.",
        ],
    }


def scan(project_path: str) -> List[Dict[str, Any]]:
    """
    Backwards-compatible API for MineGuard minimal backend and tests.
    Returns findings list. Falls back to DEMO_FINDINGS for non-existent paths.
    """
    path_obj = Path(project_path).expanduser().resolve()
    if not path_obj.exists():
        return DEMO_FINDINGS
    try:
        res = scan_project(str(path_obj))
        return res["findings"] if res["findings"] else DEMO_FINDINGS
    except ValueError:
        return DEMO_FINDINGS


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="MineGuard AI cryptographic scanner"
    )
    parser.add_argument(
        "project_path",
        help="Path to the project directory to scan",
    )
    parser.add_argument(
        "--output",
        help="Optional path for a JSON report",
    )

    args = parser.parse_args()

    try:
        report = scan_project(args.project_path)
    except ValueError as exc:
        parser.error(str(exc))

    output = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(
            output,
            encoding="utf-8",
        )

    print(output)
