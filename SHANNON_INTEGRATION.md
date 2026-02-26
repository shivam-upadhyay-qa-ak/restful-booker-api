# Shannon Integration Guide - Restful Booker API

## Overview
Shannon is an autonomous AI pentester that performs dynamic security testing on web applications. This document explains how to use Shannon with your Restful Booker API.

## Prerequisites
- Docker Desktop installed and running
- Anthropic API key (get from https://console.anthropic.com/)
- Git installed

## Setup Instructions

### 1. Environment Configuration
Navigate to the shannon directory and create a `.env` file:

```bash
cd /home/shivam/shannon
cp .env.example .env
```

Edit `.env` and add your API credentials:
```bash
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
```

### 2. Running Shannon with Restful Booker API

The API repository has already been placed in `./repos/restful-booker-api/`

Run Shannon with the configuration:
```bash
cd /home/shivam/shannon

# Basic pentest
./shannon start URL=https://restful-booker.herokuapp.com REPO=restful-booker-api

# With custom configuration
./shannon start URL=https://restful-booker.herokuapp.com REPO=restful-booker-api CONFIG=./configs/restful-booker-api.yaml

# With named workspace (easier to track)
./shannon start URL=https://restful-booker.herokuapp.com REPO=restful-booker-api WORKSPACE=restful-booker-audit
```

### 3. Monitoring Progress

While Shannon runs:

```bash
# View real-time logs
./shannon logs

# Check specific workflow status
./shannon query ID=shannon-1234567890

# Open Temporal Web UI for detailed monitoring
open http://localhost:8233
```

### 4. Stopping Shannon

```bash
# Stop containers (preserves workflow data)
./shannon stop

# Full cleanup (removes all data)
./shannon stop CLEAN=true
```

## Output & Results

Once complete, Shannon generates a comprehensive security report:

**Location:** `./audit-logs/{hostname}_{sessionId}/`

**Report structure:**
```
audit-logs/
├── session.json                                    # Metrics and session data
├── agents/                                         # Per-agent execution logs
├── prompts/                                        # Prompt snapshots
└── deliverables/
    └── comprehensive_security_assessment_report.md # Final pentest report
```

## What Shannon Tests For

Shannon targets OWASP vulnerabilities including:
- ✅ Injection attacks (SQL, Command, etc.)
- ✅ Cross-Site Scripting (XSS)
- ✅ Broken Authentication & Authorization
- ✅ Server-Side Request Forgery (SSRF)

## Configuration Options

The configuration file (`./configs/restful-booker-api.yaml`) controls:
- API endpoints to test
- Vulnerability types to focus on
- Test data and payloads
- Rate limiting
- Output format

## Important Notes

### ⚠️ Critical Disclaimer
- **DO NOT** run Shannon on production environments
- Only run on sandboxed, staging, or **testing environments**
- Shannon executes real exploits and can modify data
- Potential side effects: creating users, modifying/deleting data, triggering unintended effects
- Make sure you have **explicit written authorization** to test the target

### Performance Characteristics
- **Time:** Typically 1-1.5 hours per full test run
- **Cost:** ~$50 USD using Anthropic Claude Sonnet (varies by complexity)
- **Rate:** Tests parallelized for faster results

## File Structure

After integration:
```
/home/shivam/shannon/
├── repos/
│   └── restful-booker-api/          # Your API code
├── configs/
│   ├── example-config.yaml
│   └── restful-booker-api.yaml      # Custom config for your API
├── audit-logs/                      # Test results saved here
├── .env                             # Your credentials (add this)
└── shannon                          # Main executable script
```

## Example: Running Your First Test

```bash
cd /home/shivam/shannon

# 1. Set environment
export ANTHROPIC_API_KEY="your-key-here"

# 2. Start pentest with named workspace
./shannon start \
  URL=https://restful-booker.herokuapp.com \
  REPO=restful-booker-api \
  WORKSPACE=first-audit

# 3. Monitor in another terminal
./shannon logs

# 4. View results (after completion)
cat audit-logs/restful-booker.herokuapp.com_*/{long-id}/deliverables/comprehensive_security_assessment_report.md
```

## Resuming Interrupted Tests

If a pentest is interrupted, resume it from where it left off:

```bash
./shannon start \
  URL=https://restful-booker.herokuapp.com \
  REPO=restful-booker-api \
  WORKSPACE=first-audit
```

Shannon will detect completed agents and skip them.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker not found | Install Docker Desktop and ensure it's running |
| Permission denied on scripts | Run `chmod +x /home/shivam/shannon/shannon` |
| API key not recognized | Verify `ANTHROPIC_API_KEY` in `.env` is correct |
| Port 8233 in use | Change Temporal UI port or stop other containers |
| Slow performance | Run on a machine with sufficient CPU/RAM for Docker |

## Additional Resources

- **Shannon Repo:** https://github.com/KeygraphHQ/shannon
- **Keygraph Website:** https://keygraph.io/
- **Discord Community:** https://discord.gg/KAqzSHHpRt
- **Sample Reports:** View example penetration tests in `/sample-reports/`

## Next Steps

1. Add your Anthropic API key to `.env`
2. Run your first test: `./shannon start URL=https://restful-booker.herokuapp.com REPO=restful-booker-api`
3. Monitor with `./shannon logs`
4. Review the final report in `audit-logs/`
5. Implement fixes for any reported vulnerabilities
