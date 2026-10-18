import requests
from requests import Response


class ApiSession:
    def __init__(self, base_url: str, user_id: str):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers["x-user-id"] = user_id

    def request(
        self, method: str, url: str, validate_response: bool = True, **kwargs
    ) -> Response:
        request_url = f"{self.base_url}/{url.lstrip('/')}"
        response = self.session.request(method, url=request_url, **kwargs)
        if validate_response:
            response.raise_for_status()
        return response
