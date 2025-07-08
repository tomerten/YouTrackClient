import typer
from youtrack.client import YouTrackClient
from typing import Optional

app = typer.Typer(help="YouTrack CLI - interact with YouTrack from the command line.")

@app.command()
def list_issues(
    project_id: str = typer.Option(..., help="Project ID"),
    query: str = typer.Option("", help="YouTrack query string"),
    limit: int = typer.Option(20, help="Max results to return"),
    skip: int = typer.Option(0, help="Results to skip")
):
    """List issues in a project."""
    client = YouTrackClient.from_config()
    issues = client.list_issues(project_id, query, limit, skip)
    for issue in issues:
        typer.echo(f"{issue['id']}: {issue['summary']}")

@app.command()
def create_issue(
    project_id: str = typer.Option(..., help="Project ID"),
    summary: str = typer.Option(..., help="Issue summary/title"),
    description: str = typer.Option("", help="Issue description"),
    story_points: Optional[int] = typer.Option(None, help="Story points value")
):
    """Create a new issue."""
    client = YouTrackClient.from_config()
    issue = client.create_issue(
        project_id=project_id,
        summary=summary,
        description=description,
        story_points=story_points
    )
    typer.echo(f"Created issue: {issue['id']}")

@app.command()
def add_comment(
    issue_id: str = typer.Option(..., help="Issue ID"),
    text: str = typer.Option(..., help="Comment text")
):
    """Add a comment to an issue."""
    client = YouTrackClient.from_config()
    comment = client.add_comment(issue_id, text)
    typer.echo(f"Added comment: {comment['id']}")

@app.command()
def search_issues(
    query: str = typer.Option(..., help="YouTrack query string"),
    limit: int = typer.Option(20, help="Max results to return"),
    skip: int = typer.Option(0, help="Results to skip")
):
    """Search for issues using a YouTrack query."""
    client = YouTrackClient.from_config()
    issues = client.search_issues(query, limit, skip)
    for issue in issues:
        typer.echo(f"{issue['id']}: {issue['summary']}")

@app.command()
def update_issue(
    issue_id: str = typer.Option(..., help="Issue ID"),
    summary: Optional[str] = typer.Option(None, help="New summary"),
    description: Optional[str] = typer.Option(None, help="New description"),
    story_points: Optional[int] = typer.Option(None, help="Story points value"),
):
    """Update an existing issue."""
    client = YouTrackClient.from_config()
    custom_fields = {}
    if story_points is not None:
        custom_fields["Story points"] = {"name": str(story_points), "value": story_points}
    issue = client.update_issue(
        issue_id=issue_id,
        summary=summary,
        description=description,
        custom_fields=custom_fields if custom_fields else None
    )
    typer.echo(f"Updated issue: {issue['id']}")

@app.command()
def transition_issue(
    issue_id: str = typer.Option(..., help="Issue ID"),
    field_name: str = typer.Option(..., help="Custom field name (e.g., 'State' or 'Release Status')"),
    new_state: str = typer.Option(..., help="New state value")
):
    """Transition an issue to a new workflow state by updating a custom field."""
    client = YouTrackClient.from_config()
    issue = client.transition_issue(issue_id, field_name, new_state)
    typer.echo(f"Transitioned issue: {issue['id']}")

@app.command()
def attach_file(
    issue_id: str = typer.Option(..., help="Issue ID"),
    file_path: str = typer.Option(..., help="Path to file to attach")
):
    """Attach a file to an issue."""
    client = YouTrackClient.from_config()
    attachment = client.attach_file(issue_id, file_path)
    typer.echo(f"Attached file: {attachment['id']}")

