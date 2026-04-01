import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_to_slack(text):
    print("➡️ Sending test alert...")

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": text}
    )

    print("Status:", response.status_code)
    print("Response:", response.text)


def main():
    print("🚀 Running ALERT TEST")

    send_to_slack("🔥 ALERT TEST: Pipeline is working correctly!")


if __name__ == "__main__":
    main()
