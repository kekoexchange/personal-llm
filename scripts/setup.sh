#!/usr/bin/env bash
# One-time-ish setup: Python venv + deps, storage dir, and Ollama.
# Safe to rerun; every step is a no-op when already done.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Python environment"
# The app and pytest (requirements-dev.txt) need Python 3.11+; check the
# interpreter that will actually be used (an existing .venv, else python3)
# before installing anything, so an old Python fails here with a plain message
# instead of deep inside pip.
PYTHON=python3
[ -x .venv/bin/python ] && PYTHON=.venv/bin/python
"$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' || {
  echo "Python 3.11 or newer is required, but $PYTHON is $("$PYTHON" --version 2>&1)." >&2
  echo "Install a newer Python (https://www.python.org/downloads/), delete .venv if it exists, and rerun npm run setup." >&2
  exit 1
}
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip install -q -r requirements.txt
./.venv/bin/pip install -q -r requirements-dev.txt

echo "==> Node packages"
npm install

echo "==> Storage"
mkdir -p storage/app

echo "==> Ollama"
if ! command -v ollama >/dev/null 2>&1; then
  case "$(uname -s)" in
    Linux)
      echo "Ollama not found; installing with the official script (needs sudo)."
      curl -fsSL https://ollama.com/install.sh | sh
      ;;
    Darwin)
      if command -v brew >/dev/null 2>&1; then
        echo "Ollama not found; installing with Homebrew."
        brew install ollama
      else
        echo "Ollama not found. Install it from https://ollama.com/download and rerun." >&2
        exit 1
      fi
      ;;
    *)
      echo "Ollama not found and no installer known for $(uname -s). See https://ollama.com/download" >&2
      exit 1
      ;;
  esac
fi

ollama_ready() { curl -sf http://localhost:11434/ >/dev/null 2>&1; }

# Wait for a server to bind the port, up to $1 seconds. "Started" is not
# "listening": the Linux installer's systemd unit (and a fresh install's
# first-run key generation) can take a few seconds before it binds, and a
# one-shot check in that window would make us start a second, competing copy.
wait_for_ollama() {
  for _ in $(seq 1 "$1"); do
    ollama_ready && return 0
    sleep 1
  done
  return 1
}

# On macOS (and Linux without systemd) nothing is listening after install,
# so start a server ourselves — but only once the wait has actually expired.
if ! wait_for_ollama 20; then
  echo "Starting ollama serve in the background (log: storage/ollama.log)"
  nohup ollama serve >storage/ollama.log 2>&1 &
  wait_for_ollama 30 || { echo "Ollama did not come up; see storage/ollama.log" >&2; exit 1; }
fi
echo "Ollama is running."
