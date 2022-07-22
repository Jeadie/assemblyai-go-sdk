from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional, List

class TranscriptStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    error = "error"

class BoostType(str, Enum):
    low = "low"
    default = "default"
    high = "high"

class SupportedLanguageCode(str, Enum):
    english_global = "en"
    english_australia = "en_au"
    english_britain = "en_uk"
    english_american = "en_us"
    spanish = "es"
    french = "fr"
    italian = "it"
    german = "de"
    portugese = "pt"
    dutch = "nl"
    hindi = "hi"
    japanese = "jp"

class Sentiment(str, Enum):
    positive = "POSITIVE"
    negative = "NEGATIVE"
    neutral = "NEUTRAL"

class RedactPiiSub(str, Enum):
    entity_name = "entity_name"
    hash = "hash"

class EntityType(str, Enum):
    blood_type = "blood_type"
    credit_card_cvv = "credit_card_cvv"
    credit_card_expiration = "credit_card_expiration"
    credit_card_number = "credit_card_number"
    date = "date"
    date_of_birth = "date_of_birth"
    drug = "drug"
    event = "event"
    email_address = "email_address"
    injury = "injury"
    language = "language"
    location = "location"
    medical_condition = "medical_condition"
    medical_process = "medical_process"
    money_amount = "money_amount"
    nationality = "nationality"
    occupation = "occupation"
    organization = "organization"
    person_age = "person_age"
    person_name = "person_name"
    phone_number = "phone_number"
    political_affiliation = "political_affiliation"
    religion = "religion"
    us_social_security_number = "us_social_security_number"
    drivers_license = "drivers_license"
    banking_information = "banking_information"

@dataclass_json
@dataclass
class DetectedEntity:
    entityType: EntityType
    text: str
    start: int
    end: int

@dataclass_json
@dataclass
class SentimentAnalysisResult:
    """
    
    [Reference](https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis)
    """
    text: str
    start: int
    end: int
    sentiment: Sentiment
    speaker: Optional[str]

@dataclass_json
@dataclass
class UtteredWord:
    start: int
    end: int
    text: str
    confidence: float
    speaker: Optional[str]

@dataclass_json
@dataclass
class Utterance:
    start: int
    end: int
    text: str
    confidence: float
    # speaker: Optional[str]
    words: List[UtteredWord] = field(default_factory=list)
    # field(default_factory=list)

@dataclass_json
@dataclass
class Chapter:
    """
    
    [Reference](https://www.assemblyai.com/docs/audio-intelligence#auto-chapters-summarization)
    """
    start: int
    end: int
    summary: str
    gist: str
    headline: str

@dataclass_json
@dataclass
class CustomSpelling:
    """

    [Reference](https://www.assemblyai.com/docs/core-transcription#custom-spelling)
    """
    # from_: List[str]
    to: str

@dataclass_json
@dataclass
class ContentSafetyLabel:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#content-moderation # Interpreting Content Safety Detection Results
    status: str # "success" | "unavailable"

@dataclass_json
@dataclass
class IABCategoryResult:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#topic-detection-iab-classification 
    status: str # "success" | "unavailable"

@dataclass_json
@dataclass
class AutoHighlightResult:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#detect-important-phrases-and-words
    status: str # "success" | "unavailable"

@dataclass_json
@dataclass
class Transcript:
    """ Transcript object.
    
    *[Model Reference](https://www.assemblyai.com/docs/reference#transcript)*
    """
    id: Optional[str] = None
    status: Optional[TranscriptStatus] = None
    audio_url: Optional[str] = None
    text: Optional[str] = None
    confidence: Optional[float] = None
    audio_duration: Optional[float] = None
    punctuate: bool = False
    format_text: bool = False
    dual_channel: Optional[bool] = False
    webhook_url: Optional[str] = None
    webhook_status_code: Optional[str] = None
    audio_start_from: Optional[int] = None
    audio_end_at: Optional[int] = None
    word_boost: List[str] = field(default_factory=list)
    boost_param: Optional[BoostType] = None
    filter_profanity: bool = False
    redact_pii: bool = False
    redact_pii_audio: bool = False
    redact_pii_sub: Optional[RedactPiiSub] = None
    speaker_labels: bool = False
    content_safety: bool = False
    iab_categories: bool = False
    disfluencies: bool = False
    sentiment_analysis: bool = False
    auto_chapters: bool = False
    entity_detection: bool = False
    language_code: SupportedLanguageCode = SupportedLanguageCode.english_american
    words: List[UtteredWord] = field(default_factory=list)
    utterances: List[Utterance] = field(default_factory=list)

    ## TODO: Add these back in. Currently these fields are correctly documented by AssemblyAI.
    # auto_highlights_result: Optional[List[AutoHighlightResult]] = field(default_factory=list)
    # redact_pii_policies: Optional[List[EntityType]] = field(default_factory=list)
    # chapters: List[Chapter] = field(default_factory=list)
    # sentiment_analysis_results: List[SentimentAnalysisResult] = field(default_factory=list)
    # entities: List[DetectedEntity] = field(default_factory=list)
    # content_safety_labels: List[ContentSafetyLabel] = field(default_factory=list)
    # iab_categories_result: List[IABCategoryResult] = field(default_factory=list)
    # custom_spelling: List[CustomSpelling] = field(default_factory=list)


    # Fields that are not present in the Transcript object document, but are returned from API methods.
    resource_url : Optional[str] = None

    ## UTC datetime strings
    completed: Optional[str] = None
    created: Optional[str] = None
    
    def is_audio_intelligence_ready(self):
        """Returns True iff audio intelligence from AssemblyAI is ready to be used."""
        return self.status == TranscriptStatus.completed

@dataclass_json
@dataclass
class Upload:
    """ Upload object.
    
    *[Model Reference](https://www.assemblyai.com/docs/reference#upload)*
    """
    upload_url: str

@dataclass_json
@dataclass
class StreamPayload:
    """ Payload from stream operations.

    *[Reference](https://www.assemblyai.com/docs/reference#stream)*
    """
    id: str
    status: TranscriptStatus
    confidence: float
    text: str
    words: List[UtteredWord] = field(default_factory=list)