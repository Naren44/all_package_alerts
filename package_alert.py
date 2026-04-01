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


def fetch_advisories():
    url = "https://api.github.com/advisories?per_page=20"

    print("📡 Fetching GitHub Advisories...")

    response = requests.get(url)

    print("GitHub status:", response.status_code)

    if response.status_code != 200:
        return []

    return response.json()


def main():
    print("🚀 Running FULL advisory scan...")

    advisories = fetch_advisories()

    if not advisories:
        send_to_slack("⚠️ No advisories fetched")
        return

    alerts = 0

    for adv in advisories:
        summary = adv.get("summary", "No summary")
        severity = adv.get("severity", "unknown")
        ecosystem = adv.get("ecosystem", "unknown")

        # package info (if available)
        pkg_name = "unknown"
        if "vulnerabilities" in adv and adv["vulnerabilities"]:
            pkg_name = adv["vulnerabilities"][0].get("package", {}).get("name", "unknown")

        message = f"""
🚨 SECURITY ADVISORY

📦 Package: {pkg_name}
🧬 Ecosystem: {ecosystem}
⚠️ Severity: {severity}

📝 {summary}
"""

        send_to_slack(message)
        alerts += 1

    print(f"✅ Total alerts sent: {alerts}")


if __name__ == "__main__":
    main()
