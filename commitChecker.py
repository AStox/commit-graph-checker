import smtplib
import requests
from github import Github, GithubException
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()


def send_email_notification():
    print("No commits today!")
    subject = "Commit Reminder"
    body = "No commits today!"
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
    g = Github(access_token, timeout=60)
    user = g.get_user(os.getenv("GITHUB_USERNAME"))
    since_date = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    print(f"Checking commits since {since_date}...")

    repos = get_repos(access_token)
    for repo_data in repos:
        if repo_data["size"] == 0:
            continue
        repo = g.get_repo(repo_data["full_name"])
        try:
            for branch in repo.get_branches():
                commits = repo.get_commits(
                    sha=branch.name, since=since_date, author=user
                )
                for commit in commits:
                    print(
                        f"Found commit at {commit.commit.author.date} in {repo.full_name}: {commit.commit.message}"
                    )
                    return
        except GithubException as e:
            if e.status == 409:
                print(f"Skipping empty repository: {repo.full_name}")
                continue
            else:
                raise e

    send_email_notification()


check_commits()
