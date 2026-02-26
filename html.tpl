<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Trivy Vulnerability Report</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #1a237e; border-bottom: 3px solid #1a237e; padding-bottom: 10px; }
        h2 { color: #283593; margin-top: 30px; }
        .summary { background: #fff; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .summary-grid { display: flex; gap: 15px; flex-wrap: wrap; }
        .summary-card { flex: 1; min-width: 120px; padding: 15px; border-radius: 8px; text-align: center; color: #fff; }
        .summary-card .count { font-size: 2em; font-weight: bold; }
        .summary-card .label { font-size: 0.9em; margin-top: 5px; }
        .critical { background: #7b1fa2; }
        .high { background: #c62828; }
        .medium { background: #ef6c00; }
        .low { background: #2e7d32; }
        .unknown { background: #616161; }
        .clean { background: #2e7d32; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background: #1a237e; color: #fff; padding: 12px 15px; text-align: left; font-size: 0.9em; }
        td { padding: 10px 15px; border-bottom: 1px solid #e0e0e0; font-size: 0.85em; }
        tr:hover { background: #f5f5f5; }
        .severity-badge { padding: 3px 10px; border-radius: 12px; color: #fff; font-size: 0.8em; font-weight: bold; display: inline-block; }
        .severity-CRITICAL { background: #7b1fa2; }
        .severity-HIGH { background: #c62828; }
        .severity-MEDIUM { background: #ef6c00; }
        .severity-LOW { background: #2e7d32; }
        .severity-UNKNOWN { background: #616161; }
        .meta { color: #757575; font-size: 0.85em; margin: 10px 0; }
        .no-vulns { background: #e8f5e9; color: #2e7d32; padding: 20px; border-radius: 8px; text-align: center; font-size: 1.2em; font-weight: bold; margin: 20px 0; }
        a { color: #1565c0; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .footer { text-align: center; color: #9e9e9e; margin-top: 40px; padding: 20px; font-size: 0.85em; }
    </style>
</head>
<body>
<div class="container">
    <h1>Trivy Security Scan Report</h1>
    <div class="meta">
        <p><strong>Scan Date:</strong> {{ now }}</p>
        <p><strong>Scanner:</strong> Trivy v0.69.1</p>
    </div>
{{- range . }}
    <h2>Target: {{ escapeXML .Target }}{{ if .Type }} ({{ .Type }}){{ end }}</h2>
  {{- if (eq (len .Vulnerabilities) 0) }}
    <div class="no-vuln">No vulnerabilities found</div>
  {{- else }}
    <div class="summary">
        <h3>Vulnerability Summary</h3>
        <div class="summary-grid">
        {{- $critical := 0 }}{{ $high := 0 }}{{ $medium := 0 }}{{ $low := 0 }}{{ $unknown := 0 }}
        {{- range .Vulnerabilities }}
            {{- if eq .Severity "CRITICAL" }}{{ $critical = add $critical 1 }}
            {{- else if eq .Severity "HIGH" }}{{ $high = add $high 1 }}
            {{- else if eq .Severity "MEDIUM" }}{{ $medium = add $medium 1 }}
            {{- else if eq .Severity "LOW" }}{{ $low = add $low 1 }}
            {{- else }}{{ $unknown = add $unknown 1 }}{{ end }}
        {{- end }}
            <div class="summary-card critical"><div class="count">{{ $critical }}</div><div class="label">CRITICAL</div></div>
            <div class="summary-card high"><div class="count">{{ $high }}</div><div class="label">HIGH</div></div>
            <div class="summary-card medium"><div class="count">{{ $medium }}</div><div class="label">MEDIUM</div></div>
            <div class="summary-card low"><div class="count">{{ $low }}</div><div class="label">LOW</div></div>
            <div class="summary-card unknown"><div class="count">{{ $unknown }}</div><div class="label">UNKNOWN</div></div>
        </div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Library</th>
                <th>Vulnerability</th>
                <th>Severity</th>
                <th>Installed</th>
                <th>Fixed Version</th>
                <th>Title</th>
            </tr>
        </thead>
        <tbody>
        {{- range .Vulnerabilities }}
            <tr>
                <td>{{ escapeXML .PkgName }}</td>
                <td><a href="{{ escapeXML .PrimaryURL }}" target="_blank">{{ escapeXML .VulnerabilityID }}</a></td>
                <td><span class="severity-badge severity-{{ escapeXML .Severity }}">{{ escapeXML .Severity }}</span></td>
                <td>{{ escapeXML .InstalledVersion }}</td>
                <td>{{ escapeXML .FixedVersion }}</td>
                <td>{{ escapeXML .Title }}</td>
            </tr>
        {{- end }}
        </tbody>
    </table>
  {{- end }}

  {{- if (eq (len .Misconfigurations) 0) }}
  {{- else }}
    <h3>Misconfigurations</h3>
    <table>
        <thead>
            <tr>
                <th>Type</th>
                <th>ID</th>
                <th>Severity</th>
                <th>Title</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody>
        {{- range .Misconfigurations }}
            <tr>
                <td>{{ escapeXML .Type }}</td>
                <td>{{ escapeXML .ID }}</td>
                <td><span class="severity-badge severity-{{ escapeXML .Severity }}">{{ escapeXML .Severity }}</span></td>
                <td>{{ escapeXML .Title }}</td>
                <td>{{ escapeXML .Message }}</td>
            </tr>
        {{- end }}
        </tbody>
    </table>
  {{- end }}

  {{- if (eq (len .Secrets) 0) }}
  {{- else }}
    <h3>Secrets</h3>
    <table>
        <thead>
            <tr><th>Category</th><th>Severity</th><th>Title</th><th>Match</th></tr>
        </thead>
        <tbody>
        {{- range .Secrets }}
            <tr>
                <td>{{ escapeXML .Category }}</td>
                <td><span class="severity-badge severity-{{ escapeXML .Severity }}">{{ escapeXML .Severity }}</span></td>
                <td>{{ escapeXML .Title }}</td>
                <td>{{ escapeXML .Match }}</td>
            </tr>
        {{- end }}
        </tbody>
    </table>
  {{- end }}
{{- end }}

{{- $totalVulns := 0 }}
{{- range . }}{{ $totalVulns = add $totalVulns (len .Vulnerabilities) }}{{ end }}
{{- if eq $totalVulns 0 }}
    <div class="no-vulns">All Clear — No Vulnerabilities Detected</div>
{{- end }}

    <div class="footer">
        <p>Generated by Trivy v0.69.1 | Restful Booker API Security Report</p>
    </div>
</div>
</body>
</html>
