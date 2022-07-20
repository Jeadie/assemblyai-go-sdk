from dataclasses import dataclass
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

@dataclass
class DetectedEntity:
    entityType: EntityType
    text: str
    start: int
    end: int

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

@dataclass
class UtteredWord:
    start: int
    end: int
    text: str
    confidence: float
    speaker: Optional[str]

@dataclass
class Utterance:
    start: int
    end: int
    text: str
    confidence: float
    speaker: Optional[str]
    words: List[UtteredWord]

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

@dataclass
class CustomSpelling:
    """

    [Reference](https://www.assemblyai.com/docs/core-transcription#custom-spelling)
    """
    from_: List[str]
    to: str

@dataclass
class ContentSafetyLabel:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#content-moderation # Interpreting Content Safety Detection Results
    status: str # "success" | "unavailable"

@dataclass
class IABCategoryResult:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#topic-detection-iab-classification 
    status: str # "success" | "unavailable"

@dataclass
class AutoHighlightResult:
    # TODO: https://www.assemblyai.com/docs/audio-intelligence#detect-important-phrases-and-words
    status: str # "success" | "unavailable"

@dataclass
class Transcript:
    """ Transcript object.
    
    *[Model Reference](https://www.assemblyai.com/docs/reference#transcript)*
    """
    id: str
    status: Optional[TranscriptStatus]
    audio_url: Optional[str]
    text: Optional[str]
    confidence: Optional[float]
    audio_duration: Optional[float]
    punctuate: bool
    format_text: bool
    dual_channel: bool
    webhook_url: Optional[str]
    webhook_status_code: Optional[str]
    audio_start_from: int
    audio_end_at: int
    word_boost: List[str]
    boost_param: Optional[BoostType]
    filter_profanity: bool
    redact_pii: bool
    redact_pii_audio: bool
    redact_pii_sub: Optional[RedactPiiSub]
    speaker_labels: bool
    content_safety: bool
    iab_categories: bool
    disfluencies: bool
    sentiment_analysis: bool
    auto_chapters: bool
    entity_detection: bool
    words: List[UtteredWord]
    utterances: List[Utterance]
    auto_highlights_result: List[AutoHighlightResult]
    redact_pii_policies: List[EntityType]
    chapters: List[Chapter]
    sentiment_analysis_results: List[SentimentAnalysisResult]
    entities: List[DetectedEntity]
    content_safety_labels: List[ContentSafetyLabel]
    iab_categories_result: List[IABCategoryResult]
    custom_spelling: List[CustomSpelling]

    language_code: SupportedLanguageCode = SupportedLanguageCode.english_american

@dataclass
class Upload:
    """ Upload object.
    
    *[Model Reference](https://www.assemblyai.com/docs/reference#upload)*
    """
    upload_url: str