# YouTrack Python API Client

A comprehensive Python client for the YouTrack REST API. Supports authentication, issue management, work items, boards, sprints, user stories, reports, deadlines, links, queries, and commands.

## Features

- Authenticate with YouTrack using a personal access token
- Create, update, search, and list issues
- Add comments, transition issues, and attach files
- Retrieve issue history and changes
- List and manage work items (time tracking)
- Find IDs for projects, issues, users, custom fields, workflows, boards, user stories, and more
- Manage agile boards, sprints, and user stories (epics)
- Run reports and retrieve deadline calendars
- Manage issue links and link types
- Run queries and commands on issues

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
poetry install
```

## Configuration

Create a `.youtrack.toml` file in your home directory with the following content:

```toml
[youtrack]
token = "<your-youtrack-token>"
base_url = "https://your-youtrack-instance.myjetbrains.com/youtrack"
```

## Usage Example

```python
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

# List issues in a project
issues = client.list_issues(project_id="0-0")
for issue in issues:
    print(issue["id"], issue["summary"])

# Create a new issue
new_issue = client.create_issue(
    project_id="0-0",
    summary="Sample bug report",
    description="Steps to reproduce..."
)
print("Created issue:", new_issue["id"])
```

See the [examples/](examples/) directory for more usage patterns.

## API Reference

See method docstrings in `src/youtrack/client.py` for full details on all available operations.

---

This project is not affiliated with JetBrains or YouTrack. Licensed under the MIT License.
