"""
Example: Add a comment to an existing issue.
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

issue_id = "0-0"  # Replace with your issue ID
comment = client.add_comment(issue_id, text="This is a comment from the example script.")
print("Added comment:", comment["id"])
