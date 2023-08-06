# aioredis-ratelimit

![python](https://img.shields.io/pypi/pyversions/aioredis-ratelimit.svg)
![version](https://img.shields.io/pypi/v/aioredis-ratelimit.svg)
![downloads](https://img.shields.io/pypi/dm/aioredis-ratelimit.svg)

An asyncio coroutine decorator for limiting calls' rate based on [Redis](https://redis.io/) backend and [aioredis](https://aioredis.readthedocs.io/en/latest/) library.

## Install

Use [pip](https://pip.pypa.io/en/stable/) package installer for Python:
```bash
python -m pip install --upgrade aioredis-ratelimit
```
Make sure you have Python 3.6 or later installed.

## Usage

```python
import aioredis
from aioredis_ratelimit import ratelimit


redis = aioredis.from_url('redis://127.0.0.1:6379/0')


@ratelimit(calls=1, period=timedelta(seconds=1), redis=redis)
async def coro():
  ...
```
If passing `raise_on_limit=True` to `@ratelimit(...)`, then a `aioredis_ratelimit.RateLimitExceeded` is raised when a decorated coroutine is called more times than the defined `calls` limit within the given time `period`.

## License

This is a free software licensed under the terms of the MIT License.
