# Personal LLM - a desktop ChatGPT clone that runs 100% local off of the cloud

## Author
[Kay Ashaolu](https://www.linkedin.com/in/kayashaolu/)

## Description
Unlock the power of Language Models in your own hands! Personal LLM is a revolutionary desktop application that brings the capabilities of Large Language Models (LLMs) to your very own computer. With Personal LLM, you can now harness the intelligence and creativity of AI-powered language processing, without relying on internet connectivity or costly subscriptions. Simply download, install, and start leveraging the limitless potential of LLMs for free, right from your desktop

## Technologies Used
- HTML
- CSS
- JavaScript
- Python
- Ollama
- LLM
- ORM [Peewee](https://docs.peewee-orm.com/en/latest/)
- RDBMS [Sqlite3](https://sqlite.org/)
- [Python-Eel](https://github.com/python-eel/Eel)

## Demo
[![Personal-LLM Demo Video](http://img.youtube.com/vi/BwRgVGhxm70/0.jpg)](http://www.youtube.com/watch?v=BwRgVGhxm70 "Personal-LLM Demo Video")

## Technical System Design
[![Personal-LLM System Design Video](http://img.youtube.com/vi/MgdypIh9wrA/0.jpg)](http://www.youtube.com/watch?v=MgdypIh9wrA "Personal-LLM System Design Video")

## Setup Instructions
1. Please download and install the following dependencies
  * [Python 3](https://www.python.org/downloads/) (3.11 or newer)
  * [Node.js](https://nodejs.org/) (22 or newer)
  * [Google Chrome](https://www.google.com/chrome/)
  * [Ollama](https://ollama.com/) — optional to pre-install: `npm run start` installs it if it's missing (Linux via the official script, macOS via Homebrew) and starts it if it isn't running.
    * Ollama is a LLM model backend that lets you download and access LLMs locally and use it in your applications.
2. Clone this repository
3. Run `npm run start` to run the project (`npm run setup` and `npm run build` are the individual steps)

## Configuration
Optional environment variables:
- `PERSONAL_LLM_MODEL` — Ollama model to pull and chat with (default `gemma3:270m`)
- `PERSONAL_LLM_DB` — path to the SQLite file (default `storage/app/data.db` under the repo root; the folder is created if missing)
    * The default model is [Gemma 3 270M](https://ollama.com/library/gemma3) from Google, about 290 MB; the first run downloads it. Set `PERSONAL_LLM_MODEL` to use a different Ollama model.

## Running tests
Run `npm run setup` first (once per clone; it installs pytest into `.venv` and vitest into `node_modules`). Backend and frontend tests are separate commands:

```bash
npm run test:backend    # Python: pytest over backend/tests/
npm run test:frontend   # React:  vitest over frontend/tests/
npm test                # both, one after the other; fails if either failed
```

Each prints how many tests passed and failed, plus the error for every failure.

The backend suite includes a few tests marked `ollama` that talk to the real Ollama server on `localhost:11434` and send one short prompt to the configured model (`PERSONAL_LLM_MODEL`, default `gemma3:270m`). They fail with a message telling you what to do if Ollama isn't running or the model isn't downloaded. Everything else runs with the LLM stubbed out and needs no Ollama, browser, or network. To skip the Ollama tests: `./.venv/bin/python -m pytest -m "not ollama"`.
