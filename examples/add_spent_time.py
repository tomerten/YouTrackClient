"""
Example: Add spent time (work item) to an issue.
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

issue_id = "0-0"  # Replace with your issue ID
workitem_type_id = "1-1"  # Replace with your work item type ID
time_minutes = 60

workitem = client.add_spent_time(
    issue_id=issue_id,
    duration=time_minutes,
    workitem_type_id=workitem_type_id,
    description="Worked on bugfix."
)
print("Added work item:", workitem["id"])
