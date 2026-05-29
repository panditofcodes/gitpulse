import subprocess


def is_git_repo(repo_path):
    """
    Check whether a path is a valid Git repository.
    """

    try:

        result = subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "rev-parse",
                "--is-inside-work-tree",
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0 and result.stdout.strip() == "true"

    except Exception:
        return False


def git_fetch(repo_path, remote):
    """
    Fetch latest changes from remote.
    """

    try:

        result = subprocess.run(
            [
                "git",
                "-C",
                repo_path,
                "fetch",
                remote,
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    except Exception:
        return False


def get_latest_commit(repo_path, remote, branch):
    """
    Get latest commit information from remote branch.
    """

    cmd = [
        "git",
        "-C",
        repo_path,
        "log",
        f"{remote}/{branch}",
        "-1",
        "--pretty=format:%H|%an|%ae|%s|%cd",
        "--date=local",
    ]

    result = subprocess.check_output(
        cmd,
        text=True,
    ).strip()

    sha, author, email, message, date = result.split("|", 4)

    return {
        "sha": sha,
        "author": author,
        "email": email,
        "message": message,
        "date": date,
    }


def get_commit_count(repo_path, old_sha, new_sha):
    """
    Returns number of commits between two SHAs.
    """

    try:

        cmd = [
            "git",
            "-C",
            repo_path,
            "rev-list",
            "--count",
            f"{old_sha}..{new_sha}",
        ]

        result = subprocess.check_output(
            cmd,
            text=True,
        ).strip()

        return int(result)

    except Exception:
        return 0


def get_new_commits(repo_path, old_sha, new_sha):
    """
    Returns all commits between old_sha and new_sha.
    Useful for future versions.
    """

    try:

        cmd = [
            "git",
            "-C",
            repo_path,
            "log",
            f"{old_sha}..{new_sha}",
            "--pretty=format:%H|%an|%ae|%s|%cd",
            "--date=local",
        ]

        result = subprocess.check_output(
            cmd,
            text=True,
        ).strip()

        if not result:
            return []

        commits = []

        for line in result.splitlines():

            sha, author, email, message, date = line.split("|", 4)

            commits.append(
                {
                    "sha": sha,
                    "author": author,
                    "email": email,
                    "message": message,
                    "date": date,
                }
            )

        return commits

    except Exception:
        return []
