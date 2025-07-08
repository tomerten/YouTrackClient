"""
Example: List all issues in a project and print their summaries.
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

project_id = "0-0"  # Replace with your project ID
issues = client.list_issues(project_id=project_id)

for issue in issues:
    print(f"{issue['id']}: {issue['summary']}")
