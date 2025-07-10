import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from vaiz import __version__

@dataclass
class ErrorMeta:
    description: Optional[str] = None
    token: Optional[str] = None
    # Add other meta fields as needed

@dataclass
class APIError:
    code: str
    fields: List[str]
    original_type: str
    meta: Optional[ErrorMeta] = None

class VaizSDKError(Exception):
    """Base SDK error."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        self.api_error = api_error
        error_details = []
        
        if api_error:
            error_details.append(f"Error code: {api_error.code}")
            error_details.append(f"Original type: {api_error.original_type}")
            if api_error.fields:
                field_strs = [f.get("name", str(f)) if isinstance(f, dict) else str(f) for f in api_error.fields]
                error_details.append(f"Affected fields: {', '.join(field_strs)}")
            if api_error.meta and api_error.meta.description:
                error_details.append(f"Details: {api_error.meta.description}")
        
        if error_details:
            formatted_message = f"{message}\n\n" + "\n".join(error_details)
        else:
            formatted_message = message
            
        super().__init__(formatted_message)

class VaizAuthError(VaizSDKError):
    """Authentication error."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        super().__init__(f"Authentication error: {message}", api_error)

class VaizValidationError(VaizSDKError):
    """Data validation error."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        super().__init__(f"Validation error: {message}", api_error)

class VaizNotFoundError(VaizSDKError):
    """Resource not found."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        super().__init__(f"Resource not found: {message}", api_error)

class VaizPermissionError(VaizSDKError):
    """Permission error."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        super().__init__(f"Permission denied: {message}", api_error)

class VaizRateLimitError(VaizSDKError):
    """Request rate limit exceeded."""
    def __init__(self, message: str, api_error: Optional[APIError] = None):
        super().__init__(f"Rate limit exceeded: {message}", api_error)

class VaizHTTPError(VaizSDKError):
    def __init__(self, message, status_code=None, url=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.response_text = response_text

class BaseAPIClient:
    def __init__(self, api_key: str, space_id: str, base_url: str = "https://api.vaiz.com/v4", verify_ssl: bool = True, verbose: bool = False):
        """
        Initialize the API client.
        
        Args:
            api_key: Your Vaiz API key
            space_id: Your Vaiz space ID
            base_url: Base URL for the API (defaults to production)
            verify_ssl: Whether to verify SSL certificates (defaults to True for security)
            verbose: Whether to enable debug output
        """
        self.api_key = api_key
        self.space_id = space_id
        self.base_url = base_url
        self.verify_ssl = verify_ssl
        self.verbose = verbose
        self.app_version = f"python-sdk-{__version__}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "current-space-id": self.space_id,
            "app-version": self.app_version,
        })

    def _parse_error(self, response_data: Dict[str, Any]) -> APIError:
        """Parse error from API response."""
        error_data = response_data.get("error", {})
        meta_data = error_data.get("meta", {})
        
        return APIError(
            code=error_data.get("code", "UnknownError"),
            fields=error_data.get("fields", []),
            original_type=error_data.get("originalType", ""),
            meta=ErrorMeta(
                description=meta_data.get("description"),
                token=meta_data.get("token")
            )
        )

    def _handle_api_error(self, api_error: APIError) -> None:
        """Handle API error and raise appropriate exception."""
        error_map = {
            "JwtIncorrect": VaizAuthError,
            "JwtExpired": VaizAuthError,
            "ValidationError": VaizValidationError,
            "NotFound": VaizNotFoundError,
            "PermissionDenied": VaizPermissionError,
            "RateLimitExceeded": VaizRateLimitError,
        }
        
        error_class = error_map.get(api_error.code, VaizSDKError)
        message = api_error.meta.description if api_error.meta and api_error.meta.description else api_error.code
        raise error_class(message, api_error)

    def _make_request(self, endpoint: str, method: str = "POST", json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        if self.verbose:
            print(f"Request payload: {json_data}")  # Debug print
        
        try:
            response = self.session.request(method, url, json=json_data, verify=self.verify_ssl)
            response_data = response.json()
            
            if self.verbose:
                print(f"Response data: {response_data}")  # Debug print

            # Check for error in response
            if "error" in response_data:
                api_error = self._parse_error(response_data)
                self._handle_api_error(api_error)
            
            return response_data

        except requests.exceptions.RequestException as e:
            raise VaizSDKError(f"Network error for {url}: {e}") from e