from __future__ import annotations

import asyncio
from itertools import count
from json import JSONDecodeError
from socket import AF_INET
from typing import Any

from aiohttp import (
    BasicAuth,
    ClientConnectorError,
    ClientOSError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
    ConnectionTimeoutError,
    ContentTypeError,
    TCPConnector,
)
from rich.pretty import pprint
from yarl import URL


async def do_http(
    url: URL | str,
    verb: str = "get",
    *,
    data: Any = None,
    connect_timeout: int = 3,
    max_tries: int = 3,
    retry_interval: int = 1,
    credentials: dict | None = None,
    headers: dict | None = None,
    verify_ssl: bool | None = None,
    total_timeout: int | None = None,
) -> Any:
    timeout = ClientTimeout(connect=connect_timeout, total=total_timeout)
    conn = TCPConnector(family=AF_INET)

    auth = None
    res = None

    if credentials:
        # user password
        auth = BasicAuth(*credentials)

    if not headers:
        headers = {}

    async with ClientSession(
        connector=conn,
    ) as session:
        for attempt in count(start=1):
            if max_tries and attempt > max_tries:
                break

            remaining = max(0, max_tries - attempt)

            try:
                method = getattr(session, verb)
                async with method(
                    url,
                    timeout=timeout,
                    auth=auth,
                    headers=headers,
                    data=data,
                    ssl=verify_ssl,
                ) as resp:
                    resp: ClientResponse  # type: ignore

                    if resp.status in [429, 500, 502, 503, 504]:
                        if remaining or not max_tries:
                            await asyncio.sleep(retry_interval)
                        continue

                    if resp.status in [401, 403, 404]:
                        return None

                    try:
                        res = await resp.json()
                    except (JSONDecodeError, ContentTypeError):
                        res = None
                    break

            except (
                ClientConnectorError,
                ConnectionTimeoutError,
                ClientOSError,
                asyncio.TimeoutError,
            ):
                if remaining or not max_tries:
                    await asyncio.sleep(retry_interval)

    return res
