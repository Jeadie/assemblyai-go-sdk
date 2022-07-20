"""AssemblyAI API endpoints"""

from typing import Optional, List, TYPE_CHECKING

from datetime import date
from venv import create

from assemblyai.model import StreamPayload, Transcript, TranscriptStatus, Upload, UtteredWord


if TYPE_CHECKING:
    from assemblyai.client import Client


class Endpoint:
    """Abstract Endpoint entity that represents a set of related API endpoints."""
    def __init__(self, parent: "Client") -> None:
        self.parent = parent


class TranscriptEndpoint(Endpoint):
    """ API Operations related to the model.Transcript object.
    
        *[Endpoint reference](https://www.assemblyai.com/docs/reference#transcript)*
    """
    PREFIX="transcript"

    def create(self, transcript: Transcript) -> Transcript:
        return transcript

    def get(self, transcript_id: str) -> Transcript:
        response =  self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}", "GET")
        return Transcript.schema().loads(response)

    def sentences(self, transcript_id: str) -> List[UtteredWord]:
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}/sentences", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def paragraphs(self, transcript_id: str) -> List[UtteredWord]:
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}/paragraphs", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def all(self, limit: Optional[int] = None, status: Optional[TranscriptStatus] = None, created_on: Optional[date] = None, before_id: Optional[str]=None, after_id: Optional[str]=None, throttled_only: bool = False) -> List[Transcript]:
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}", "GET", body = {
            "limit": limit,
            "status": status,
            "created_on": created_on.isoformat() if created_on else None,
            "before_id": before_id,
            "after_id": after_id,
            "throttled_only": throttled_only
        })
        return self._parse_all_response(response)

    def _parse_all_response(self, response: any) -> List[Transcript]:
        return []

    def delete(self, transcript_id: str):
        self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}", "DELETE")

class UploadEndpoint(Endpoint):
    """ API Operations related to the model.Upload object.

        *[Endpoint reference](https://www.assemblyai.com/docs/reference#upload)*
    """

    def upload_bytes(self, content: bytes) -> Upload:
        pass

    def upload_File(self, filename: str) -> Upload:
        pass

class StreamEndpoint(Endpoint):
    """ API Operations related to the model.Stream object.

        *[Endpoint reference](https://www.assemblyai.com/docs/reference#stream)*
    """
    def stream_raw(self, base64_raw_audio: str, format_text: bool = False, punctuate: bool = False) -> StreamPayload:
        pass