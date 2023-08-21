import smtplib
import requests
import time
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def send_email_notification(
    subject="Commit Reminder", body="You have until 7pm to commit something!"
):
    print("No commits today!")
    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT")) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
        server.sendmail(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_TO"), msg)


def get_repos(access_token):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {access_token}"}
    repos = []
    page = 1
    while True:
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)
        if not response.json():
            break
        repos.extend(response.json())
        page += 1
    return repos


def check_commits():
    access_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    url = f"https://api.github.com/users/{username}/events"
    headers = {"Authorization": f"token {access_token}"}
    since_date = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    print(f"Since:    {since_date}")
    print(f"now:      {datetime.now(timezone.utc)}")

    response = requests.get(url, headers=headers, params={"since": since_date})
    events = response.json()

    commits_today = False
    for event in events:
        # print push events and the time it happened and the commit message
        if event["type"] == "PushEvent":
            print(
                event["type"],
                event["created_at"],
                event["payload"]["commits"][0]["message"],
            )
            commit_date = datetime.fromisoformat(
                event["created_at"].replace("Z", "+00:00")
            )
            if commit_date < since_date:
                continue  # Skip this commit as it's before the since date
            commits_today = True
            # email number of commits
            send_email_notification(
                subject="Commit Reminder",
                body=f"You committed something today at {commit_date}! In total, you committed {len(event['payload']['commits'])} times.",
            )
            print(
                f"Found commit in {event['repo']['name']}: {event['payload']['commits'][0]['message']}, time: {event['created_at']}"
            )
            break

    if not commits_today:
        print("No commits today!")
        send_email_notification()


def check_rate_limit(access_token):
    url = "https://api.github.com/users/octocat"  # You can replace 'octocat' with your username
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, headers=headers)

    rate_limit = response.headers["x-ratelimit-limit"]
    remaining = response.headers["x-ratelimit-remaining"]
    used = response.headers["x-ratelimit-used"]
    reset_time = datetime.fromtimestamp(int(response.headers["x-ratelimit-reset"]))

    print(f"Rate Limit: {rate_limit}")
    print(f"Remaining: {remaining}")
    print(f"Used: {used}")
    print(f"Reset Time: {reset_time}")


# access_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
# check_rate_limit(access_token)

check_commits()
