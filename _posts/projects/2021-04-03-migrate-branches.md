---
title: "Renaming master to main everywhere"
description: "A small Bash script that renames master to main across an account's GitHub repositories in one go."
tags: [open-source, bash, github]
---

migrate_branches is a small Bash script I wrote to ease the move from `master` to `main` on GitHub. It uses the GitHub REST API to find the repositories still using the old branch name and renames it in each one.

For every repository your token can see that belongs to `OWNER`, isn't archived, and still has the source branch as its default, it calls GitHub's branch rename endpoint. Renaming through the API means GitHub also:

- updates the default branch
- shows users a notice about the name change
- updates GitHub Pages setups that were based on the old branch

Usage, from the README:

```bash
GITHUB_TOKEN=xxxx \
OWNER=Jell \
SOURCE_BRANCH=master \
TARGET_BRANCH=main \
./migrate_branches.sh
```

Source on GitHub: [ReifyAB/migrate_branches](https://github.com/ReifyAB/migrate_branches)
