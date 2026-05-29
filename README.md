# GitPulse

GitPulse is a lightweight Git repository monitoring utility that continuously watches one or more local Git repositories and notifies you whenever new commits are pushed to the configured remote branches.

It is designed for developers who work with multiple repositories and want instant desktop notifications without constantly checking GitHub, GitLab, or running `git fetch` manually.

---

## Features

### Repository Monitoring

* Monitor multiple Git repositories simultaneously
* Watch any remote and branch combination
* Automatically fetch remote changes
* Detect new commits in real time

### Desktop Notifications

* Linux desktop notifications using `notify-send`
* Displays:

  * Repository name
  * Branch name
  * Commit author
  * Commit message
  * Commit SHA (optional)

### Configuration Management

* JSON-based configuration
* Simple configuration UI (`index.html`)
* Add repositories
* Edit repositories
* Delete repositories
* Save configuration directly to `config.json`

### Logging

* Logs all detected commits
* Logs watcher events and errors
* Persistent log file support

---

## Project Structure

```text
gitpulse/
├── config.json
├── index.html
├── main.py
├── log/
│   └── watcher.log
│
└── watcher/
    ├── __init__.py
    ├── config.py
    ├── git_utils.py
    ├── notifier.py
    └── requirements.txt
```

---

## Requirements

### System Packages

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install git libnotify-bin
```

Optional:

```bash
sudo apt install chromium
```

Chromium is recommended for using the configuration UI because it supports the File System Access API.

---

## Python Version

Recommended:

```text
Python 3.10+
```

Tested on:

```text
Python 3.12
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/panditofcodes/gitpulse
cd gitpulse
```

Install dependencies:

```bash
pip install -r watcher/requirements.txt
```

---

## Configuration

Create a `config.json` file:

```json
{
    "check_interval": 60,
    "repositories": [
        {
            "name": "Devfolio",
            "path": "/home/piyush/Projects/devfolio",
            "remote": "origin",
            "branch": "develop"
        },
        {
            "name": "Yuma",
            "path": "/home/piyush/yuma/benches/custom-erp/apps/yuma",
            "remote": "upstream",
            "branch": "develop"
        }
    ]
}
```

### Configuration Fields

| Field          | Description               |
| -------------- | ------------------------- |
| name           | Friendly repository name  |
| path           | Local repository path     |
| remote         | Git remote name           |
| branch         | Branch to monitor         |
| check_interval | Check interval in seconds |

---

## Running GitPulse

Start the watcher:

```bash
python3 main.py
```

Example:

```text
============================================================
GitPulse Started
============================================================

Repository : Devfolio
Remote     : origin
Branch     : develop
Interval   : 60 sec
```

---

## Example Notification

```text
🚀 Devfolio

🌿 develop
👤 Piyush Shukla
📝 Fix header formatting in README.md
```

---

## Configuration UI

Open:

```text
index.html
```

using Chromium or Chrome.

The UI supports:

* Open existing config file
* Create new config file
* Add repositories
* Edit repositories
* Delete repositories
* Save configuration

---

## Logs

Logs are stored in:

```text
log/watcher.log
```

Example:

```text
2026-05-30 10:15:20 - New Commit | Piyush Shukla | Fix README
```

---

## Future Roadmap

### Planned Features

* Enable/Disable repositories
* System tray integration
* Startup on boot
* Commit history viewer
* Sound notifications
* Branch-specific notifications
* Multiple notification themes
* Desktop application packaging
* Windows support
* GitHub/GitLab integration

---

## License

MIT License

---

## Author

**Piyush Shukla**

GitPulse was built to simplify repository monitoring and provide instant visibility into team activity across multiple projects.
