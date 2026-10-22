# State management

The helper uses Python 3's standard library on macOS/Linux. It locates `state.json` relative to its own file, so changing projects does not change the saved destination. State changes use a lock and an atomic replacement. A missing file starts empty; malformed or unsupported state fails without resetting it.

Use absolute paths and normal shell quoting. These examples assume `skill_dir` is the installed skill directory:

```sh
python3 "$skill_dir/scripts/state.py" show
python3 "$skill_dir/scripts/state.py" show fitween
python3 "$skill_dir/scripts/state.py" set fitween \
  --name 'Fitween Blog' --url 'https://blog.fitween.app' \
  --account 'junnos.dev@gmail.com' --workflow moa \
  --repo '/Users/junnos/.t3/projects/blog'
python3 "$skill_dir/scripts/state.py" use fitween
python3 "$skill_dir/scripts/state.py" set fitween --account 'writer@fitween.app'
```

`set` creates or patches one profile without changing the default. New profiles require an HTTPS URL and a concrete email address; a domain such as `@fitween.app` is not an author identity. `use` changes the persistent default. Use `browser` for other blog platforms unless a specific workflow reference exists.

For a one-off account override, retain the saved profile and pass the chosen account to `record --account`. `--expected-account` must match the saved preference, detecting concurrent preference changes. Usually the two emails are identical.

```sh
python3 "$skill_dir/scripts/state.py" record fitween \
  --expected-account 'junnos.dev@gmail.com' --account 'junnos.dev@gmail.com' \
  --status draft --title '이번 작업에서 배운 점' --draft-path '/absolute/path/post.md'

python3 "$skill_dir/scripts/state.py" record fitween \
  --expected-account 'junnos.dev@gmail.com' --account 'junnos.dev@gmail.com' \
  --status published --title '이번 작업에서 배운 점' \
  --post-url 'https://blog.fitween.app/#/post/POST_ID' \
  --author 'junnos.dev@gmail.com' --draft-path '/absolute/path/post.md'
```

For an unregistered one-off destination, keep its result in the task's draft file and report it. Register a profile only when the user wants it remembered. A profile's record always belongs to its configured blog.

## Stored shape

```json
{
  "schema_version": 1,
  "default_blog": "fitween",
  "blogs": {
    "fitween": {
      "name": "Fitween Blog",
      "url": "https://blog.fitween.app",
      "account_email": "junnos.dev@gmail.com",
      "workflow": "moa",
      "repo_path": "/Users/junnos/.t3/projects/blog",
      "updated_at": "2026-10-22T00:00:00+00:00"
    }
  }
}
```

`last_result` is added by `record` and replaced for each stage/task. It contains `status`, `title`, `account_email`, `recorded_at`, and supplied `post_url`, `author_email`, or `draft_path`. Statuses are `draft`, `auth_required`, `submitting`, `uncertain`, and `published`. Preserve an unresolved submission until it has been reconciled. This is a latest-result record, not a publishing queue or audit log.

The helper stores metadata; it does not log in or publish. `published` requires a same-origin canonical URL and an observed author matching the chosen account. These checks catch accidental records but cannot prove that a post exists; the agent must verify the actual post first.

State files are written with owner-only permissions. Preserve `state.json` when upgrading this skill. Keep personal state out of shared/public skill repositories. For isolated testing, pass `--state-file /absolute/temp/state.json` before the subcommand.
