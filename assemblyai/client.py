from typing import Any, Dict, Optional

import httpx

from assemblyai.api_endpoints import StreamEndpoint, TranscriptEndpoint, UploadEndpoint

BASE_URL_V2 = "https://api.assemblyai.com/v2/"

class Client:
    """Basic Client for AssemblyAI APIs"""

    client: httpx.Client

    def __init__(self, api_key: str) -> None:
        if client is None:
            client = httpx.Client()

        client.Headers =  httpx.Headers({
            'authorization': api_key,
            'content-type': 'application/json'
        })
        self.base_url = BASE_URL_V2

        self.transcript = TranscriptEndpoint(self)
        self.upload = UploadEndpoint(self)
        self.stream = StreamEndpoint(self)
        

    def _build_request(self, method: str, path: str, query: Optional[Dict[Any, Any]] = None, body: Optional[Dict[Any, Any]] = None) -> httpx.Request:
        """Build a request object for the client."""
        # TODO: remove null values, and convert Enum -> str.
        return self.client.build_request(
            method, path, params=query, json=body,
        )

    def _parse_response(self, response: httpx.Response) -> Any:
        """Parses the response from a client request. Throws a httpx.HTTPStatusError if an error status code is returned."""
        response.raise_for_status()
        return response.json()

    
    def request(self, path: str, method: str, query: Optional[Dict[Any, Any]] = None, body: Optional[Dict[Any, Any]] = None) -> Any:
        """ Sends a JSON-encoded, HTTP request with required authorization to AssemblyAI api.
        
        Throws:
            httpx.HTTPStatusError: If the response was unsuccessful.
            httpx.TimeoutException: If a timeout occured on the request.
        """
        request = self._build_request(method, f"{self.base_url}{path}", query, body)
        response = self.client.send(request)
        return self._parse_response(response)