# Quick Reference: Running Shannon

## 📁 Locations
- **Shannon:** `/home/shivam/shannon/`
- **Your API:** `/home/shivam/restful-booker-api/`
- **API in Shannon:** `/home/shivam/shannon/repos/restful-booker-api/`
- **Config:** `/home/shivam/shannon/configs/restful-booker-api.yaml`

## 🚀 Quick Start (3 steps)

### Step 1: Add API Key
```bash
cd /home/shivam/shannon
echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' > .env
```

### Step 2: Start Pentest
```bash
./shannon start URL=https://restful-booker.herokuapp.com REPO=restful-booker-api WORKSPACE=restful-booker-audit
```

### Step 3: View Results (after ~1-1.5 hours)
```bash
# List all reports
ls -la audit-logs/

# View the main report
cat audit-logs/restful-booker.herokuapp.com_*/*/deliverables/comprehensive_security_assessment_report.md
```

## 📊 Monitoring Commands

```bash
# View live logs
./shannon logs

# Check workflow status
./shannon query ID=shannon-1234567890

# List all workspaces
./shannon workspaces

# Open Temporal UI
open http://localhost:8233
```

## ⏹️ Control Commands

```bash
# Stop gracefully
./shannon stop

# Stop and clean everything
./shannon stop CLEAN=true
```

## 📝 Expected Results

Shannon will generate a report with:
- ✅ Verified exploitable vulnerabilities
- ✅ Proof-of-Concept (PoC) code samples
- ✅ Detailed attack paths
- ✅ OWASP category classifications
- ✅ Risk severity levels

## ⚠️ Remember
- Only test on **sandboxed/staging environments**
- Shannon executes **real exploits** - data may be modified
- Typical cost: ~$50 USD per full run
- Typical duration: 1-1.5 hours

## 💬 Get Help
- **Community:** https://discord.gg/KAqzSHHpRt
- **GitHub Issues:** https://github.com/KeygraphHQ/shannon/issues
- **Full Guide:** See `SHANNON_INTEGRATION.md` in your API directory

---

**That's it!** Shannon handles everything automatically from here. 🤖
