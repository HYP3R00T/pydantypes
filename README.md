# pydantypes

[![CI](https://img.shields.io/github/actions/workflow/status/oborchers/pydantypes/ci.yml?branch=main&logo=github&label=CI)](https://github.com/oborchers/pydantypes/actions/workflows/ci.yml)
[![license](https://img.shields.io/github/license/oborchers/pydantypes.svg)](https://github.com/oborchers/pydantypes/blob/main/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**The missing types for Pydantic** — cloud, DevOps, web, and data engineering.

pydantypes provides validated, constrained Pydantic types for identifiers, ARNs, URIs, and resource names that appear everywhere in modern infrastructure code. Catch invalid values at parse time, not at deploy time.

## Installation

```bash
pip install pydantypes
```

## Quick Example

```python
from pydantic import BaseModel
from pydantypes.cloud.aws import S3Uri, IamRoleArn

class PipelineConfig(BaseModel):
    source: S3Uri
    execution_role: IamRoleArn

config = PipelineConfig(
    source="s3://my-bucket/data/input.parquet",
    execution_role="arn:aws:iam::123456789012:role/pipeline-role",
)
# Invalid values are rejected immediately:
# PipelineConfig(source="not-an-s3-uri", ...)  -> ValidationError
```

## Domains

| Domain | Package | Examples |
|--------|---------|----------|
| **AWS** | `pydantypes.cloud.aws` | S3 URIs, IAM ARNs, Lambda function names, EC2 instance IDs |
| **Azure** | `pydantypes.cloud.azure` | Blob Storage URIs, resource IDs, Key Vault names |
| **GCP** | `pydantypes.cloud.gcp` | GCS URIs, project IDs, Cloud Run service names |
| **DevOps** | `pydantypes.devops` | Docker image refs, semver strings, cron expressions |
| **Web** | `pydantypes.web` | Endpoint paths, header names, MIME types |
| **Data** | `pydantypes.data` | SQL identifiers, connection strings, column names |

## Compatibility

pydantypes is designed as a complement to [pydantic-extra-types](https://github.com/pydantic/pydantic-extra-types). While pydantic-extra-types covers general-purpose types (colors, phone numbers, payment cards), pydantypes focuses on infrastructure and engineering identifiers.

- Requires **Pydantic v2.5.2+**
- Supports **Python 3.10–3.13**

## Development

```bash
# Clone and set up
git clone https://github.com/oborchers/pydantypes.git
cd pydantypes
make init

# Run checks
make check        # lint + typecheck + test
make format       # auto-format code
make test-cov     # tests with coverage report
```

## License

MIT
