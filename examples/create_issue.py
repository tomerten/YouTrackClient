"""
Example: Create a new issue in a project.
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

project_id = "0-0"  # Replace with your project ID
new_issue = client.create_issue(
    project_id=project_id,
    summary="Example bug report from script",
    description="Steps to reproduce: ..."
)
print("Created issue:", new_issue["id"])
