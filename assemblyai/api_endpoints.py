"""AssemblyAI API endpoints"""

import json
from typing import Any, Dict, Optional, List, TYPE_CHECKING

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
        response =  self._handle_request("", "POST", body=transcript.to_json())
        return Transcript.schema().loads(response)

    def get(self, transcript_id: str) -> Transcript:
        """ Retrieve a specific transcript
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-a-transcript)*
        """
        response =  self._handle_request(transcript_id, "GET")
        return Transcript.schema().loads(response)

    def sentences(self, transcript_id: str) -> List[UtteredWord]:
        """ Retrieve the sentences of a transcript.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-sentences-of-a-transcript)*
        """
        response = self._handle_request(f"{transcript_id}/sentences", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def paragraphs(self, transcript_id: str) -> List[UtteredWord]:
        """ Retrieve the paragraphs of a transcript.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-paragraphs-of-a-transcript)*
        """
        response = self._handle_request(f"{transcript_id}/paragraphs", "GET")
        return UtteredWord.schema().loads(response, many=True)

    def delete(self, transcript_id: str):
        """ Delete a specific transcript.

        Note: The record of the transcript will exist and remain queryable, however, all fields 
        containing sensitive data (like text transcriptions) will be permanently deleted.
        
        *[Reference](https://www.assemblyai.com/docs/reference#delete-a-transcript)*
        """
        self._handle_request(transcript_id, "DELETE")

    def all(self, limit: Optional[int] = None, status: Optional[TranscriptStatus] = None, created_on: Optional[date] = None, before_id: Optional[str]=None, after_id: Optional[str]=None, throttled_only: bool = False, first_page_only: bool = True) -> List[Transcript]:
        """Retrieve all transcripts.
        
        *[Reference](https://www.assemblyai.com/docs/reference#get-all-transcripts)*
        """
        response = self._handle_request("", "GET", body = {
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
            response = self._handle_request(path, "GET")

            result.extend(self._parse_all_response(response))
            next_url = self._all_next_url(response)

        return result

    def _handle_request(self, operation: str, method: str, query: Optional[Dict[Any, Any]] = None, body: Optional[Dict[Any, Any]] = None):
        """Handles sending a request to the transcript endpoints."""
        return self.parent.request(f"{TranscriptEndpoint.PREFIX}/{operation}", method, body = body, query=query, headers={"content-type": 'application/json'})

    def _clean_body(self, body: Optional[Dict[Any, Any]]) -> Optional[Dict[Any, Any]]:
        """Cleans a json body of pythonic values and unnecessary keys."""
        if not body:
            return body

        # Remove key-value with null values
        body_items = filter(lambda x: x[1] is not None, body.items())

        return dict(body_items)

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
    PREFIX="upload"

    def upload_bytes(self, content: bytes) -> Upload:
        """Upload bytes of raw audio to AssemblyAI servers.
        
        Note: does not run transcription or any audio intelligence.
        
        *[Reference](https://www.assemblyai.com/docs/reference#creating-an-upload)*
        """
        response = self.parent.request(UploadEndpoint.PREFIX, "POST", data=content, headers={"Transfer-Encoding": "chunked"})
        return Upload.schema().loads(response)

    def upload_file(self, filename: str) -> Upload:
        """Upload file from raw audio to AssemblyAI servers.
        
        Note: does not run transcription or any audio intelligence.
        
        *[Reference](https://www.assemblyai.com/docs/reference#creating-an-upload)*
        """
        return self.upload_bytes(self._read_binary_file(filename))

    def _read_binary_file(self, filename, chunk_size=5242880):
        """Reads data from a binary file in chunks."""
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


class StreamEndpoint(Endpoint):
    """ API Operations related to the model.Stream object.

        *[Endpoint reference](https://www.assemblyai.com/docs/reference#stream)*
    """
    def stream_raw(self, base64_raw_audio: str, format_text: bool = False, punctuate: bool = False) -> StreamPayload:
        """
        
        *[Reference](https://www.assemblyai.com/docs/reference#stream)*
        """
        pass