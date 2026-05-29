import time
import logging
from datetime import datetime

from watcher.config import load_config
from watcher.git_utils import git_fetch, get_latest_commit, is_git_repo
from watcher.notifier import send_notification

config = load_config()

CHECK_INTERVAL = config["check_interval"]
REPOSITORIES = config["repositories"]


logging.basicConfig(
    filename="log/watcher.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)


def print_header():

    print("=" * 60)
    print("Git Watcher Started")
    print("=" * 60)

    print(f"Repositories : {len(REPOSITORIES)}")
    print(f"Interval     : {CHECK_INTERVAL} sec")
    print()

    for repo in REPOSITORIES:

        print(f"• {repo['name']}")
        print(f"  Path   : {repo['path']}")
        print(f"  Remote : {repo['remote']}")
        print(f"  Branch : {repo['branch']}")
        print()


def main():

    last_commits = {}

    print_header()

    while True:

        try:

            for repo in REPOSITORIES:

                repo_name = repo["name"]
                repo_path = repo["path"]
                remote = repo["remote"]
                branch = repo["branch"]

                if not is_git_repo(repo_path):

                    print(f"[{repo_name}] Invalid Git Repository")

                    continue

                git_fetch(repo_path, remote)

                commit = get_latest_commit(repo_path, remote, branch)

                # First Run
                if repo_name not in last_commits:

                    last_commits[repo_name] = commit["sha"]

                    print(f"[{repo_name}] " f"Loaded: {commit['message']}")

                    logging.info(
                        f"{repo_name} | "
                        f"Initial Commit | "
                        f"{commit['author']} | "
                        f"{commit['message']}"
                    )

                # New Commit
                elif commit["sha"] != last_commits[repo_name]:

                    print()
                    print("=" * 60)
                    print(f"NEW COMMIT DETECTED IN {repo_name}")
                    print("=" * 60)

                    print(
                        f"Detected At : "
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    print(f"Repository  : {repo_name}")

                    print(f"Author      : {commit['author']}")

                    if "email" in commit:

                        print(f"Email       : {commit['email']}")

                    print(f"Message     : {commit['message']}")

                    print(f"Commit Date : {commit['date']}")

                    send_notification(
                        f"🚀 New Commit • {repo_name}",
                        (
                            f"🌿 Branch : {branch}\n"
                            f"👤 Author : {commit['author']}\n"
                            f"📝 Commit : {commit['message']}"
                        ),
                    )
                   
                    logging.info(
                        f"{repo_name} | "
                        f"New Commit | "
                        f"{commit['author']} | "
                        f"{commit['message']}"
                    )

                    last_commits[repo_name] = commit["sha"]

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:

            print("\nWatcher Stopped.")
            break

        except Exception as error:

            print(f"\nError: {error}")

            logging.error(str(error))

            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
