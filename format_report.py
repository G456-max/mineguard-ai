"""
format_report.py
Generates a clean visual HTML report for the cryptographic scan output
and launches it alongside the JSON report.
"""

import json
from pathlib import Path

json_path = Path(r"C:\Users\gudae mahalakshmi\OneDrive\Documents\Desktop\MineGuard_Scan_Report.json")
html_path = Path(r"C:\Users\gudae mahalakshmi\OneDrive\Documents\Desktop\MineGuard_Scan_Report.html")

data = json.load(open(json_path, "r", encoding="utf-8"))

findings_html = []
for f in data.get("findings", [])[:150]:
    sev = f.get("severity", "LOW")
    sev_color = "#ef4444" if sev == "HIGH" else ("#f59e0b" if sev == "MEDIUM" else "#10b981")
    cat = f.get("category", "")
    rule = f.get("rule_id", "")
    algo = f.get("algorithm", "")
    file_loc = f"{f.get('file')}:{f.get('line')}"
    evid = f.get("evidence", "").replace("<", "&lt;").replace(">", "&gt;")
    rec = f.get("recommendation", "")

    row = f"""
    <tr>
      <td><span style="background:{sev_color}22;color:{sev_color};padding:4px 8px;border-radius:4px;font-weight:700;">{sev}</span></td>
      <td><b>{rule}</b><br/><span style="color:#9ca3af;font-size:0.8rem;">{algo}</span></td>
      <td><code style="color:#38bdf8;">{file_loc}</code></td>
      <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"><code>{evid}</code></td>
      <td style="font-size:0.85rem;color:#d1d5db;">{rec}</td>
    </tr>
    """
    findings_html.append(row)

rows_str = "\n".join(findings_html)
high_count = data.get("severity_summary", {}).get("HIGH", 0)
med_count = data.get("severity_summary", {}).get("MEDIUM", 0)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MineGuard AI — Cryptographic Audit Report</title>
  <style>
    body {{ background: #0b0f19; color: #f9fafb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 30px; margin: 0; }}
    .header {{ margin-bottom: 24px; border-bottom: 1px solid #1f2937; padding-bottom: 20px; }}
    h1 {{ color: #f59e0b; margin: 0 0 8px 0; font-size: 2rem; }}
    .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
    .card {{ background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 18px; }}
    .card h3 {{ margin: 0 0 6px 0; font-size: 0.85rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }}
    .card .val {{ font-size: 1.8rem; font-weight: 800; color: #fff; }}
    table {{ width: 100%; border-collapse: collapse; background: #111827; border-radius: 8px; overflow: hidden; }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid #1f2937; font-size: 0.9rem; }}
    th {{ background: #1e293b; color: #9ca3af; font-size: 0.8rem; text-transform: uppercase; }}
    tr:hover {{ background: #1e293b; }}
    code {{ background: #030712; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.85rem; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>🛡️ MineGuard AI — Cryptographic Audit Report</h1>
    <div style="color:#9ca3af;">Scanned Project Target: <b>{data.get('project')}</b> | Status: <b style="color:#10b981;">{data.get('scan_status').upper()}</b></div>
  </div>
  <div class="stats">
    <div class="card"><h3>Files Scanned</h3><div class="val">{data.get('files_scanned')}</div></div>
    <div class="card"><h3>Total Unique Findings</h3><div class="val">{data.get('findings_count')}</div></div>
    <div class="card"><h3>High Severity (Shor Breakable)</h3><div class="val" style="color:#ef4444;">{high_count}</div></div>
    <div class="card"><h3>Medium Severity (Weak Hash)</h3><div class="val" style="color:#f59e0b;">{med_count}</div></div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Severity</th>
        <th>Rule / Algorithm</th>
        <th>File Location</th>
        <th>Detected Evidence</th>
        <th>PQC Recommendation</th>
      </tr>
    </thead>
    <tbody>
      {rows_str}
    </tbody>
  </table>
  <div style="margin-top:20px;color:#9ca3af;font-size:0.85rem;">
    Showing top 150 cryptographic findings. Full raw findings available in <b>MineGuard_Scan_Report.json</b>.
  </div>
</body>
</html>
"""

html_path.write_text(html, encoding="utf-8")
print(f"Generated visual report at: {html_path}")
