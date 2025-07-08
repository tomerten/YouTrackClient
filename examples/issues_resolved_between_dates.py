"""
Example: List issues resolved between two dates for a given project, using a custom state field 'Release Status'.
"""
from youtrack.client import YouTrackClient

client = YouTrackClient.from_config()

project_id = "0-0"  # Replace with your project ID
start_date = "2025-07-01"  # YYYY-MM-DD
end_date = "2025-07-08"    # YYYY-MM-DD

# YouTrack query: project:<project_id> 'Release Status':Resolved Resolved: {start_date} .. {end_date}
query = f"project:{project_id} 'Release Status':Resolved Resolved: {start_date} .. {end_date}"

issues = client.search_issues(query)

for issue in issues:
    print(f"{issue['id']}: {issue['summary']}")
