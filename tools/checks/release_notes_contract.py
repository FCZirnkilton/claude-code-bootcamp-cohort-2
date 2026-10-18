"""Acceptance check for Part 11: the frozen release-notes HTTP contract.

Run from a Shipyard repo. Starts the real server (`python3 -m notes_api.server`, configured with
PORT and NOTES_DB) on a free port with a throwaway database, creates notes through POST /api/notes
and checks only what briefs/release-notes-team.md freezes, so any implementation that honours the
contract passes, whatever its internal function names. Prints `contract ok` on success.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


def request(base: str, method: str, path: str, body: dict | None = None) -> tuple[int, str, str]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.headers.get("Content-Type", ""), resp.read().decode()
    except urllib.error.HTTPError as err:
        return err.code, err.headers.get("Content-Type", ""), err.read().decode()


def fail(message: str) -> None:
    sys.exit(f"contract broken: {message}")


def main() -> None:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "PORT": str(port), "NOTES_DB": os.path.join(tmp, "notes.db")}
        server = subprocess.Popen([sys.executable, "-m", "notes_api.server"], env=env,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        try:
            for _ in range(100):
                if server.poll() is not None:
                    fail(f"server exited: {server.stderr.read().strip().splitlines()[-1:]}")
                try:
                    socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                    break
                except OSError:
                    time.sleep(0.1)
            else:
                fail("server did not start within 10 s")

            notes = [
                {"title": "Contract alpha", "body": "Alpha first line\nmore", "tags": ["release:v1.4", "backend", "dashboard"]},
                {"title": "Contract beta", "body": "Beta first line", "tags": ["release:v1.4", "ops"]},
                {"title": "Contract gamma", "body": "Gamma first line", "tags": ["release:v1.3", "backend"]},
            ]
            for note in notes:
                status, _, text = request(base, "POST", "/api/notes", note)
                if status not in (200, 201):
                    fail(f"POST /api/notes -> {status} {text[:200]}")

            status, _, text = request(base, "GET", "/api/releases/v1.4/notes")
            if status != 200:
                fail(f"GET /api/releases/v1.4/notes -> {status} {text[:200]}")
            release = json.loads(text)
            if release.get("version") != "v1.4" or release.get("count") != 2:
                fail(f"expected version v1.4 and count 2, got {release.get('version')!r} / {release.get('count')!r}")
            filled = [s for s in release.get("sections", []) if s.get("notes")]
            if [s.get("title") for s in filled] != ["Backend", "Operations"]:
                fail(f"expected sections Backend, Operations; got {[s.get('title') for s in filled]}")
            if [s.get("key") for s in filled] != ["backend", "ops"]:
                fail(f"expected section keys backend, ops; got {[s.get('key') for s in filled]}")
            if json.dumps(release).count("Contract alpha") != 1:
                fail("a note tagged backend and dashboard must appear once, under Backend")
            if "Contract gamma" in text:
                fail("a v1.3 note appears in the v1.4 release")

            status, ctype, text = request(base, "GET", "/api/releases/v1.4/notes?format=markdown")
            if status != 200 or not ctype.startswith("text/markdown"):
                fail(f"?format=markdown -> {status} {ctype!r}")
            if "Alpha first line" not in text:
                fail("markdown changelog does not use the first body line")

            status, _, _ = request(base, "GET", "/api/releases/1.4/notes")
            if status != 400:
                fail(f"invalid version 1.4 -> {status}, expected 400")
        finally:
            server.terminate()
            server.wait(timeout=5)
    print("contract ok")


if __name__ == "__main__":
    main()
