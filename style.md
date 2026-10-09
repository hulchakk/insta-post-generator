# Commit & Code Style Guide

## Git Commits

**Format:** `type(scope): description`

**Types:**

* `feat` — new feature or capability
* `fix` — bug fix
* `refactor` — rewrite without changing behavior
* `docs` — documentation updates
* `chore` — dependencies, build config, general cleanup

**Rules:**

* Imperative tone, lowercase description, no period at end
* Scope in parentheses is the affected module/feature (e.g., `auth`, `payments`, `settings`)
* Action-oriented verbs: "add X", "fix Y", "remove Z" (not "added", "fixing")
* Keep subject line under 50 characters
* Body (if needed): explain *why*, not *what* — the diff shows what
* Single author (no unnecessary co-author tags)

**Examples:**

```text
fix(auth): use environment variable for token validation
feat(payments): add lesson balance refund logic
refactor(docker): switch to production application runner

```

---

## Code Style

**Self-documenting code:**

* **No comments** unless the *WHY* is non-obvious (business rules, workarounds, invariants)
* Skip comments or docstrings that state what the code already clearly shows

**Naming:**

* Full words, clear intent, no cryptic shortcuts (`charged_before` instead of `cb`, `send_receipt_task` instead of `sr_task`)
* Functions name the action and outcome directly (`consume_lessons`, `refund_lessons`, `get_charged_user_ids`)

**Abstractions & Architecture:**

* Keep it simple: do not build abstractions for single-use cases or hypothetical future needs
* Inline helper utils used only once or twice
* Rely on framework/language guarantees; avoid redundant error handling for impossible states

**Testing:**

* One clear, runnable test per feature/bugfix
* Minimal setup — avoid unnecessary fixtures, heavy mocks, or testing framework built-ins

---

## README

**Audience:** Developer or reviewer who wants to understand, build, and run the project fast.

**Structure:**

1. **Hero:** One line explaining what the project is
2. **Why:** One sentence on the problem it solves
3. **Tech Stack:** Concise list or table of core technologies and why they were chosen
4. **Getting Started:** Quick local setup in 2–3 copy-paste commands
5. **Key Decisions:** Core architectural trade-offs or solutions to common pitfalls
6. **Status / Roadmap:** Honest, short list of next steps or current limitations

**Tone & Content:**

* Explain features from the user's perspective first, then the technical implementation
* Direct and clear — no marketing fluff or filler
* Code blocks in README: only commands to run or deploy (avoid pasting long code snippets)

---

## Persistent Work

**One branch per feature or fix:**

* Branch off `develop`, merge back into `develop`; `main` only takes tested releases
* Name: `type/scope-description`, same types and scopes as commits, kebab-case (`feat/video-background-music`, `fix/publish-youtube-token-refresh`)
* Small focused commits on the branch, never commit straight to `develop` or `main`

**Test-driven (red → green → refactor):**

1. Write the failing test first: one plain `assert` test in `tests/test_<module>.py`, run it, see it fail for the right reason
2. Write the minimum code that makes it pass
3. Simplify with the test green, then run every check from `README.md`
* Bug fix starts with a test that reproduces the bug
* Pure logic (parsing, timing, validation, prompts' post-processing) is always tested; paid API calls, renders and publishing are not run, only the code around them

**Minimal code (ponytail mode, always on):**

* Before writing: does it need to exist → already in the codebase → stdlib → installed dependency → one line → only then new code
* Shortest diff that fixes the root cause, no scaffolding for later
* A deliberate shortcut with a known limit gets a `ponytail:` comment naming the limit and the upgrade path

**Finish the job:**

* A task is done when tests and typechecks are green, `README.md` matches the new behaviour, and the branch is ready to merge
* Don't stop at the first error: find the root cause, fix it, rerun the checks

---

## Workflow Rules

**When to ask questions:**

* Feature scope or priority trade-offs
* Choosing between two valid architectural choices
* Environment or deployment configuration details

**What to skip:**

* Comments restating obvious code logic
* Abstractions without current usage
* Over-engineering for unrequested edge cases
