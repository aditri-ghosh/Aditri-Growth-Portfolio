#!/usr/bin/env python3
"""Fetch YouTube transcripts via the Supadata API and save them as Markdown."""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

SUPADATA_BASE_URL = "https://api.supadata.ai/v1"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "research" / "youtube-transcripts"
JOB_POLL_INTERVAL_SECONDS = 1
JOB_POLL_TIMEOUT_SECONDS = 300


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript from Supadata and save it as Markdown.",
    )
    parser.add_argument("url", help="YouTube video URL (e.g. https://www.youtube.com/watch?v=VIDEO_ID)")
    parser.add_argument(
        "--lang",
        default=None,
        help="Preferred transcript language code (ISO 639-1, e.g. en)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for saved transcripts (default: {DEFAULT_OUTPUT_DIR})",
    )
    return parser.parse_args()


def get_api_key() -> str:
    api_key = os.environ.get("SUPADATA_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Missing SUPADATA_API_KEY environment variable. "
            "Set it to your Supadata API key before running this script."
        )
    return api_key


def supadata_headers(api_key: str) -> dict[str, str]:
    return {
        "x-api-key": api_key,
        "Accept": "application/json",
    }


def raise_for_supadata_error(response: requests.Response) -> None:
    if response.ok:
        return

    try:
        payload = response.json()
        message = payload.get("message") or payload.get("error") or response.text
    except ValueError:
        message = response.text

    raise RuntimeError(f"Supadata API error ({response.status_code}): {message}")


def extract_youtube_video_id(url: str) -> str | None:
    patterns = (
        r"(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/|youtube\.com/live/)([A-Za-z0-9_-]{11})",
    )
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def sanitize_filename(title: str, max_length: int = 120) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        cleaned = "youtube-transcript"
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip(" .")
    return cleaned


def fetch_metadata(session: requests.Session, api_key: str, url: str) -> dict[str, Any]:
    response = session.get(
        f"{SUPADATA_BASE_URL}/metadata",
        headers=supadata_headers(api_key),
        params={"url": url},
        timeout=60,
    )
    raise_for_supadata_error(response)
    return response.json()


def request_transcript(
    session: requests.Session,
    api_key: str,
    url: str,
    lang: str | None,
) -> requests.Response:
    params: dict[str, str | bool] = {
        "url": url,
        "text": True,
        "mode": "auto",
    }
    if lang:
        params["lang"] = lang

    return session.get(
        f"{SUPADATA_BASE_URL}/transcript",
        headers=supadata_headers(api_key),
        params=params,
        timeout=120,
    )


def poll_transcript_job(
    session: requests.Session,
    api_key: str,
    job_id: str,
) -> dict[str, Any]:
    deadline = time.time() + JOB_POLL_TIMEOUT_SECONDS

    while time.time() < deadline:
        response = session.get(
            f"{SUPADATA_BASE_URL}/transcript/{quote(job_id, safe='')}",
            headers=supadata_headers(api_key),
            timeout=60,
        )
        raise_for_supadata_error(response)
        payload = response.json()

        status = payload.get("status")
        if status == "completed":
            return payload
        if status == "failed":
            error = payload.get("error") or payload.get("message") or "Unknown job failure"
            raise RuntimeError(f"Transcript job failed: {error}")

        time.sleep(JOB_POLL_INTERVAL_SECONDS)

    raise TimeoutError(f"Timed out waiting for transcript job {job_id}")


def extract_transcript_text(payload: dict[str, Any]) -> tuple[str, str | None, list[str]]:
    content = payload.get("content")
    lang = payload.get("lang")
    available_langs = payload.get("availableLangs") or []

    if isinstance(content, str):
        text = content.strip()
    elif isinstance(content, list):
        segments = []
        for segment in content:
            if isinstance(segment, dict):
                segment_text = segment.get("text", "").strip()
                if segment_text:
                    segments.append(segment_text)
            elif isinstance(segment, str) and segment.strip():
                segments.append(segment.strip())
        text = "\n\n".join(segments)
    else:
        text = str(content or "").strip()

    if not text:
        raise RuntimeError("Supadata returned an empty transcript.")

    return text, lang, available_langs


def fetch_transcript(
    session: requests.Session,
    api_key: str,
    url: str,
    lang: str | None,
) -> tuple[str, str | None, list[str]]:
    response = request_transcript(session, api_key, url, lang)

    if response.status_code == 202:
        payload = response.json()
        job_id = payload.get("jobId")
        if not job_id:
            raise RuntimeError("Supadata returned async processing without a job ID.")
        payload = poll_transcript_job(session, api_key, job_id)
    else:
        raise_for_supadata_error(response)
        payload = response.json()

    return extract_transcript_text(payload)


def format_markdown(
    *,
    title: str,
    url: str,
    transcript: str,
    lang: str | None,
    available_langs: list[str],
    author: str | None = None,
) -> str:
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# {title}",
        "",
        f"- **Source:** [{url}]({url})",
    ]

    if author:
        lines.append(f"- **Channel:** {author}")
    if lang:
        lines.append(f"- **Language:** {lang}")
    if available_langs:
        lines.append(f"- **Available languages:** {', '.join(available_langs)}")
    lines.extend(
        [
            f"- **Fetched:** {fetched_at}",
            "",
            "---",
            "",
            transcript,
            "",
        ]
    )
    return "\n".join(lines)


def build_output_path(output_dir: Path, title: str, video_id: str | None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = sanitize_filename(title)
    if video_id:
        base_name = f"{base_name} [{video_id}]"

    output_path = output_dir / f"{base_name}.md"
    if output_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = output_dir / f"{base_name} ({timestamp}).md"

    return output_path


def main() -> int:
    args = parse_args()
    api_key = get_api_key()
    video_id = extract_youtube_video_id(args.url)

    with requests.Session() as session:
        try:
            metadata = fetch_metadata(session, api_key, args.url)
        except RuntimeError as exc:
            print(f"Warning: could not fetch metadata ({exc}). Falling back to video ID.", file=sys.stderr)
            metadata = {}

        title = metadata.get("title") or (f"YouTube Video {video_id}" if video_id else "YouTube Transcript")
        author = None
        author_data = metadata.get("author")
        if isinstance(author_data, dict):
            author = author_data.get("displayName") or author_data.get("username")

        transcript, lang, available_langs = fetch_transcript(session, api_key, args.url, args.lang)

    markdown = format_markdown(
        title=title,
        url=args.url,
        transcript=transcript,
        lang=lang,
        available_langs=available_langs,
        author=author,
    )

    output_path = build_output_path(args.output_dir, title, video_id)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Saved transcript to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