@app.command()
def get_issue_history(
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Retrieve the history and changes of an issue."""
    client = YouTrackClient.from_config()
    history = client.get_issue_history(issue_id)
    typer.echo(history)

@app.command()
def list_workitems(
    project_id: str = typer.Option(..., help="Project ID"),
    limit: int = typer.Option(20, help="Max results to return"),
    skip: int = typer.Option(0, help="Results to skip")
):
    """List workitems (time tracking entries) in a project."""
    client = YouTrackClient.from_config()
    workitems = client.list_workitems(project_id, limit, skip)
    typer.echo(workitems)

@app.command()
def calculate_time_spent(
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Calculate total time spent on an issue."""
    client = YouTrackClient.from_config()
    total = client.calculate_time_spent(issue_id)
    typer.echo(f"Total time spent: {total} minutes")

@app.command()
def list_workitem_types(
    project_id: str = typer.Option(..., help="Project ID")
):
    """List allowed workitem types for a project."""
    client = YouTrackClient.from_config()
    types = client.list_workitem_types(project_id)
    typer.echo(types)

@app.command()
def add_spent_time(
    issue_id: str = typer.Option(..., help="Issue ID"),
    duration: int = typer.Option(..., help="Time spent in minutes"),
    workitem_type_id: str = typer.Option(..., help="Workitem type ID"),
    description: str = typer.Option("", help="Description for the workitem")
):
    """Add spent time (workitem) to an issue."""
    client = YouTrackClient.from_config()
    workitem = client.add_spent_time(issue_id, duration, workitem_type_id, description)
    typer.echo(f"Added workitem: {workitem['id']}")

@app.command()
def list_projects():
    """List all projects."""
    client = YouTrackClient.from_config()
    projects = client.list_projects()
    typer.echo(projects)

@app.command()
def get_issue(
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Get details for a specific issue."""
    client = YouTrackClient.from_config()
    issue = client.get_issue(issue_id)
    typer.echo(issue)

@app.command()
def list_users(
    query: str = typer.Option("", help="Query string to filter users"),
    limit: int = typer.Option(20, help="Max results to return"),
    skip: int = typer.Option(0, help="Results to skip")
):
    """List users."""
    client = YouTrackClient.from_config()
    users = client.list_users(query, limit, skip)
    typer.echo(users)

@app.command()
def list_custom_fields(
    project_id: str = typer.Option(..., help="Project ID")
):
    """List custom fields for a project."""
    client = YouTrackClient.from_config()
    fields = client.list_custom_fields(project_id)
    typer.echo(fields)

@app.command()
def list_workflows():
    """List all workflows."""
    client = YouTrackClient.from_config()
    workflows = client.list_workflows()
    typer.echo(workflows)

@app.command()
def list_boards(
    project_id: Optional[str] = typer.Option(None, help="Project ID to filter boards")
):
    """List all agile boards."""
    client = YouTrackClient.from_config()
    boards = client.list_boards(project_id)
    typer.echo(boards)

@app.command()
def list_sprints(
    board_id: str = typer.Option(..., help="Board ID")
):
    """List all sprints for a given agile board."""
    client = YouTrackClient.from_config()
    sprints = client.list_sprints(board_id)
    typer.echo(sprints)

@app.command()
def list_user_stories(
    board_id: str = typer.Option(..., help="Board ID"),
    sprint_id: Optional[str] = typer.Option(None, help="Sprint ID")
):
    """List user stories (epics) on a board."""
    client = YouTrackClient.from_config()
    stories = client.list_user_stories(board_id, sprint_id)
    typer.echo(stories)

@app.command()
def add_issue_to_sprint(
    board_id: str = typer.Option(..., help="Board ID"),
    sprint_id: str = typer.Option(..., help="Sprint ID"),
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Add an issue to a sprint on a board."""
    client = YouTrackClient.from_config()
    result = client.add_issue_to_sprint(board_id, sprint_id, issue_id)
    typer.echo(result)

@app.command()
def add_issue_to_user_story(
    board_id: str = typer.Option(..., help="Board ID"),
    user_story_id: str = typer.Option(..., help="User story (epic) ID"),
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Add an issue as a subtask to a user story (epic) on a board."""
    client = YouTrackClient.from_config()
    result = client.add_issue_to_user_story(board_id, user_story_id, issue_id)
    typer.echo(result)

@app.command()
def add_user_story_to_sprint(
    board_id: str = typer.Option(..., help="Board ID"),
    sprint_id: str = typer.Option(..., help="Sprint ID"),
    user_story_id: str = typer.Option(..., help="User story (epic) ID")
):
    """Add a user story (epic) to a sprint on a board."""
    client = YouTrackClient.from_config()
    result = client.add_user_story_to_sprint(board_id, sprint_id, user_story_id)
    typer.echo(result)

@app.command()
def run_report(
    report_id: str = typer.Option(..., help="Report ID")
):
    """Run a report by its ID and return the result."""
    client = YouTrackClient.from_config()
    result = client.run_report(report_id)
    typer.echo(result)

@app.command()
def get_deadline_calendars():
    """Retrieve all deadline calendars (holiday calendars) in the instance."""
    client = YouTrackClient.from_config()
    calendars = client.get_deadline_calendars()
    typer.echo(calendars)

@app.command()
def get_issue_links(
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """Get all links for a specific issue."""
    client = YouTrackClient.from_config()
    links = client.get_issue_links(issue_id)
    typer.echo(links)

@app.command()
def list_issue_link_types():
    """List all available issue link types in the instance."""
    client = YouTrackClient.from_config()
    types = client.list_issue_link_types()
    typer.echo(types)

@app.command()
def list_issue_link_types_for_issue(
    issue_id: str = typer.Option(..., help="Issue ID")
):
    """List link types available for a specific issue."""
    client = YouTrackClient.from_config()
    types = client.list_issue_link_types_for_issue(issue_id)
    typer.echo(types)

@app.command()
def list_issue_link_types_for_project(
    project_id: str = typer.Option(..., help="Project ID")
):
    """List link types available for a specific project."""
    client = YouTrackClient.from_config()
    types = client.list_issue_link_types_for_project(project_id)
    typer.echo(types)

@app.command()
def add_issue_link(
    source_issue_id: str = typer.Option(..., help="Source issue ID"),
    target_issue_id: str = typer.Option(..., help="Target issue ID"),
    link_type_id: str = typer.Option(..., help="Link type ID")
):
    """Add a link between two issues using a specific link type."""
    client = YouTrackClient.from_config()
    result = client.add_issue_link(source_issue_id, target_issue_id, link_type_id)
    typer.echo(result)

@app.command()
def run_query(
    query: str = typer.Option(..., help="YouTrack query string"),
    fields: str = typer.Option("id,summary,description", help="Comma-separated fields to return for each issue"),
    limit: int = typer.Option(20, help="Max results to return"),
    skip: int = typer.Option(0, help="Results to skip")
):
    """Run a search query on issues, returning selected fields."""
    client = YouTrackClient.from_config()
    issues = client.run_query(query, fields, limit, skip)
    typer.echo(issues)

@app.command()
def run_command(
    issue_id: str = typer.Option(..., help="Issue ID"),
    command: str = typer.Option(..., help="Command string to execute (YouTrack command language)"),
    comment: Optional[str] = typer.Option(None, help="Optional comment to add with the command")
):
    """Run a command on an issue (e.g., change state, assign, add comment, etc.)."""
    client = YouTrackClient.from_config()
    result = client.run_command(issue_id, command, comment)
    typer.echo(result)

if __name__ == "__main__":
    app()
