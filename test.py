from dataclasses import dataclass
import os
from typing import Any, Optional, List
from venv import create

from assemblyai.client import Client as AssemblyClient
from assemblyai.model import Chapter, Transcript, Utterance, UtteredWord

from notion_client import Client as NotionClient

@dataclass
class PodcastEpisode:
    transcript: Optional[Transcript]
    audio_link: str
    title: str
    sentences: List[UtteredWord]

NOTION_DB = "699df7d9390d474bb8b8134dec103232"

def main():
    notion = NotionClient(auth=os.environ["NOTION_KEY"])

    create_notion_page(notion, create_podcast_episode(
        "omhb2gkhws-d497-44db-9db1-224c8e7cfd7c",
        "Living with an Abundance Mindset",
        "https://www.city-lights.church/media/episodes/4nxebg7wcehdf181t4tzedfvcw/4amhd8tt65nbn4r6f40whdjmnr/2022-07-17t10-15-00_41zk7ygfxxnedtbqzh8bb90dcg.mp3"
        )
    )
    # create_notion_page(notion, create_podcast_episode(
    #     "omhbf2zn5x-2126-4acd-87f3-6d5744907739",
    #     "Unpacking the 1,000 assets Report with Mike Mortlock",
    #     "https://mcdn.podbean.com/mf/download/qcvrud/Interview_with_Mike_Mortlock_1_ax8yv.mp3"
    #     )
    # )

def create_podcast_episode(transcript_id: str, episode_name: str, audio: str) -> PodcastEpisode:
    assembly = AssemblyClient(os.environ["ASSEMBLY_KEY"])
    t = assembly.transcript.get(transcript_id)
    s = assembly.transcript.sentences(transcript_id)
    return PodcastEpisode(
        t,
        audio,
        episode_name,
        s
    )


def create_notion_page(notion: NotionClient, episode: PodcastEpisode):
     notion.pages.create(
        parent={
            "type": "database_id",
            "database_id": NOTION_DB
        },
        properties={
            "Name": {
                "title": [
                {
                    "type": "text",
                    "text": {
                        "content": episode.title
                    }
                }
                ]
            },
            "TranscriptId": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": episode.transcript.id
                        }
                    }],
            },
            "Audio": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": episode.audio_link,
                            "link": {
                                "url": episode.audio_link
                            }
                        }
                    }],
            }
        },
        children=[
            SimpleHeading("Audio", 2),
            SimpleEmbed(episode.audio_link)
        ] + [
            SimpleHeading("Chapters", 2),
        ] + [CreateNotionChapter(c, episode.transcript, episode.sentences) for c in episode.transcript.chapters]
    )

def CreateNotionChapter(c: Chapter, transcript: Transcript, sentences: List[UtteredWord]) -> any:
    duration_secs = (c.end - c.start)/1000
    duration_mins = duration_secs // 60
    start_time = format_ms_time(c.start)
    chapter_duration = f"{int(duration_mins)} min {int(duration_secs % 60)} secs"

    # Filter based on start only, because chapters aren't linked exactly to utterances. 
    utterances = list(filter(lambda x: x.start >= c.start and x.start <= c.end, transcript.utterances))
    chapter_sentences = list(filter(lambda x: x.start >= c.start and x.start <= c.end, sentences))
    if len(utterances) == 0:
        utterances = chapter_sentences

    print("chapter", c.start, c.end, transcript.audio_start_from, transcript.audio_end_at)
    x = [print(u.start, u.end) for u in transcript.utterances]
    x = [print(u.start, u.end) for u in utterances]
    print(" --- ")
    summary_paragraphs = create_summary_paragraphs(c.summary)

    return ToggleBlock(SimpleRichText(c.headline, is_bold=True), [
            SimpleQuote(c.gist, color = "gray"),
            SimpleParagraph(start_time, bold_prefix = "Start Time: "),
            SimpleParagraph(chapter_duration, bold_prefix = "Chapter Duration: ")
        ] + summary_paragraphs + [
            ToggleBlock(SimpleRichText("Transcript", is_bold=True), convert_utterances_to_paragraphs(utterances))
        ]
    )

def create_summary_paragraphs(summary: str) -> List[Any]:
    result = []

    y = 2000
    chunks =  [summary[y*i:y*(i+1)] for i in range((len(summary)//y)+1)]
    SimpleParagraph(summary, bold_prefix = "Summary: "),
    result.append(SimpleParagraph(chunks[0], bold_prefix = "Summary: "))

    if len(chunks) > 1:
        result.extend([SimpleParagraph(c) for c in chunks[1:]])
    return result

def convert_utterances_to_paragraphs(utterances: List[Utterance]) -> List[Any]:
    result = []

    for u in utterances:
        # Notion only lets paragraphs <=2000
        y = 2000
        chunks =  [u.text[y*i:y*(i+1)] for i in range((len(u.text)//y)+1)]
        print([len(c) for c in chunks])
        result.append(SimpleParagraph(chunks[0], bold_prefix = f"Speaker {u.speaker}: "))

        # Add extra chunks without speaker prefix.
        if len(chunks) > 1:
            result.extend([SimpleParagraph(c) for c in chunks[1:]])

    return result


def format_ms_time(x: int) -> str:
    mins = x // (60*1000)
    sec = int(x/1000) % 60
    return f"{mins}:{sec:02}"


def ToggleBlock(rich_text: List[Any], children: List[Any], color: str = "default") -> Any:
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": rich_text,
            "color": "default",
            "children": children
        }
    }

def SimpleHeading(text: str, size: int) -> Any:
    return {
        "type": f"heading_{size}",
        f"heading_{size}": {
            "rich_text": [{
            "type": "text",
            "text": {
                "content": text
            }
            }],
            "color": "default"
        }
    }

def SimpleRichText(text: str, is_bold: bool = False) -> List[Any]:
    if is_bold:
        annotations = {"bold": True}
    else:
        annotations = {}

    return [{
        "type": "text",
        "text": {
            "content": text,
        },
        "annotations": annotations
    }]


def SimpleQuote(text: str, bold_prefix: Optional[str] = None, color: str = "default") -> Any:
    rich_text_paragraphs = []
    if bold_prefix:
        rich_text_paragraphs.append({
                "type": "text",
                "text": {
                    "content": bold_prefix,
                },
                # "color": color,
                "annotations": {
                    "bold": True,
                }
            })
    return {
        "type": "quote",
        "object": "block",
        "quote": {
            "rich_text": rich_text_paragraphs + [{
            "type": "text",
            "text": {
                "content": text,
            }
        }],
            "color": color,
            "children":[]
        }
    }

def SimpleEmbed(url: str) -> Any:
    return {
        "type": "embed",
        "embed": {
            "url": url
        }
    }

def SimpleParagraph(text: str, bold_prefix: Optional[str] = None, color: str = "default") -> Any:
    rich_text_paragraphs = []
    if bold_prefix:
        rich_text_paragraphs.append({
                "type": "text",
                "text": {
                    "content": bold_prefix,
                },
                # "color": color,
                "annotations": {
                    "bold": True,
                }
            })
    if len(text) > 2000:
        print(text)

    return {
        "type": "paragraph",
        "object": "block",
        "paragraph": {
            "rich_text": rich_text_paragraphs + [{
            "type": "text",
            "text": {
                "content": text,
            }
        }],
            "color": color,
            # "children":[]
        }
    }

if __name__ == "__main__":
    main()