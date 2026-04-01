import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_to_slack(text):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": text}
    )
    print("Slack status:", response.status_code)


def fetch_github_advisories():
    url = "https://api.github.com/advisories?per_page=10"

    print("📡 Fetching GitHub Advisories...")

    response = requests.get(url)

    print("GitHub status:", response.status_code)

    if response.status_code != 200:
        return []

    return response.json()


def main():
    print("🚀 Running advisory scan...")

    advisories = fetch_github_advisories()

    if not advisories:
        send_to_slack("⚠️ No advisories fetched")
        return

    # take first advisory
    adv = advisories[0]

    summary = adv.get("summary", "No summary")
    severity = adv.get("severity", "unknown")
    ecosystem = adv.get("ecosystem", "unknown")

    message = f"""
🚨 NEW SECURITY ADVISORY

🧬 Ecosystem: {ecosystem}
⚠️ Severity: {severity}

📝 {summary}
"""

    send_to_slack(message)


if __name__ == "__main__":
    main()
