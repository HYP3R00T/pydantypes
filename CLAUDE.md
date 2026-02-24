# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pydantypes — The missing types for Pydantic. Validated, constrained types for cloud (AWS/Azure/GCP), DevOps, web, data, and AI engineering identifiers.

**Repo**: https://github.com/oborchers/pydantypes | **Python**: 3.10+ | **Pydantic**: v2.5.2+

## Quick Start

```bash
make init        # Full setup: env + install + pre-commit
make check       # Run all: lint + typecheck + tests
```

## Development Commands

```bash
# Setup: env, install, init, sync
# Quality: format, format-check, lint, lint-fix, typecheck
# Testing: test, test-cov
# Build: build, clean
# All: check (lint+typecheck+tests)
```

### Pre-commit Hooks

**Auto** (every commit): format, lint (staged Python only) | **Manual**: typecheck, test

## Critical Rules

### Always Use UV

```bash
# Correct
uv run python script.py
uv run pytest tests/ -v
make test

# Wrong — never use python/pip directly
python script.py
pip install pydantypes
```

### Always Analyze Codebase Before Making Changes

Check existing patterns first, never invent new ones. See [ARCHITECTURE.md](ARCHITECTURE.md) for the canonical reference on type patterns (A/B/C/D), regex placement, docstring conventions, error handling, JSON schema, and test structure.

```bash
tree src/pydantypes/
grep -r "class.*Type" src/ --include="*.py" | head -20
```

### Avoid Lazy Imports

All imports at file top — ONLY exception is circular imports.

### Never Reference Removed Code in Comments

Comments describe what code DOES, not what it USED TO DO. Git tracks history.

### Check Before Creating Files

Prefer editing existing files. Never proactively create docs. Check structure first.

## Project Structure

```
src/pydantypes/
  __init__.py          # Package root, version import
  py.typed             # PEP 561 marker
  cloud/
    aws/               # S3 URIs, IAM ARNs, EC2 IDs, ...
    azure/             # Blob URIs, resource IDs, ...
    gcp/               # GCS URIs, project IDs, ...
  devops/              # Docker refs, semver, cron, ...
  web/                 # Endpoints, headers, MIME types, ...
  data/                # SQL identifiers, connection strings, ...
  ai/                  # LLM classification labels
tests/                 # Mirrors src structure
```

## Python and Formatting

**Ruff**: 100 chars, double quotes, 4-space indent, rules: E/F/UP/B/SIM/I/PLC/RUF/PT/N

### Modern Type Syntax (3.10+)

```python
# Correct — use built-in generics and union syntax
def process(val: str | int) -> str | None:
    items: list[dict[str, Any]] = []

# Wrong — old typing imports
from typing import Union, Optional, Dict, List
```

### Pydantic Patterns

Use `BaseModel` for all models. Avoid dataclasses.

```python
from pydantic import BaseModel, Field, field_validator

class Config(BaseModel):
    key: str = Field(..., min_length=1)

    @field_validator("key")
    @classmethod
    def validate_key(cls, v: str) -> str:
        if not v.startswith("sk-"):
            raise ValueError("must start with sk-")
        return v
```

### StrEnum for Constants

```python
from enum import StrEnum

class CloudProvider(StrEnum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
```

## Error Handling

```python
# Exception chaining (B904)
raise CustomError("msg") from e

# Unused loop variables: prefix with _
for name, _value in items:
    pass

# Flatten nested conditions (SIM102)
if c1 and c2 and c3:
    pass
```

## Testing

### Organization

Mirror src structure: `src/pydantypes/cloud/aws/s3.py` -> `tests/cloud/aws/test_s3.py`

1 test file per source file. Use fixtures in `conftest.py`, parametrize for multiple cases.

### Coverage: 90%+ Target

**Priority**: models -> validation errors -> happy path -> edge cases

```python
# Use dirty-equals for flexible assertions
from dirty_equals import IsStr, IsInstance

# Use real values in mocks, not Mock()
mock_settings.threshold = 0.5
```

## Versioning

Git tags `0.0.0` (no 'v' prefix) via hatch-vcs. `_version.py` is auto-generated at build time, never committed.

## Important Guidelines

- **UV only**: `uv run` for all Python execution
- **Quality**: Run `make format` / `make check` frequently
- **Git**: NEVER `git push` (user only), stage+commit only, meaningful messages
- **Files**: Avoid creating new files, prefer editing, NEVER proactive docs
- Use bullet lists, not numbered lists in documentation
