import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_to_slack(text):
    print("➡️ Sending to Slack...")

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": text}
    )

    print("Slack status:", response.status_code)


def fetch_osv_feed():
    url = "https://api.osv.dev/v1/vulns"

    print("📡 Fetching OSV global feed...")

    response = requests.get(url)

    print("OSV status:", response.status_code)

    data = response.json()

    vulns = data.get("vulns", [])

    print(f"📊 Total vulnerabilities fetched: {len(vulns)}")

    return vulns


def main():
    print("🚀 Running OSV FEED scan...")

    vulns = fetch_osv_feed()

    if not vulns:
        send_to_slack("⚠️ OSV feed returned no data")
        return

    # 🔥 Take first vuln for testing
    v = vulns[0]

    vuln_id = v.get("id", "N/A")
    summary = v.get("summary", "No summary")

    affected = v.get("affected", [])
    name = "unknown"
    ecosystem = "unknown"

    if affected:
        pkg = affected[0].get("package", {})
        name = pkg.get("name", "unknown")
        ecosystem = pkg.get("ecosystem", "unknown")

    message = f"""
🚨 OSV FEED ALERT

📦 Package: {name}
🧬 Ecosystem: {ecosystem}
🆔 ID: {vuln_id}

📝 {summary}
"""

    send_to_slack(message)


if __name__ == "__main__":
    main()
