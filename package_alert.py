import requests
from datetime import datetime, timedelta
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


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

    # 🔥 7-day window (for testing)
    since = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"

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


def main():
    print("🚀 Running OSV test scan...")

    vulns = fetch_osv_vulns()

    if not vulns:
        print("❌ No vulnerabilities returned from OSV")
        send_to_slack("⚠️ OSV returned no data (unexpected)")
        return

    # 🔥 Take first vulnerability (test)
    first = vulns[0]

    vuln_id = first.get("id", "N/A")
    summary = first.get("summary", "No summary")

    affected = first.get("affected", [])
    pkg_name = "unknown"
    ecosystem = "unknown"

    if affected:
        pkg = affected[0].get("package", {})
        pkg_name = pkg.get("name", "unknown")
        ecosystem = pkg.get("ecosystem", "unknown")

    print("🆔 ID:", vuln_id)
    print("📦 Package:", pkg_name)
    print("🧬 Ecosystem:", ecosystem)
    print("📝 Summary:", summary)

    # 🚨 Force alert from OSV data
    message = f"""
🚨 OSV TEST ALERT

📦 Package: {pkg_name}
🧬 Ecosystem: {ecosystem}
🆔 ID: {vuln_id}

📝 {summary}
"""

    send_to_slack(message)


if __name__ == "__main__":
    main()
