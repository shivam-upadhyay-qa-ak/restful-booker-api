from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, TableColumnProperties, TableCellProperties, ParagraphProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P
from datetime import datetime


def create_style(doc, name, bold=False, bg_color=None, font_size="10pt", color=None, align=None):
    style = Style(name=name, family="table-cell")
    tp = TextProperties()
    if bold:
        tp.setAttribute("fontweight", "bold")
    if font_size:
        tp.setAttribute("fontsize", font_size)
    if color:
        tp.setAttribute("color", color)
    style.addElement(tp)
    if bg_color:
        tcp = TableCellProperties(backgroundcolor=bg_color)
        style.addElement(tcp)
    if align:
        pp = ParagraphProperties(textalign=align)
        style.addElement(pp)
    doc.automaticstyles.addElement(style)
    return style


def add_row(table, values, style=None):
    row = TableRow()
    for val in values:
        cell = TableCell()
        if style:
            cell.setAttribute("stylename", style)
        cell.addElement(P(text=str(val)))
        row.addElement(cell)
    table.addElement(row)


def main():
    doc = OpenDocumentSpreadsheet()

    # Styles
    header_style = create_style(doc, "Header", bold=True, bg_color="#1a237e", color="#ffffff", font_size="10pt")
    title_style = create_style(doc, "Title", bold=True, font_size="14pt")
    high_style = create_style(doc, "High", bold=True, bg_color="#ffcdd2", color="#c62828")
    medium_style = create_style(doc, "Medium", bold=True, bg_color="#fff3e0", color="#ef6c00")
    low_style = create_style(doc, "Low", bold=True, bg_color="#e8f5e9", color="#2e7d32")
    clean_style = create_style(doc, "Clean", bold=True, bg_color="#e8f5e9", color="#2e7d32")
    normal_style = create_style(doc, "Normal", font_size="10pt")

    critical_style = create_style(doc, "Critical", bold=True, bg_color="#e1bee7", color="#7b1fa2")
    severity_styles = {"CRITICAL": critical_style, "HIGH": high_style, "MEDIUM": medium_style, "LOW": low_style, "SAFE": clean_style}

    # ==================== Sheet 1: Summary ====================
    summary = Table(name="Summary")

    add_row(summary, ["Security Assessment Report - Restful Booker API"], title_style)
    add_row(summary, [f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], normal_style)
    add_row(summary, [f"Target: https://restful-booker.herokuapp.com"], normal_style)
    add_row(summary, [""], normal_style)

    add_row(summary, ["Tool", "Type", "Findings", "Status"], header_style)
    add_row(summary, ["Shannon (AI Pentester)", "DAST (Autonomous AI)", "5 vulnerabilities (2 Critical, 1 High, 2 Medium)", "OPEN"], critical_style)
    add_row(summary, ["Trivy v0.69.1", "SCA (Dependencies)", "41 CVEs found → All Fixed", "RESOLVED"], clean_style)
    add_row(summary, ["Bandit v1.9.4", "SAST (Source Code)", "3 issues found → All Fixed", "RESOLVED"], clean_style)
    add_row(summary, ["Gitleaks", "Secret Scanner", "0 leaks in source code", "CLEAN"], clean_style)
    add_row(summary, ["Manual DAST", "Live API Testing", "7 vulnerabilities found", "OPEN"], high_style)

    add_row(summary, [""], normal_style)
    add_row(summary, ["Overall: 2 CRITICAL | 4 HIGH | 5 MEDIUM | 1 LOW | 1 SAFE"], title_style)

    doc.spreadsheet.addElement(summary)

    # ==================== Sheet 2: Trivy (41 CVEs) ====================
    trivy_sheet = Table(name="Trivy - Dependencies")

    add_row(trivy_sheet, ["Trivy Dependency Scan Results (Before Fix)"], title_style)
    add_row(trivy_sheet, ["Total: 41 vulnerabilities (HIGH: 13, MEDIUM: 25, LOW: 3, CRITICAL: 0)"], normal_style)
    add_row(trivy_sheet, [""], normal_style)

    add_row(trivy_sheet, ["Library", "CVE", "Severity", "Installed Version", "Fixed Version", "Title"], header_style)

    trivy_vulns = [
        ["Brotli", "CVE-2025-6176", "HIGH", "1.1.0", "1.2.0", "Python brotli decompression bomb DoS"],
        ["Flask-Cors", "CVE-2024-6221", "HIGH", "4.0.0", "4.0.2", "Access-Control bypass vulnerability"],
        ["Flask-Cors", "CVE-2024-1681", "MEDIUM", "4.0.0", "4.0.1", "Log injection vulnerability"],
        ["Flask-Cors", "CVE-2024-6839", "MEDIUM", "4.0.0", "6.0.0", "Improper regex path matching"],
        ["Flask-Cors", "CVE-2024-6844", "MEDIUM", "4.0.0", "6.0.0", "Incorrect CORS header handling"],
        ["Flask-Cors", "CVE-2024-6866", "MEDIUM", "4.0.0", "6.0.0", "CORS policy bypass"],
        ["Flask", "CVE-2026-27205", "LOW", "3.0.2", "3.1.3", "Information disclosure via session caching"],
        ["Jinja2", "CVE-2024-22195", "MEDIUM", "3.1.2", "3.1.3", "HTML attribute injection via xmlattr"],
        ["Jinja2", "CVE-2024-34064", "MEDIUM", "3.1.2", "3.1.4", "Non-attribute characters in keys"],
        ["Jinja2", "CVE-2024-56201", "MEDIUM", "3.1.2", "3.1.5", "Sandbox breakout via malicious filenames"],
        ["Jinja2", "CVE-2024-56326", "MEDIUM", "3.1.2", "3.1.5", "Sandbox breakout via format method"],
        ["Jinja2", "CVE-2025-27516", "MEDIUM", "3.1.2", "3.1.6", "Sandbox breakout via attr filter"],
        ["PyNaCl", "CVE-2025-69277", "MEDIUM", "1.5.0", "1.6.2", "Improper elliptic curve point validation"],
        ["Werkzeug", "CVE-2024-34069", "HIGH", "3.0.1", "3.0.3", "Remote code execution on dev machine"],
        ["Werkzeug", "CVE-2024-49766", "MEDIUM", "3.0.1", "3.0.6", "safe_join not safe on Windows"],
        ["Werkzeug", "CVE-2024-49767", "MEDIUM", "3.0.1", "3.0.6", "Resource exhaustion in form parsing"],
        ["Werkzeug", "CVE-2025-66221", "MEDIUM", "3.0.1", "3.1.4", "DoS via Windows device names"],
        ["Werkzeug", "CVE-2026-21860", "MEDIUM", "3.0.1", "3.1.5", "Windows device names with compound extensions"],
        ["Werkzeug", "CVE-2026-27199", "MEDIUM", "3.0.1", "3.1.6", "Windows special device names bypass"],
        ["certifi", "CVE-2024-39689", "LOW", "2023.11.17", "2024.7.4", "Remove GLOBALTRUST root certificates"],
        ["configobj", "CVE-2023-26112", "LOW", "5.0.8", "5.0.9", "Regular expression denial of service"],
        ["cryptography", "CVE-2023-50782", "HIGH", "41.0.7", "42.0.0", "RSA Bleichenbacher timing oracle attack"],
        ["cryptography", "CVE-2024-26130", "HIGH", "41.0.7", "42.0.4", "NULL pointer dereference"],
        ["cryptography", "CVE-2026-26007", "HIGH", "41.0.7", "46.0.5", "Subgroup attack on SECT curves"],
        ["cryptography", "CVE-2024-0727", "MEDIUM", "41.0.7", "42.0.2", "OpenSSL denial of service"],
        ["cryptography", "GHSA-h4gh-qq45-vh27", "MEDIUM", "41.0.7", "43.0.1", "Vulnerable OpenSSL in wheels"],
        ["idna", "CVE-2024-3651", "MEDIUM", "3.6", "3.7", "DoS via crafted inputs to idna.encode()"],
        ["locust", "CVE-2020-28364", "MEDIUM", "0.0.0", "1.3.2", "Stored Cross-site Scripting"],
        ["paramiko", "CVE-2023-48795", "MEDIUM", "2.12.0", "3.4.0", "SSH prefix truncation attack (Terrapin)"],
        ["pillow", "CVE-2024-28219", "HIGH", "10.2.0", "10.3.0", "Buffer overflow in _imagingcms.c"],
        ["requests", "CVE-2024-35195", "MEDIUM", "2.31.0", "2.32.0", "Cert verification ignored on same host"],
        ["requests", "CVE-2024-47081", "MEDIUM", "2.31.0", "2.32.4", ".netrc credentials leak via malicious URLs"],
        ["setuptools", "CVE-2024-6345", "HIGH", "68.1.2", "70.0.0", "RCE via package_index download functions"],
        ["setuptools", "CVE-2025-47273", "HIGH", "68.1.2", "78.1.1", "Path traversal in PackageIndex"],
        ["urllib3", "CVE-2025-66418", "HIGH", "2.0.7", "2.6.0", "Unbounded decompression chain"],
        ["urllib3", "CVE-2025-66471", "HIGH", "2.0.7", "2.6.0", "Compressed data handling issue"],
        ["urllib3", "CVE-2026-21441", "HIGH", "2.0.7", "2.6.3", "Decompression-bomb bypass on redirects"],
        ["urllib3", "CVE-2024-37891", "MEDIUM", "2.0.7", "2.2.2", "Proxy-auth header leak on redirects"],
        ["urllib3", "CVE-2025-50181", "MEDIUM", "2.0.7", "2.5.0", "Redirects not disabled when retries off"],
        ["wheel", "CVE-2026-24049", "HIGH", "0.42.0", "0.46.2", "Privilege escalation via malicious wheel"],
        ["zipp", "CVE-2024-5569", "MEDIUM", "1.0.0", "3.19.1", "DoS via crafted zip file"],
    ]

    for vuln in trivy_vulns:
        sev = vuln[2]
        style = severity_styles.get(sev, normal_style)
        add_row(trivy_sheet, vuln, style)

    add_row(trivy_sheet, [""], normal_style)
    add_row(trivy_sheet, ["STATUS: ALL 41 CVEs FIXED — Dependencies upgraded"], clean_style)

    doc.spreadsheet.addElement(trivy_sheet)

    # ==================== Sheet 3: Bandit (SAST) ====================
    bandit_sheet = Table(name="Bandit - SAST")

    add_row(bandit_sheet, ["Bandit SAST Scan Results"], title_style)
    add_row(bandit_sheet, [""], normal_style)

    add_row(bandit_sheet, ["File", "Line", "Issue ID", "Severity", "CWE", "Description"], header_style)
    add_row(bandit_sheet, ["api/create_booking.py", "8", "B113", "MEDIUM", "CWE-400", "requests.post() without timeout"], medium_style)
    add_row(bandit_sheet, ["api/get_all_bookings.py", "8", "B113", "MEDIUM", "CWE-400", "requests.get() without timeout"], medium_style)
    add_row(bandit_sheet, ["api/get_booking_by_id.py", "8", "B113", "MEDIUM", "CWE-400", "requests.get() without timeout"], medium_style)

    add_row(bandit_sheet, [""], normal_style)
    add_row(bandit_sheet, ["STATUS: ALL 3 ISSUES FIXED — timeout=30 added to all requests"], clean_style)

    doc.spreadsheet.addElement(bandit_sheet)

    # ==================== Sheet 4: Gitleaks ====================
    gitleaks_sheet = Table(name="Gitleaks - Secrets")

    add_row(gitleaks_sheet, ["Gitleaks Secret Scan Results"], title_style)
    add_row(gitleaks_sheet, [""], normal_style)

    add_row(gitleaks_sheet, ["Scope", "Leaks Found", "Status"], header_style)
    add_row(gitleaks_sheet, ["api/", "0", "CLEAN"], clean_style)
    add_row(gitleaks_sheet, ["config/", "0", "CLEAN"], clean_style)
    add_row(gitleaks_sheet, ["main.py", "0", "CLEAN"], clean_style)
    add_row(gitleaks_sheet, ["venv/ (third-party)", "12 false positives", "IGNORED — Library code"], normal_style)

    add_row(gitleaks_sheet, [""], normal_style)
    add_row(gitleaks_sheet, ["STATUS: NO SECRETS LEAKED IN SOURCE CODE"], clean_style)

    doc.spreadsheet.addElement(gitleaks_sheet)

    # ==================== Sheet 5: DAST (Live API) ====================
    dast_sheet = Table(name="DAST - Live API")

    add_row(dast_sheet, ["Manual DAST Scan Results — Live API Testing"], title_style)
    add_row(dast_sheet, ["Target: https://restful-booker.herokuapp.com"], normal_style)
    add_row(dast_sheet, [""], normal_style)

    add_row(dast_sheet, ["#", "Finding", "Severity", "API Endpoint", "Description", "Status"], header_style)

    dast_findings = [
        ["1", "Stored XSS", "HIGH", "POST /booking", "<script>alert(1)</script> accepted and stored without sanitization", "OPEN"],
        ["2", "No Authentication Required", "HIGH", "POST /booking", "Bookings created without any auth token/API key", "OPEN"],
        ["3", "IDOR", "HIGH", "GET /booking/{id}", "Any booking accessible by iterating IDs without authorization", "OPEN"],
        ["4", "Missing Security Headers", "MEDIUM", "All APIs", "Missing: X-Content-Type-Options, X-Frame-Options, HSTS, CSP, X-XSS-Protection", "OPEN"],
        ["5", "No Input Validation", "MEDIUM", "POST /booking", "SQL injection payloads accepted: ' OR 1=1 --", "OPEN"],
        ["6", "No Rate Limiting", "MEDIUM", "All APIs", "10+ rapid requests all return HTTP 200, no throttling", "OPEN"],
        ["7", "Server Technology Exposed", "LOW", "All APIs", "X-Powered-By: Express header reveals server framework", "OPEN"],
        ["8", "Path Traversal", "SAFE", "GET /booking/{id}", "/../../../etc/passwd returns 404 — properly handled", "SAFE"],
    ]

    for finding in dast_findings:
        sev = finding[2]
        style = severity_styles.get(sev, normal_style)
        add_row(dast_sheet, finding, style)

    add_row(dast_sheet, [""], normal_style)
    add_row(dast_sheet, ["STATUS: 7 OPEN VULNERABILITIES — Server-side fixes required"], high_style)

    doc.spreadsheet.addElement(dast_sheet)

    # ==================== Sheet 6: Shannon (AI Pentester) ====================
    shannon_sheet = Table(name="Shannon - AI Pentester")

    add_row(shannon_sheet, ["Shannon Autonomous AI Pentester — Security Assessment"], title_style)
    add_row(shannon_sheet, ["Assessment Date: 2026-02-20"], normal_style)
    add_row(shannon_sheet, ["Assessment Type: Autonomous AI Penetration Testing"], normal_style)
    add_row(shannon_sheet, ["Target: https://restful-booker.herokuapp.com"], normal_style)
    add_row(shannon_sheet, ["Tool: Shannon (https://github.com/KeygraphHQ/shannon)"], normal_style)
    add_row(shannon_sheet, [""], normal_style)

    # Shannon Summary
    add_row(shannon_sheet, ["VULNERABILITY SUMMARY"], title_style)
    add_row(shannon_sheet, ["Metric", "Value"], header_style)
    add_row(shannon_sheet, ["Total Vulnerabilities", "5"], normal_style)
    add_row(shannon_sheet, ["Critical Issues", "2"], critical_style)
    add_row(shannon_sheet, ["High Severity Issues", "1"], high_style)
    add_row(shannon_sheet, ["Medium Severity Issues", "2"], medium_style)
    add_row(shannon_sheet, ["Status", "VULNERABLE - ACTION REQUIRED"], critical_style)
    add_row(shannon_sheet, [""], normal_style)

    # Shannon Detailed Findings
    add_row(shannon_sheet, ["DETAILED VULNERABILITY FINDINGS"], title_style)
    add_row(shannon_sheet, ["#", "Vulnerability", "Severity", "Status", "CWE", "CVSS Score", "Verified", "Remarks"], header_style)

    shannon_findings = [
        ["1", "SQL Injection - checkin/checkout Parameters", "CRITICAL", "CONFIRMED VULNERABLE", "CWE-89", "9.8", "YES", "Payload: ' OR '1'='1 returns manipulated data"],
        ["2", "Stored XSS - firstname, lastname, additionalneeds", "HIGH", "CONFIRMED VULNERABLE", "CWE-79", "6.1", "YES", "Payloads stored verbatim in database"],
        ["3", "Weak Input Validation", "MEDIUM", "CONFIRMED VULNERABLE", "CWE-20", "5.3", "YES", "Accepts negative prices, invalid dates, long strings"],
        ["4", "Information Disclosure", "MEDIUM", "CONFIRMED VULNERABLE", "CWE-200", "5.3", "YES", "Guest info, prices exposed to all authenticated users"],
        ["5", "Horizontal Privilege Escalation (IDOR)", "CRITICAL", "NOT VULNERABLE", "CWE-639", "7.5", "NO", "Authorization checks appear to be working correctly"],
    ]

    for finding in shannon_findings:
        sev = finding[2]
        style = severity_styles.get(sev, normal_style)
        add_row(shannon_sheet, finding, style)

    add_row(shannon_sheet, [""], normal_style)

    # Shannon Test Results
    add_row(shannon_sheet, ["MANUAL VERIFICATION TEST RESULTS"], title_style)
    add_row(shannon_sheet, ["Test Name", "Tool Used", "Payload/Method", "Expected Result", "Actual Result", "Vulnerable?", "Evidence", "Recommendation"], header_style)

    shannon_tests = [
        ["SQL Injection - OR True", "curl/Python", "?checkin=' OR '1'='1", "Empty or normal results", "Returns manipulated booking data", "YES", "HTTP 200, data count differs from baseline", "Use parameterized queries immediately"],
        ["SQL Injection - AND True/False", "curl/Python", "?checkin=' AND '1'='1 vs ' AND '1'='2", "Same results", "Different results - boolean-based injection works", "YES", "Boolean-based SQLi confirmed", "Implement input validation and parameterized queries"],
        ["Stored XSS - Script Tag", "Postman/Python", 'firstname: "<script>alert(XSS)</script>"', "Payload sanitized", "Payload stored verbatim in database", "YES", "Payload retrieved as-is from GET /booking/:id", "Implement input sanitization and output encoding"],
        ["Weak Input Validation - Negative Price", "Postman", "totalprice: -999", "Request rejected with 400/422", "HTTP 200 - booking created with negative price", "YES", "Negative price accepted in POST request", "Add server-side validation for price > 0"],
        ["Information Disclosure", "curl", "GET /booking with token", "Limited data with ownership check", "Full guest details exposed to all users", "YES", "firstname, lastname, prices visible to all", "Implement data filtering based on user role"],
        ["IDOR - Unauthorized Access", "curl", "GET /booking/1 with admin token", "Access denied or forbidden", "HTTP 200 - data accessible", "NO", "Authorization check appears functional", "Continue monitoring"],
    ]

    for test in shannon_tests:
        vuln = test[5]
        style = high_style if vuln == "YES" else clean_style
        add_row(shannon_sheet, test, style)

    add_row(shannon_sheet, [""], normal_style)

    # Shannon Priority Action Items
    add_row(shannon_sheet, ["PRIORITY ACTION ITEMS"], title_style)
    add_row(shannon_sheet, ["Priority", "Action Item", "Timeline", "Owner", "Status", "Notes"], header_style)

    action_items = [
        ["P0 - CRITICAL", "Fix SQL Injection in checkin/checkout parameters", "24-48 hours", "Backend Team", "NOT STARTED", "Use parameterized queries"],
        ["P0 - CRITICAL", "Implement proper authorization checks (IDOR fix)", "24-48 hours", "Backend Team", "NOT STARTED", "Verify data ownership before access"],
        ["P1 - HIGH", "Implement input sanitization for XSS", "1 week", "Backend Team", "NOT STARTED", "Sanitize firstname, lastname, additionalneeds"],
        ["P1 - HIGH", "Add input validation (prices, dates)", "1 week", "Backend Team", "NOT STARTED", "Reject invalid values server-side"],
        ["P2 - MEDIUM", "Implement data filtering/redaction", "2 weeks", "Backend Team", "NOT STARTED", "Hide sensitive info from unauthorized users"],
    ]

    for item in action_items:
        priority = item[0]
        if "CRITICAL" in priority:
            style = critical_style
        elif "HIGH" in priority:
            style = high_style
        else:
            style = medium_style
        add_row(shannon_sheet, item, style)

    doc.spreadsheet.addElement(shannon_sheet)

    # Save
    output_path = "/home/shivam/restful-booker-api/Security_Assessment_Complete_Report.ods"
    doc.save(output_path)
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
