---
description: Configuration for AI behavior when interacting with Codacy's MCP Server
applyTo: '**'
---
# Codacy Rules

## using any tool that accepts the arguments: `provider`, `organization`, or `repository`
- ALWAYS use:
  - provider: gh
  - organization: jpvelasco
  - repository: redstone-rigger

## CRITICAL: After ANY successful file edit
- Run `codacy_cli_analyze` for each edited file with `rootPath` = workspace path, `file` = edited file path, `tool` unset
- If issues found, propose and apply fixes before continuing

## CRITICAL: After dependency changes
- Run `codacy_cli_analyze` with `tool: "trivy"`
- Resolve any vulnerabilities before continuing
