import requests
from datetime import datetime, timedelta
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

KEYWORDS = [
    "malicious",
    "typosquat",
    "dependency confusion",
    "backdoor",
    "credential",
    "token",
    "exfiltrate"
]


def send_to_slack(text):
    print("➡️ Sending to Slack...")

    if not SLACK_WEBHOOK_URL:
        print("❌ Missing Slack webhook")
        return

    response = requests.post(SLACK_WEBHOOK_URL, json={"text": text})

    print("Slack status:", response.status_code)
    print("Slack response:", response.text)


def fetch_osv_vulns():
    url = "https://api.osv.dev/v1/query"

    # 🔥 1 hour window
    since = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"

    payload = {
        "query": {
            "modified_since": since
        }
    }

    print("📡 Calling OSV API...")
    response = requests.post(url, json=payload)

    print("OSV status:", response.status_code)

    data = response.json()
    vulns = data.get("vulns", [])

    print(f"📊 Total vulnerabilities fetched: {len(vulns)}")

    return vulns


def is_relevant(v):
    vuln_id = v.get("id", "").lower()
    summary = v.get("summary", "").lower()

    # detect malicious advisories
    if vuln_id.startswith("mal"):
        return True

    # keyword-based detection
    return any(k in summary for k in KEYWORDS)


def main():
    print("🚀 Running supply chain scan (1-hour window)...")

    vulns = fetch_osv_vulns()

    alerts = 0

    for v in vulns:
        print("----- DEBUG START -----")

        vuln_id = v.get("id", "N/A")
        summary = v.get("summary", "No summary")

        affected = v.get("affected", [])
        if not affected:
            continue

        pkg = affected[0].get("package", {})
        name = pkg.get("name", "unknown")
        ecosystem = pkg.get("ecosystem", "unknown")

        print("🆔 ID:", vuln_id)
        print("📦 Package:", name)
        print("🧬 Ecosystem:", ecosystem)
        print("📝 Summary:", summary)
        print("----- DEBUG END -----")

        # 🔥 COMMENTED OUT ecosystem filter for visibility
        # if ecosystem not in ["npm", "pypi"]:
        #     continue

        if not is_relevant(v):
            continue

        message = f"""
🚨 SUPPLY CHAIN ALERT

📦 Package: {name}
🧬 Ecosystem: {ecosystem}
🆔 ID: {vuln_id}

📝 {summary}
"""

        send_to_slack(message)
        alerts += 1

    if alerts == 0:
        print("✅ No relevant supply chain threats in last 1 hour")


if __name__ == "__main__":
    main()
