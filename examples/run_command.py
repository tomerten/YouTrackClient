"""
Example: Run a YouTrack command on an issue (e.g., change state).
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

issue_id = "0-0"  # Replace with your issue ID
command = "State Fixed"  # Example command

result = client.run_command(issue_id, command, comment="Fixed in commit abc123.")
print("Command result:", result)
