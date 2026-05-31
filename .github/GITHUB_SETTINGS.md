# GitHub Repository Settings

These settings are configured outside the repo (GitHub UI or API) and cannot
be enforced by files in the codebase. Re-apply these when setting up a fork
or new instance.

> **Public repos:** all settings below can be applied via `gh api`.
> **Private repos on free tier:** rulesets, secret scanning, push protection,
> and CodeQL must be set via the GitHub UI.

---

## Apply via `gh api` (replace `OWNER/REPO`)

```bash
# General settings
gh api repos/OWNER/REPO \
  --method PATCH \
  --field delete_branch_on_merge=true \
  --field default_branch=main

# Dependabot
gh api repos/OWNER/REPO/vulnerability-alerts --method PUT
gh api repos/OWNER/REPO/automated-security-fixes --method PUT

# Secret scanning + push protection
gh api repos/OWNER/REPO \
  --method PATCH \
  --header "Content-Type: application/json" \
  --input - <<'EOF'
{
  "security_and_analysis": {
    "secret_scanning": { "status": "enabled" },
    "secret_scanning_push_protection": { "status": "enabled" }
  }
}
EOF

# CodeQL default setup
gh api repos/OWNER/REPO/code-scanning/default-setup \
  --method PATCH \
  --input - <<'EOF'
{ "state": "configured", "query_suite": "default" }
EOF

# Branch ruleset: protect-main
gh api repos/OWNER/REPO/rulesets \
  --method POST \
  --header "Content-Type: application/json" \
  --input - <<'EOF'
{
  "name": "protect-main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks": []
      }
    }
  ]
}
EOF

# Tag ruleset: protect-version-tags
gh api repos/OWNER/REPO/rulesets \
  --method POST \
  --header "Content-Type: application/json" \
  --input - <<'EOF'
{
  "name": "protect-version-tags",
  "target": "tag",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["refs/tags/v*"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" }
  ]
}
EOF
```

> **Note on required status checks:** the `required_status_checks` array above
> is intentionally empty — GitHub only recognises job names after they've run
> once. After the first CI run, update the ruleset via:
> `PATCH /repos/OWNER/REPO/rulesets/{ruleset_id}`

---

## Current settings

### General
- Default branch: `main`
- Auto-delete head branches: enabled

### Branch protection (`main`)
- Require PR before merging: yes
- Required approvals: 0
- Dismiss stale reviews on push: yes
- Require review from code owners: yes
- Require conversation resolution: yes
- Require branch up to date: yes
- Block force pushes: yes
- Allow deletions: no
- Enforce on admins: yes

### Tag protection (`v*`)
- Ruleset name: `protect-version-tags`
- Restrict deletions: yes
- Restrict updates: yes

### Security & Analysis
- Secret scanning: enabled
- Push protection: enabled
- CodeQL (default setup): enabled
- Dependabot alerts: enabled
- Dependabot security updates: enabled
