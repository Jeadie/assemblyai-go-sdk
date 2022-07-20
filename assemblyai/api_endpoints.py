"""AssemblyAI API endpoints"""

from typing import List, TYPE_CHECKING

from assemblyai.model import StreamPayload, Transcript, Upload, UtteredWord


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

    def create(self, transcript: Transcript) -> Transcript:
        return transcript

    def get(self, transcript_id: str) -> Transcript:
        return Transcript()

    def sentences(self, transcript_id: str) -> List[UtteredWord]:
        return []

    def paragraphs(self, transcript_id: str) -> List[UtteredWord]:
        return []

    def all(self) -> List[Transcript]:
        return []

    def delete(self, transcript_id: str):
        return 

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