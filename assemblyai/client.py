import httpx

from assemblyai.api_endpoints import StreamEndpoint, TranscriptEndpoint, UploadEndpoint

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

        self.transcript = TranscriptEndpoint(self)
        self.upload = UploadEndpoint(self)
        self.stream = StreamEndpoint(self)
        