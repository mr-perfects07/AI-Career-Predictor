#!/bin/bash
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install it, then double-click run.command again."
  read -r -p "Press Return to close this window. "
  exit 1
fi

python3 backend/server.py &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null' EXIT INT TERM
sleep 1
open "http://127.0.0.1:8000"
wait "$server_pid"
