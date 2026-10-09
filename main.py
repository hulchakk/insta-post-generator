import argparse
import base64
import json
import mimetypes
import os
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMPLATE_DIR = Path(__file__).parent / "template"


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    PIXABAY_API_KEY: str = ""
    OLLAMA_URL: str = "http://localhost:11434/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


PROMPT = """You are a social media editor who makes Instagram event announcements for students and teenagers. \
From the event details, the author's idea and photos, build a post.

Caption:
- First line is a hook under 110 characters, visible before "more": what the event is and why go. No clickbait.
- Then 2-4 short paragraphs of 1-2 sentences, lively plain language, 1-3 fitting emoji, no corporate tone.
- End with one call to action: save the post, send it to a friend, ask in the comments.
- hashtags: 4-5 tags without spaces and without #, from narrow (city, event topic) to broad. No junk like fyp or love.

Slides ({layout}). One idea per slide, readable in 3 seconds:
- cover (first): title is a hook of up to 6 words; text is date and place in up to 5 words, or empty.
- info: title up to 5 words; text up to 20 words and/or 2-4 items of up to 6 words: why go, what happens, who it is for.
- facts (right before final): title (like "Details"), items are practical details like "When: October 12, 6 PM", \
"Where: ...", "Price: ...", "Registration: ...". Only what is in the data.
- final (last): title is a call to action (up to 5 words), text is what to do next, items are 0-3 short chips.
Unused slide fields are an empty string or an empty list.

Rules:
- Only facts from the data. Never invent prices, times, addresses or guests; leave out what is missing and \
say so in notes.
- Write in the language of the event details, unless the author asks for another.
- photo is the index (from 0) of the author's photo that fits the slide, or null. One photo on at most two slides.
- photo_query is 2-3 English words for a stock photo ("friends party", "concert crowd"), only when the author \
gave no photos; otherwise an empty string.
- notes are 3-6 tips for the author: best time to post, what to tag (location, organizers, collab), what to add \
to stories or the first comment, what to clarify before publishing.
"""


class Slide(BaseModel):
    kind: Literal["cover", "info", "facts", "final"]
    title: str
    text: str
    items: list[str]
    photo: int | None
    photo_query: str


class Post(BaseModel):
    caption: str
    hashtags: list[str]
    slides: list[Slide]
    notes: list[str]


def image_part(path: Path) -> dict:
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode()
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}", "detail": "low"}}


def generate_post(event: str, idea: str, photos: list[Path], story: bool, client: OpenAI, model: str) -> Post:
    layout = "story, 3-5 slides" if story else "carousel, 4-7 slides"
    text = f"Event details:\n{event}\n\nAuthor's idea: {idea or 'none'}\n\nAuthor's photos: {len(photos)} (attached in order, from 0)"
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": PROMPT.format(layout=layout)},
            {"role": "user", "content": [{"type": "text", "text": text}, *map(image_part, photos)]},
        ],
        response_format=Post,
    )
    return response.choices[0].message.parsed


def download_stock_photo(query: str, path: Path, api_key: str) -> bool:
    def fetch(url: str) -> bytes:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
            return response.read()

    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": api_key, "q": query, "image_type": "photo", "orientation": "horizontal", "per_page": 3}
    )
    try:
        hits = json.loads(fetch(url))["hits"]
        if hits:
            path.write_bytes(fetch(hits[0]["largeImageURL"]))
    except OSError as error:
        print(f"Pixabay \"{query}\": {error}")
        return False
    return bool(hits)


def photo_names(slides: list[Slide], user_names: list[str], work: Path, pixabay_key: str) -> list[str | None]:
    names: list[str | None] = []
    for i, slide in enumerate(slides):
        if user_names:
            names.append(user_names[slide.photo] if slide.photo is not None and 0 <= slide.photo < len(user_names) else None)
        elif slide.photo_query and pixabay_key and download_stock_photo(slide.photo_query, work / f"stock_{i}.jpg", pixabay_key):
            names.append(f"stock_{i}.jpg")
        else:
            names.append(None)
    return names


def to_markdown(post: Post, story: bool, photos: list[str | None]) -> str:
    tags = " ".join(f"#{tag.lstrip('#')}" for tag in post.hashtags)
    slides = "\n".join(
        f"{i}. {slide.kind}: {slide.title}" + ("" if photos[i - 1] else " (no photo)") for i, slide in enumerate(post.slides, 1)
    )
    notes = "\n".join(f"- {note}" for note in post.notes)
    kind = "story" if story else "carousel"
    return (
        f"# Instagram caption\n\n{post.caption}\n\n{tags}\n\n"
        f"# For the author\n\nFormat: {kind}, {len(post.slides)} slides (1.png … {len(post.slides)}.png)\n\n{notes}\n\n"
        f"# Slides\n\n{slides}\n"
    )


def render(work: Path, out: Path, post: Post, photos: list[str | None], story: bool) -> None:
    props = work / "post.json"
    slides = [slide.model_dump(include={"kind", "title", "text", "items"}) | {"photo": photo} for slide, photo in zip(post.slides, photos)]
    props.write_text(json.dumps({"format": "story" if story else "carousel", "slides": slides}, ensure_ascii=False), encoding="utf-8")
    frames = work / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    subprocess.run(
        ["npx", "remotion", "render", "src/index.tsx", "Post", str(frames), "--sequence", "--image-format=png",
         f"--props={props}", f"--public-dir={work}", "--overwrite"],
        cwd=TEMPLATE_DIR,
        check=True,
    )
    for old in out.glob("[0-9]*.png"):
        old.unlink()
    for i, frame in enumerate(sorted(frames.glob("*.png"), key=lambda path: int(path.stem.split("-")[-1])), 1):
        frame.replace(out / f"{i}.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Instagram event post: instagram.md and slides 1.png, 2.png…")
    parser.add_argument("event", help="event details: text or a path to a text file")
    parser.add_argument("--idea", default="", help="idea or wishes for the post")
    parser.add_argument("--photo", nargs="*", default=[], type=Path, help="event photos")
    parser.add_argument("--story", action="store_true", help="story 1080x1920 instead of carousel 1080x1350")
    parser.add_argument("--ollama", metavar="MODEL", help="use a local Ollama model (vision-capable for --photo), e.g. gemma3")
    parser.add_argument("-o", "--output", type=Path, default=Path("output"))
    args = parser.parse_args()

    settings = Settings()
    event = Path(args.event).read_text(encoding="utf-8") if os.path.isfile(args.event) else args.event
    if args.ollama:
        client, model = OpenAI(base_url=settings.OLLAMA_URL, api_key="ollama", timeout=900), args.ollama
    else:
        client, model = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=120), settings.OPENAI_MODEL
    post = generate_post(event, args.idea, args.photo, args.story, client, model)

    work = args.output / ".work"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    user_names = []
    for i, photo in enumerate(args.photo):
        user_names.append(f"photo_{i}{photo.suffix}")
        shutil.copyfile(photo, work / user_names[-1])
    photos = photo_names(post.slides, user_names, work, settings.PIXABAY_API_KEY)

    (args.output / "instagram.md").write_text(to_markdown(post, args.story, photos), encoding="utf-8")
    render(work.resolve(), args.output, post, photos, args.story)
    print(f"Done: {args.output}/instagram.md and {len(post.slides)} slides")


if __name__ == "__main__":
    main()
