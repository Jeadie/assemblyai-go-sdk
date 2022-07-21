"""AssemblyAI API endpoints"""

import json
from typing import Any, Optional, List, TYPE_CHECKING

from datetime import date

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
        """ Create a new Transcript object.
        
        Results in AsssemblyAI running core transcription (and possibly audio intelligence) on the audio referenced.
        Note: Maximum file size for audio is 10 hours.
        
        *[Reference](https://www.assemblyai.com/docs/reference#create-a-transcript)*
        """
        response =  self.parent.request("{TranscriptEndpoint.PREFIX}", "POST", body=transcript.to_json())
        return Transcript.schema().loads(response)

    def get(self, transcript_id: str) -> Transcript:
        """ Retrieve a specific transcript
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-a-transcript)*
        """
        response =  self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}", "GET")
        return Transcript.schema().loads(response)

    def sentences(self, transcript_id: str) -> List[UtteredWord]:
        """ Retrieve the sentences of a transcript.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-sentences-of-a-transcript)*
        """
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}/sentences", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def paragraphs(self, transcript_id: str) -> List[UtteredWord]:
        """ Retrieve the paragraphs of a transcript.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-paragraphs-of-a-transcript)*
        """
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}/paragraphs", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def delete(self, transcript_id: str):
        """ Delete a specific transcript.

        Note: The record of the transcript will exist and remain queryable, however, all fields 
        containing sensitive data (like text transcriptions) will be permanently deleted.
        
        *[Reference](https://www.assemblyai.com/docs/reference#delete-a-transcript)*
        """
        self.parent.request(f"{TranscriptEndpoint.PREFIX}/{transcript_id}", "DELETE")

    def all(self, limit: Optional[int] = None, status: Optional[TranscriptStatus] = None, created_on: Optional[date] = None, before_id: Optional[str]=None, after_id: Optional[str]=None, throttled_only: bool = False, first_page_only: bool = True) -> List[Transcript]:
        """Retrieve all transcripts.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-transcripts)*
        """
        response = self.parent.request(f"{TranscriptEndpoint.PREFIX}", "GET", body = {
            "limit": limit,
            "status": status,
            "created_on": created_on.isoformat() if created_on else None,
            "before_id": before_id,
            "after_id": after_id,
            "throttled_only": throttled_only
        })
        result = self._parse_all_response(response)

        next_url = self._all_next_url(response)
        if not next_url or first_page_only:
            return result

        while next_url:
            # Take only url suffix path
            path = self.parent.path_from_full_url(next_url)
            response = self.parent.request(path, "GET")

            result.extend(self._parse_all_response(response))
            next_url = self._all_next_url(response)

        return result


    def _all_next_url(self, response: any) -> Optional[str]:
        """For a response from self.all(), retrieve the url for the next set of paginated results. 
        
        If None, no more results are present.
        """
        resp_json = json.loads(response)
        if not resp_json.get("page_details"):
            return None

        return resp_json["page_details"].get("next_url", None)

    def _parse_all_response(self, response: any) -> List[Transcript]:
        """For a response from self.all(), parse all transcripts from this response."""
        resp_json = json.loads(response)
        if not resp_json.get("transcripts"):
            return []

        # Convert transcripts back to JSON to use dataclass JSON parsing.
        raw_transcripts = json.dumps(resp_json.get("transcripts"))
        return Transcript.schema().loads(raw_transcripts, many=True)

class UploadEndpoint(Endpoint):
    """ API Operations related to the model.Upload object.

        *[Endpoint reference](https://www.assemblyai.com/docs/reference#upload)*
    """

    def upload_bytes(self, content: bytes) -> Upload:
        """
        
        *[Reference](https://www.assemblyai.com/docs/reference#creating-an-upload)*
        """
        pass

    def upload_File(self, filename: str) -> Upload:
        """
        
        *[Reference](https://www.assemblyai.com/docs/reference#creating-an-upload)*
        """
        pass

class StreamEndpoint(Endpoint):
    """ API Operations related to the model.Stream object.

        *[Endpoint reference](https://www.assemblyai.com/docs/reference#stream)*
    """
    def stream_raw(self, base64_raw_audio: str, format_text: bool = False, punctuate: bool = False) -> StreamPayload:
        """
        
        *[Reference](https://www.assemblyai.com/docs/reference#stream)*
        """
        pass