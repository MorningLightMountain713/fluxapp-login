# Flux App Login Example

## Requirements

uv - https://docs.astral.sh/uv/getting-started/installation/

## Install

```bash
uv sync
```

## Usage

```
flux-login
```

This will generate a new key on each login - which is not what you want. You would want to generate a key one-time, then pass in the same key in the future.

Once logged in, you can use the auth header on subsequent calls that require authentication / authorization.
