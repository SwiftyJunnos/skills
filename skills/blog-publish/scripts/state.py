#!/usr/bin/env python3
"""Manage local blog profiles and publication metadata; never authenticate or publish."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import parse_qsl, urlsplit

DEFAULT_STATE = Path(__file__).resolve().parent.parent / "state.json"
STATUSES = ("draft", "auth_required", "submitting", "uncertain", "published")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def email(value):
    require(isinstance(value, str) and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value),
            "Use a concrete email address, not a domain or login secret.")
    return value.lower()


def url(value, base=False):
    require(isinstance(value, str) and not any(c.isspace() for c in value), "Invalid URL.")
    parsed = urlsplit(value)
    require(parsed.scheme == "https" and parsed.hostname and not parsed.username
            and not parsed.password, "Use an HTTPS URL without credentials.")
    _ = parsed.port  # Validate malformed ports.
    if base:
        require(not parsed.query and not parsed.fragment, "Blog URLs cannot contain query or fragment data.")
    else:
        keys = [key.lower().replace("-", "_") for key, _ in parse_qsl(parsed.query)]
        require(not any(re.search(r"token|auth|secret|password|code|key|signature|session|jwt|otp", key)
                        for key in keys), "Store a canonical post URL without authentication parameters.")
        require(not re.search(r"(?:token|auth|secret|password|code|key|session|jwt|otp)=", parsed.fragment, re.I),
                "Store a canonical post URL without authentication parameters.")
    return value.rstrip("/") if base else value


def origin(value):
    parsed = urlsplit(value)
    return parsed.scheme, parsed.hostname, parsed.port or 443


def absolute_path(value):
    require(isinstance(value, str) and Path(value).is_absolute(), "Use an absolute file or repository path.")
    return value


def validate(data):
    require(isinstance(data, dict) and data.get("schema_version") == 1,
            "Unsupported or missing state schema; preserve the file and inspect it.")
    blogs = data.get("blogs")
    require(isinstance(blogs, dict), "State must contain a blogs object.")
    require("default_blog" in data and (data["default_blog"] is None or data["default_blog"] in blogs),
            "The default blog must reference an existing profile.")
    for blog_id, profile in blogs.items():
        require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", blog_id), "Invalid blog ID.")
        require(isinstance(profile, dict), "Invalid blog profile.")
        url(profile.get("url"), base=True)
        email(profile.get("account_email"))
        require(profile.get("workflow") in ("browser", "moa"), "Unknown blog workflow.")
        if "repo_path" in profile:
            absolute_path(profile["repo_path"])
        result = profile.get("last_result")
        if result is not None:
            require(isinstance(result, dict) and result.get("status") in STATUSES, "Invalid last result.")
            account = email(result.get("account_email"))
            require(isinstance(result.get("title"), str) and result["title"].strip(), "A result needs a title.")
            if "draft_path" in result:
                absolute_path(result["draft_path"])
            if "post_url" in result:
                url(result["post_url"])
                require(origin(result["post_url"]) == origin(profile["url"]), "Post URL must belong to this blog.")
            if "author_email" in result:
                email(result["author_email"])
            if result["status"] == "published":
                require(bool(result.get("post_url")), "Published results need a verified canonical post URL.")
                require(email(result.get("author_email")) == account, "Verified author must match the chosen account.")
    return data


def read(path):
    if not path.exists():
        return {"schema_version": 1, "default_blog": None, "blogs": {}}
    return validate(json.loads(path.read_text(encoding="utf-8")))


@contextmanager
def locked(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path) + ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def write(path, data):
    validate(data)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".state-", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def profile(data, blog_id):
    require(blog_id in data["blogs"], "Unknown blog ID; register the destination first.")
    return data["blogs"][blog_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE,
                        help="Override the state file for isolated testing.")
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show", help="Read all state or one blog profile.")
    show.add_argument("blog_id", nargs="?")
    set_profile = commands.add_parser("set", help="Create or patch a blog profile without changing the default.")
    set_profile.add_argument("blog_id")
    for option in ("name", "url", "account", "repo"):
        set_profile.add_argument("--" + option)
    set_profile.add_argument("--workflow", choices=("browser", "moa"))
    use = commands.add_parser("use", help="Select the persistent default blog.")
    use.add_argument("blog_id")
    record = commands.add_parser("record", help="Record observed progress; does not publish anything.")
    record.add_argument("blog_id")
    record.add_argument("--expected-account", required=True, help="Current saved profile account.")
    record.add_argument("--account", required=True, help="Account selected for this operation.")
    record.add_argument("--status", choices=STATUSES, required=True)
    record.add_argument("--title", required=True)
    record.add_argument("--post-url")
    record.add_argument("--author")
    record.add_argument("--draft-path")
    args = parser.parse_args()
    path = args.state_file.expanduser().absolute()
    try:
        if args.command == "show":
            data = read(path)
            output = profile(data, args.blog_id) if args.blog_id else data
        else:
            with locked(path):
                data = read(path)
                now = datetime.now(timezone.utc).isoformat(timespec="seconds")
                if args.command == "set":
                    current = data["blogs"].get(args.blog_id, {
                        "name": args.blog_id, "workflow": "browser"})
                    for argument, key, convert in (
                        (args.name, "name", str), (args.url, "url", lambda value: url(value, base=True)),
                        (args.account, "account_email", email), (args.repo, "repo_path", absolute_path),
                        (args.workflow, "workflow", str),
                    ):
                        if argument is not None:
                            current[key] = convert(argument)
                    current["updated_at"] = now
                    data["blogs"][args.blog_id] = current
                elif args.command == "use":
                    profile(data, args.blog_id)
                    data["default_blog"] = args.blog_id
                else:
                    current = profile(data, args.blog_id)
                    require(email(args.expected_account) == email(current["account_email"]),
                            "Saved account changed; reread the profile before recording.")
                    result = {"status": args.status, "title": args.title,
                              "account_email": email(args.account), "recorded_at": now}
                    for value, key in ((args.post_url, "post_url"), (args.author, "author_email"),
                                       (args.draft_path, "draft_path")):
                        if value is not None:
                            result[key] = email(value) if key == "author_email" else value
                    current["last_result"] = result
                write(path, data)
                output = data
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(f"State unchanged: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
