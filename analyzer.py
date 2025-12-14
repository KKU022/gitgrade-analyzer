import json
import urllib.request


def fetch_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except:
        return None


def analyze_repo(repo_url):
    owner, repo = repo_url.replace("https://github.com/", "").split("/")[:2]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    data = fetch_json(api_url)
    if not data:
        return None

    score = 100

    # README check
    if not fetch_json(f"{api_url}/readme"):
        score -= 20

    # Commit count
    commits = fetch_json(f"{api_url}/commits")
    if not commits or len(commits) < 5:
        score -= 15

    # Folder structure check
    contents = fetch_json(f"{api_url}/contents")
    if not contents or not any("test" in item["name"].lower() for item in contents):
        score -= 20

    # CI/CD check
    if not fetch_json(f"{api_url}/contents/.github/workflows"):
        score -= 10

    score = max(0, score)

    summary = (
        "This repository shows a basic project setup. "
        "However, it lacks testing, automation, and detailed documentation, "
        "which are important for real-world software projects."
    )

    roadmap = [
        "Add a clear README with setup instructions",
        "Write basic unit tests",
        "Introduce CI using GitHub Actions",
        "Improve commit frequency and messages",
        "Refactor folder structure for clarity"
    ]

    return score, summary, roadmap


if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    result = analyze_repo(repo_url)

    if not result:
        print("Invalid repository URL or API error.")
    else:
        score, summary, roadmap = result
        print("\nScore:", score)
        print("\nSummary:", summary)
        print("\nRoadmap:")
        for step in roadmap:
            print("-", step)
