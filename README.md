# pydantypes

pydantypes is an extension to Pydantic that defines a collection of various datatypes relevant for cloud software engineering. It includes custom types for AWS, Azure, and Google Cloud services, as well as other commonly used non-native types.

## Installation

To install pydantypes, use pip:

```bash
pip install pydantypes
```

## Usage

Here is a simple example of how to use pydantypes:


```python
from pydantic import BaseModel
import pydantypes.aws.S3 as S3

class Data(BaseModel):
    uri: S3.Uri

data = Data(uri="s3://my-bucket/my-object")
print(data)
```

## Features

- AWS Types: Custom datatypes for various AWS services like S3, EC2, Lambda, etc.
- Azure Types: Custom datatypes for various Azure services like Blob Storage, VMs, Functions, etc.
- Google Cloud Types: Custom datatypes for various Google Cloud services like GCS, Compute Engine, Cloud Functions, etc.
- Other Types: Frequently used types that are not native but commonly appear in engineering.

