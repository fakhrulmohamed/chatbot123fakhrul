"""
Helper script to push Crescent FAQ Chatbot to GitHub.
Works with or without Git installed on Windows using Dulwich.
"""

import sys
import os
import getpass
from dulwich.repo import Repo
from dulwich.porcelain import push

def main():
    repo_path = os.path.abspath(os.path.dirname(__file__))
    repo = Repo(repo_path)

    print("==================================================")
    print("  🚀 Push Crescent Chatbot to GitHub (@fakhrulmohamed)")
    print("==================================================")

    repo_name = input("Enter your GitHub repository name (default: crescent-college-faq-chatbot): ").strip()
    if not repo_name:
        repo_name = "crescent-college-faq-chatbot"

    target_url = f"https://github.com/fakhrulmohamed/{repo_name}.git"
    print(f"\nTarget Repository: {target_url}")

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("\nTo push securely to GitHub, you need a Personal Access Token (PAT).")
        print("Create one with 'repo' scope at: https://github.com/settings/tokens")
        token = input("Enter your GitHub Personal Access Token (PAT): ").strip()

    if not token:
        print("❌ Error: GitHub Token is required to push to a remote repository.")
        sys.exit(1)

    auth_url = f"https://fakhrulmohamed:{token}@github.com/fakhrulmohamed/{repo_name}.git"

    print("\nPushing to GitHub...")
    try:
        push(repo, auth_url, "refs/heads/master:refs/heads/main")
        print(f"\n✅ Successfully pushed to: https://github.com/fakhrulmohamed/{repo_name}")
    except Exception as e:
        # Fallback to push same ref
        try:
            push(repo, auth_url, "HEAD:refs/heads/main")
            print(f"\n✅ Successfully pushed to: https://github.com/fakhrulmohamed/{repo_name}")
        except Exception as err:
            print(f"\n❌ Push failed: {err}")
            print("\nPlease ensure:")
            print(f"1. You created the repository at https://github.com/new named '{repo_name}'")
            print("2. Your Personal Access Token has the 'repo' permission checked.")

if __name__ == "__main__":
    main()
