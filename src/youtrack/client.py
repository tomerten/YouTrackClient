"""
YouTrack API client implementation.
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

    def create_issue(self, project_id: str, summary: str, description: str = "", custom_fields: dict = None):
        """
        Create a new issue in the specified project.
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description"
        data = {
            "project": {"id": project_id},
            "summary": summary,
            "description": description
        }
        if custom_fields:
            data["customFields"] = custom_fields
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def list_issues(self, project_id: str, query: str = "", limit: int = 20, skip: int = 0):
        """
        List issues in a project with optional query, pagination supported.
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description&query=project:{project_id} {query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def update_issue(self, issue_id: str, summary: str = None, description: str = None, custom_fields: dict = None):
        """
        Update an existing issue with new information.
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
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,description&query={query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_comment(self, issue_id: str, text: str):
        """
        Add a comment to an issue.
        """
        url = f"{self.base_url}/api/issues/{issue_id}/comments?fields=id,text,author"
        data = {"text": text}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def transition_issue(self, issue_id: str, field_name: str, new_state: str):
        """
        Transition an issue to a new workflow state by updating a custom field (e.g., State).
        """
        url = f"{self.base_url}/api/issues/{issue_id}/fields/{field_name}"
        data = {"name": field_name, "value": {"name": new_state}}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def attach_file(self, issue_id: str, file_path: str):
        """
        Attach a file to an issue.
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
        """
        url = f"{self.base_url}/api/issues/{issue_id}/activities?fields=id,timestamp,author,added,removed"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_workitems(self, project_id: str, limit: int = 20, skip: int = 0):
        """
        List workitems (time tracking entries) in a project, with pagination support.
        """
        url = f"{self.base_url}/api/issues?fields=id,summary,workItems(id,duration,author,date,description)&query=project:{project_id}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def calculate_time_spent(self, issue_id: str):
        """
        Calculate total time spent on an issue by summing its workitems' durations.
        """
        url = f"{self.base_url}/api/issues/{issue_id}/timeTracking/workItems?fields=duration"
        response = requests.get(url, headers=self._headers())
        workitems = self._handle_response(response)
        total = sum(wi.get('duration', 0) for wi in workitems)
        return total

    def list_workitem_types(self, project_id: str):
        """
        List allowed workitem types for a project.
        """
        url = f"{self.base_url}/api/admin/projects/{project_id}/timetrackingsettings/workitemtypes?fields=id,name,localizedName"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def add_spent_time(self, issue_id: str, duration: int, workitem_type_id: str, description: str = ""):
        """
        Add spent time (workitem) to an issue. Duration is in minutes. workitem_type_id is required.
        """
        url = f"{self.base_url}/api/issues/{issue_id}/timeTracking/workItems?fields=id,duration,description,type(id,name)"
        data = {"duration": duration, "description": description, "type": {"id": workitem_type_id}}
        response = requests.post(url, json=data, headers=self._headers())
        return self._handle_response(response)

    def list_projects(self):
        """
        List all projects and their IDs.
        """
        url = f"{self.base_url}/api/admin/projects?fields=id,name,shortName"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def get_issue(self, issue_id: str):
        """
        Get details for a specific issue by ID.
        """
        url = f"{self.base_url}/api/issues/{issue_id}?fields=id,summary,description,project(id,name)"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_users(self, query: str = "", limit: int = 20, skip: int = 0):
        """
        List users and their IDs. Optionally filter by query string.
        """
        url = f"{self.base_url}/api/users?fields=id,login,name,email&query={query}&$skip={skip}&$top={limit}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def list_custom_fields(self, project_id: str):
        """
        List custom fields for a project and their IDs.
        """
        url = f"{self.base_url}/api/admin/projects/{project_id}/customfields?fields=id,name,fieldType(id,valueType)"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def authenticate(self):
        """
        Placeholder for authentication logic.
        """
        pass
