# Instagram Post Generator

An automatic content generator that automates making Instagram event announcements: event details in, caption and ready-to-post slides out.

This is a learning project: a small end-to-end example of combining an LLM with a React rendering pipeline.

## How it works

1. You give it event details, an optional idea for the post and optional photos.
2. An LLM (gpt-4o) looks at the photos and writes the caption, hashtags and slide texts following reach best practices. Without photos, stock ones come from Pixabay.
3. Remotion renders the slides from light React templates (cover, info, facts, final) to PNG, as a 4:5 carousel or a 9:16 story.
4. The result lands in `output/`: `instagram.md` (caption to paste, notes for the author) and `1.png`, `2.png`… in slide order.

## Tech Stack

| What | Why |
|---|---|
| Python 3.12, uv | one script, three dependencies |
| OpenAI `gpt-4o` or local Ollama + Pydantic | structured output straight into models, photos as vision input; Ollama speaks the same API |
| Remotion (React + TypeScript) | slides are plain React components rendered to PNG |
| Pixabay | free stock photos |

## Getting Started

Needs Python 3.12+, [uv](https://docs.astral.sh/uv/) and Node.js 22+.

```bash
cp .env.example .env
uv sync && (cd template && npm install)
uv run python main.py event.txt --idea "stress the free food" --photo a.jpg b.jpg
uv run python main.py "Board game night, Friday 6 PM, free entry" --story
```

Fill `OPENAI_API_KEY` in `.env`; `PIXABAY_API_KEY` is optional. Options: `--idea` wishes for the post, `--photo` your photos, `--story` story format instead of carousel, `--ollama MODEL` local model instead of OpenAI, `-o` output folder (default `output`).

### Local model (Ollama)

Runs fully offline and free, no OpenAI key needed. Install [Ollama](https://ollama.com), pull a model and pass its name:

```bash
ollama pull gemma3
uv run python main.py event.txt --ollama gemma3
```

With `--photo` the model must support images (for example `gemma3` or `llama3.2-vision`), otherwise it ignores them. Small models follow the caption rules worse than `gpt-4o`. The server address is `OLLAMA_URL` in `.env` (default `http://localhost:11434/v1`).

## Key Decisions

- One frame of the Remotion composition is one slide, so a single render call produces every PNG.
- LLM output is not trusted: a photo index that does not exist is dropped, and the prompt forbids invented prices, times and addresses.
- Slide design lives only in `template/src/Slide.tsx`; preview it with `cd template && npm run studio`.

## Status

- Works for one event per run; no scheduling or publishing, the author posts by hand.
- Slide text is not checked for overflow beyond the length limits in the prompt.
