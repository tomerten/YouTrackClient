"""
YouTrack API client implementation.

This module provides the YouTrackClient class for interacting with the YouTrack REST API.

Features:
- Authenticate with YouTrack using a personal access token
- Create, update, search, and list issues
- Add comments, transition issues, and attach files
- Retrieve issue history and changes
- List and manage workitems (time tracking)
- Find IDs for projects, issues, users, custom fields, workflows, boards, user stories, and more
- Manage agile boards, sprints, and user stories (epics)
- Run reports and retrieve deadline calendars
- Manage issue links and link types
- Run queries and commands on issues

Usage:
    from youtrack.client import YouTrackClient
    client = YouTrackClient.from_config()
    issues = client.list_issues(project_id="0-0")

See each method's docstring for details.
"""

import toml
import requests
from pathlib import Path
from typing import Optional

class YouTrackError(Exception):
    """Custom exception for YouTrack API errors with meaningful messages."""
    pass

class YouTrackClient:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    @classmethod
    def from_config(cls, config_path: Optional[str] = None):
        """
        Load YouTrack credentials from a .youtrack.toml file.
        """
        config_file = config_path or str(Path.home() / ".youtrack.toml")
        config = toml.load(config_file)
        token = config["youtrack"]["token"]
        base_url = config["youtrack"]["base_url"]
        return cls(token, base_url)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            try:
                error = response.json()
                message = error.get('error_description') or error.get('message') or str(error)
            except Exception:
                message = response.text
            raise YouTrackError(f"YouTrack API error: {message}") from e
        return response.json()

    def create_issue(self, project_id: str, summary: str, description: str = "", custom_fields: dict = None, story_points: int = None):
        """
        Create a new issue in the specified project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param summary: The issue summary/title.
        :type summary: str
        :param description: The issue description.
        :type description: str, optional
        :param custom_fields: Custom fields to set.
        :type custom_fields: dict, optional
        :param story_points: Value for the 'Story points' custom field. Required in some workflows.
        :type story_points: int, optional
        :return: The created issue data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description"
        data = {
            "project": {"id": project_id},
            "summary": summary,
            "description": description
        }
        # Always include 'Story points' if provided
        custom_fields = custom_fields.copy() if custom_fields else {}
        if story_points is not None:
            custom_fields["Story points"] = {"name": str(story_points), "value": story_points}
        if custom_fields:
            data["customFields"] = [
                {"name": k, **(v if isinstance(v, dict) else {"value": v})}
                for k, v in custom_fields.items()
            ]
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def list_issues(self, project_id: str, query: str = "", limit: int = 20, skip: int = 0):
        """
        List issues in a project with optional query and pagination.

        :param project_id: The ID of the project.
        :type project_id: str
        :param query: YouTrack query string.
        :type query: str, optional
        :param limit: Max results to return.
        :type limit: int, optional
        :param skip: Results to skip.
        :type skip: int, optional
        :return: List of issues.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description&query=project:{project_id} {query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def update_issue(self, issue_id: str, summary: str = None, description: str = None, custom_fields: dict = None):
        """
        Update an existing issue with new information.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param summary: New summary.
        :type summary: str, optional
        :param description: New description.
        :type description: str, optional
        :param custom_fields: Custom fields to update.
        :type custom_fields: dict, optional
        :return: The updated issue data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}?fields=id,summary,description"
        data = {}
        if summary is not None:
            data["summary"] = summary
        if description is not None:
            data["description"] = description
        if custom_fields:
            data["customFields"] = custom_fields
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def search_issues(self, query: str, limit: int = 20, skip: int = 0):
        """
        Search for issues using a YouTrack query.

        :param query: YouTrack query string.
        :type query: str
        :param limit: Max results to return.
        :type limit: int, optional
        :param skip: Results to skip.
        :type skip: int, optional
        :return: List of issues.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description&query={query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_comment(self, issue_id: str, text: str):
        """
        Add a comment to an issue.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param text: The comment text.
        :type text: str
        :return: The created comment data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}/comments?fields=id,text,author"
        data = {"text": text}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def transition_issue(self, issue_id: str, field_name: str, new_state: str):
        """
        Transition an issue to a new workflow state by updating a custom field (e.g., State).

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param field_name: The custom field name (e.g., 'State').
        :type field_name: str
        :param new_state: The new state value.
        :type new_state: str
        :return: The updated issue data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}/fields/{field_name}"
        data = {"name": field_name, "value": {"name": new_state}}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def attach_file(self, issue_id: str, file_path: str):
        """
        Attach a file to an issue.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param file_path: Path to the file to attach.
        :type file_path: str
        :return: The attachment data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}/attachments?fields=id,name"
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(url, files=files, headers=headers)
        return self._handle_response(response)

    def get_issue_history(self, issue_id: str):
        """
        Retrieve the history and changes of an issue.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :return: List of activity records.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues/{issue_id}/activities?fields=id,timestamp,author,added,removed"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_workitems(self, project_id: str, limit: int = 20, skip: int = 0):
        """
        List workitems (time tracking entries) in a project, with pagination support.

        :param project_id: The ID of the project.
        :type project_id: str
        :param limit: Max results to return.
        :type limit: int, optional
        :param skip: Results to skip.
        :type skip: int, optional
        :return: List of workitems.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,workItems(id,duration,author,date,description)&query=project:{project_id}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def calculate_time_spent(self, issue_id: str):
        """
        Calculate total time spent on an issue by summing its workitems' durations.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :return: Total time spent (minutes).
        :rtype: int
        """
        url = f"{self.base_url}/api/issues/{issue_id}/timeTracking/workItems?fields=duration"
        response = requests.get(url, headers=self._headers())
        workitems = self._handle_response(response)
        total = sum(wi.get('duration', 0) for wi in workitems)
        return total

    def list_workitem_types(self, project_id: str):
        """
        List allowed workitem types for a project.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: List of workitem types.
        :rtype: list
        """
        url = f"{self.base_url}/api/admin/projects/{project_id}/timetrackingsettings/workitemtypes?fields=id,name,localizedName"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_spent_time(self, issue_id: str, duration: int, workitem_type_id: str, description: str = ""):
        """
        Add spent time (workitem) to an issue. Duration is in minutes. workitem_type_id is required.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param duration: Time spent in minutes.
        :type duration: int
        :param workitem_type_id: The workitem type ID.
        :type workitem_type_id: str
        :param description: Description for the workitem.
        :type description: str, optional
        :return: The created workitem data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}/timeTracking/workItems?fields=id,duration,description,type(id,name)"
        data = {"duration": duration, "description": description, "type": {"id": workitem_type_id}}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def list_projects(self):
        """
        List all projects in the YouTrack instance.

        :return: List of projects, each as a dict with 'id', 'name', and 'shortName'.
        :rtype: list
        """
        url = f"{self.base_url}/api/admin/projects?fields=id,name,shortName"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def get_issue(self, issue_id: str):
        """
        Retrieve details for a specific issue by its ID.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :return: Issue details including id, summary, description, and project info.
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}?fields=id,summary,description,project(id,name)"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_users(self, query: str = "", limit: int = 20, skip: int = 0):
        """
        List users in the YouTrack instance, optionally filtered by a query string.

        :param query: Query string to filter users (e.g., by name or email).
        :type query: str, optional
        :param limit: Maximum number of users to return.
        :type limit: int, optional
        :param skip: Number of users to skip (for pagination).
        :type skip: int, optional
        :return: List of user dicts with id, login, name, and email.
        :rtype: list
        """
        url = f"{self.base_url}/api/users?fields=id,login,name,email&query={query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_custom_fields(self, project_id: str):
        """
        List custom fields for a given project.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: List of custom fields with id, name, and field type info.
        :rtype: list
        """
        url = f"{self.base_url}/api/admin/projects/{project_id}/customfields?fields=id,name,fieldType(id,valueType)"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_workflows(self):
        """
        List all workflows in the YouTrack instance.

        :return: List of workflows with id, name, and description.
        :rtype: list
        """
        url = f"{self.base_url}/api/workflows?fields=id,name,description"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_boards(self, project_id: str = None):
        """
        List all agile boards. Optionally filter boards by project ID.

        :param project_id: If provided, only boards containing this project are returned.
        :type project_id: str, optional
        :return: List of boards with id, name, and associated projects.
        :rtype: list
        """
        url = f"{self.base_url}/api/agiles?fields=id,name,projects(id,name)"
        response = requests.get(url, headers=self._headers())
        boards = self._handle_response(response)
        if project_id:
            boards = [b for b in boards if any(p['id'] == project_id for p in b.get('projects', []))]
        return boards

    def list_sprints(self, board_id: str):
        """
        List all sprints for a given agile board.

        :param board_id: The ID of the agile board.
        :type board_id: str
        :return: List of sprints with id, name, start, finish, and isArchived status.
        :rtype: list
        """
        url = f"{self.base_url}/api/agiles/{board_id}/sprints?fields=id,name,start,finish,isArchived"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_user_stories(self, board_id: str, sprint_id: str = None):
        """
        List user stories (epics) on a board, optionally for a specific sprint.

        :param board_id: The ID of the agile board.
        :type board_id: str
        :param sprint_id: The ID of the sprint. If provided, only user stories in this sprint are listed.
        :type sprint_id: str, optional
        :return: List of user stories with id, summary, and custom fields.
        :rtype: list
        """
        url = f"{self.base_url}/api/agiles/{board_id}/issues?fields=id,summary,customFields(id,name,value(name))"
        if sprint_id:
            url += f"&sprint={sprint_id}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_issue_to_sprint(self, board_id: str, sprint_id: str, issue_id: str):
        """
        Add an issue to a sprint on a specific agile board.

        :param board_id: The ID of the agile board.
        :type board_id: str
        :param sprint_id: The ID of the sprint.
        :type sprint_id: str
        :param issue_id: The ID of the issue to add.
        :type issue_id: str
        :return: The response from the API (usually the updated sprint or issue info).
        :rtype: dict
        """
        url = f"{self.base_url}/api/agiles/{board_id}/sprints/{sprint_id}/issues/{issue_id}"
        response = requests.put(url, headers=self._headers())
        return self._handle_response(response)

    def add_issue_to_user_story(self, board_id: str, user_story_id: str, issue_id: str):
        """
        Add an issue as a subtask to a user story (epic) on a board.

        :param board_id: The ID of the agile board.
        :type board_id: str
        :param user_story_id: The ID of the user story (epic).
        :type user_story_id: str
        :param issue_id: The ID of the issue to add as a subtask.
        :type issue_id: str
        :return: The response from the API (usually the updated user story or issue info).
        :rtype: dict
        """
        url = f"{self.base_url}/api/agiles/{board_id}/issues/{user_story_id}/subtasks/{issue_id}"
        response = requests.put(url, headers=self._headers())
        return self._handle_response(response)

    def add_user_story_to_sprint(self, board_id: str, sprint_id: str, user_story_id: str):
        """
        Add a user story (epic) to a sprint on a board.

        :param board_id: The ID of the agile board.
        :type board_id: str
        :param sprint_id: The ID of the sprint.
        :type sprint_id: str
        :param user_story_id: The ID of the user story (epic) to add.
        :type user_story_id: str
        :return: The response from the API (usually the updated sprint or user story info).
        :rtype: dict
        """
        url = f"{self.base_url}/api/agiles/{board_id}/sprints/{sprint_id}/issues/{user_story_id}"
        response = requests.put(url, headers=self._headers())
        return self._handle_response(response)

    def run_report(self, report_id: str):
        """
        Run a report by its ID and return the result.

        :param report_id: The ID of the report to execute.
        :type report_id: str
        :return: The report execution result.
        :rtype: dict
        """
        url = f"{self.base_url}/api/reports/{report_id}/execute"
        response = requests.post(url, headers=self._headers())
        return self._handle_response(response)

    def authenticate(self):
        """
        Placeholder for authentication logic. Not required for token-based auth.
        """
        pass

    def get_deadline_calendars(self):
        """
        Retrieve all deadline calendars (holiday calendars) in the instance.

        :return: List of calendars with id, name, and holidays.
        :rtype: list
        """
        url = f"{self.base_url}/api/admin/calendars?fields=id,name,holidays"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def get_issue_links(self, issue_id: str):
        """
        Get all links for a specific issue.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :return: List of issue links with id, direction, link type, and linked issues.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues/{issue_id}/links?fields=id,direction,linkType(id,name,directed),issues(id,summary)"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_issue_link_types(self):
        """
        List all available issue link types in the instance.

        :return: List of link types with id, name, and direction info.
        :rtype: list
        """
        url = f"{self.base_url}/api/issueLinkTypes?fields=id,name,directed"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_issue_link_types_for_issue(self, issue_id: str):
        """
        List link types available for a specific issue.

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :return: List of link types for the issue.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues/{issue_id}/links/types?fields=id,name,directed"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_issue_link_types_for_project(self, project_id: str):
        """
        List link types available for a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: List of link types for the project.
        :rtype: list
        """
        url = f"{self.base_url}/api/admin/projects/{project_id}/issueLinkTypes?fields=id,name,directed"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_issue_link(self, source_issue_id: str, target_issue_id: str, link_type_id: str):
        """
        Add a link between two issues using a specific link type.

        :param source_issue_id: The ID of the source issue.
        :type source_issue_id: str
        :param target_issue_id: The ID of the target issue.
        :type target_issue_id: str
        :param link_type_id: The ID of the link type to use.
        :type link_type_id: str
        :return: The response from the API (usually the updated link info).
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{source_issue_id}/links/{link_type_id}/{target_issue_id}"
        response = requests.put(url, headers=self._headers())
        return self._handle_response(response)

    def run_query(self, query: str, fields: str = "id,summary,description", limit: int = 20, skip: int = 0):
        """
        Run a search query on issues, returning selected fields.

        :param query: YouTrack query string.
        :type query: str
        :param fields: Comma-separated fields to return for each issue.
        :type fields: str, optional
        :param limit: Max results to return.
        :type limit: int, optional
        :param skip: Results to skip.
        :type skip: int, optional
        :return: List of issues matching the query.
        :rtype: list
        """
        url = f"{self.base_url}/api/issues?fields={fields}&query={query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def run_command(self, issue_id: str, command: str, comment: str = None):
        """
        Run a command on an issue (e.g., change state, assign, add comment, etc.).

        :param issue_id: The ID of the issue.
        :type issue_id: str
        :param command: The command string to execute (YouTrack command language).
        :type command: str
        :param comment: Optional comment to add with the command.
        :type comment: str, optional
        :return: The response from the API (usually the updated issue info).
        :rtype: dict
        """
        url = f"{self.base_url}/api/issues/{issue_id}/execute"
        data = {"query": command}
        if comment:
            data["comment"] = {"text": comment}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)
