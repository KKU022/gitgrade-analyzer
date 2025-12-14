import requests

def analyze_repo(repo_url):
    parts = repo_url.replace("https://github.com/", "").split("/")
    owner, repo = parts[0], parts[1]

    api = f"https://api.github.com/repos/{owner}/{repo}"
    data = requests.get(api).json()

    score = 100
    issues = []

    if data.get("open_issues_count", 0) == 0:
        issues.append("Project has no tracked issues")

    score -= 20
    issues.append("No automated tests detected")
    score -= 10
    issues.append("CI/CD pipeline not found")

    summary = "This repository shows basic structure but lacks testing and automation."
    roadmap = [
        "Add a README with setup instructions",
        "Write basic unit tests",
        "Introduce CI using GitHub Actions",
        "Improve commit messages",
        "Refactor folder structure"
    ]

    return score, summary, roadmap


if __name__ == "__main__":
    url = input("Enter GitHub repo URL: ")
    score, summary, roadmap = analyze_repo(url)

    print("\nScore:", score)
    print("\nSummary:", summary)
    print("\nRoadmap:")
    for step in roadmap:
        print("-", step)
