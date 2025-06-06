# vaiz/client.py
from typing import Dict, Any
import requests
from vaiz.models import CreateTaskRequest, TaskResponse


class VaizClient:
    def __init__(self, api_key: str, space_id: str, base_url: str = "https://api.vaiz.com/v4"):
        self.api_key = api_key
        self.space_id = space_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "current-space-id": self.space_id,
            "app-version": "1.68.1",
        })

    def create_task(self, task: CreateTaskRequest) -> TaskResponse:
        url = f"{self.base_url}/createTask"
        json_data = task.dict(by_alias=True)
        print(f"Request payload: {json_data}")  # Debug print
        response = self.session.post(url, json=json_data)
        if not response.ok:
            print(f"Error response: {response.text}")  # Debug print
        response.raise_for_status()
        response_data = response.json()
        print(f"Response data: {response_data}")  # Debug print
        return TaskResponse(**response_data)