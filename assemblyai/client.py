from typing import Any, Dict, Optional

import httpx

from assemblyai.api_endpoints import StreamEndpoint, TranscriptEndpoint, UploadEndpoint

BASE_URL_V2 = "https://api.assemblyai.com/v2/"
JSON_CONTENT_TYPE = "application/json"


class Client:
    """Basic Client for AssemblyAI APIs"""

    def __init__(self, api_key: str) -> None:
        self.client = httpx.Client()

        self.client.headers =  httpx.Headers({
            'authorization': api_key,
        })
        self.base_url = BASE_URL_V2

        self.transcript = TranscriptEndpoint(self)
        self.upload = UploadEndpoint(self)
        self.stream = StreamEndpoint(self)

    def _parse_response(self, response: httpx.Response) -> httpx.Response:
        """Parses the response from a client request. Throws a httpx.HTTPStatusError if an error status code is returned."""
        response.raise_for_status()
        return response

    def request(self, path: str, method: str, query: Optional[Dict[Any, Any]] = None, data: Optional[Dict[Any, Any]] = None, body: Optional[Dict[Any, Any]] = None, headers: Optional[Dict[str, str]]=None) -> httpx.Response:
        """ Sends a JSON-encoded, HTTP request with required authorization to AssemblyAI api.

        Throws:
            httpx.HTTPStatusError: If the response was unsuccessful.
            httpx.TimeoutException: If a timeout occured on the request.
        """
        request = self.client.build_request(method, f"{self.base_url}{path}", params=query, json=body, headers=headers, data=data)
        response = self.client.send(request)
        return self._parse_response(response)

    def path_from_full_url(self, full_url: str) -> str:
        start_index = full_url.find(self.base_url)
        if start_index == -1:
            raise ValueError(f"full_url: {full_url} has unexpected based url. Expected {self.base_url}.")
        return full_url[len(self.base_url):]