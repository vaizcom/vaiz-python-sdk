import requests
from typing import Dict, Any

class BaseAPIClient:
    def __init__(self, api_key: str, space_id: str, base_url: str = "https://api.vaiz.com/v4", verify_ssl: bool = True):
        self.api_key = api_key
        self.space_id = space_id
        self.base_url = base_url
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "current-space-id": self.space_id,
            "app-version": "1.68.1",
        })

    def _make_request(self, endpoint: str, method: str = "POST", json_data: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        print(f"Request payload: {json_data}")  # Debug print
        response = self.session.request(method, url, json=json_data, verify=self.verify_ssl)
        if not response.ok:
            print(f"Error response: {response.text}")  # Debug print
        response.raise_for_status()
        response_data = response.json()
        print(f"Response data: {response_data}")  # Debug print
        return response_data 